/*******************************************************************************
 * Copyright 2017 McGill University All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/
/*******************************************************************************
Modified by
BENOIT ?
?
2021
 *******************************************************************************/
package asmvec;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//import com.fasterxml.jackson.databind.ObjectMapper;
import static java.util.stream.Collectors.*;

import java.io.Serializable;
import java.util.ArrayList;

import static java.lang.Math.sqrt;

public class LearnerAsm2Vec implements Serializable {

	private static final long serialVersionUID = -743890181829256933L;

	private static Logger logger = LoggerFactory.getLogger(LearnerAsm2Vec.class);
	
	// New parameters to fit asm2vec paper
	public static class Asm2VecNewParam extends Param {
		private static final long serialVersionUID = -817341338942724187L;
		public int min_freq = 1;
		public int vec_dim = 200;
		public double optm_subsampling = -1;//1e-4;
		public double optm_initAlpha = 0.025;
		public int optm_window = 2;
		public int optm_negSample = 25;
		public int optm_iteration = 50;
		public int optm_aphaUpdateInterval = 10000;
		public int num_rand_wlk = 10;
		public double optm_iteration_test_ratio = 0.5;
		public long seed = 2;
		public boolean useSeed = false;
	}

	public Consumer<Integer> iterationHood = null;

	public Map<String, NodeWord> vocab = null;
	public Map<String, NodeWord> trainDocMap = null;
	public List<NodeWord> vocabL = null;
	public int[] pTable;
	public transient volatile double alpha;
	public transient volatile long tknCurrent;
	public transient volatile long tknLastUpdate;
	public transient volatile int iteration = 0;
	public volatile long tknTotal;
	public volatile boolean debug = true;
	public Asm2VecNewParam param;
	
	private RandL rl = null;

	private void preprocess(List<FuncTokenized> funcs) {
		
		
		if (this.param.useSeed)
		{
			rl = new RandL(this.param.seed);
		}
		else
		{
			rl = new RandL();
		}
		
		
		vocab = null;

		// frequency map:
		final HashMap<String, Long> counter = new HashMap<>();
		funcs.forEach(func -> func.forEach(blk -> blk
				.forEach(token -> counter.compute(token.trim().toLowerCase(), (w, c) -> c == null ? 1 : c + 1))));
		


		// add additional word (for /n)
		counter.put("</s>", Long.MAX_VALUE);

		// create word nodes (matrix)
		vocab = counter.entrySet().stream().parallel().filter(en -> en.getValue() >= param.min_freq)
				.collect(toMap(Map.Entry::getKey, p -> new NodeWord(p.getKey(), p.getValue())));

		// total valid word count
		tknTotal = vocab.values().stream().filter(w -> !w.token.equals("</s>")).mapToLong(w -> w.freq).sum();

		// vocabulary list (sorted)
		vocabL = vocab.values().stream().sorted((a, b) -> b.token.compareTo(a.token))
				.sorted((a, b) -> Double.compare(b.freq, a.freq)).collect(toList());

		// reset frequency for /n
		vocabL.get(0).freq = 0;

		// initialize matrix:
		vocabL.stream().forEach(node -> node.init(param.vec_dim, rl));

		// sub-sampling probability
		if (param.optm_subsampling > 0) {
			double fcount = param.optm_subsampling * tknTotal;
			vocabL.stream().parallel().forEach(w -> w.samProb = (sqrt(w.freq / fcount) + 1) * fcount / w.freq);
		}

		pTable = MathUtilities.createPTbl(vocabL, (int) 1e8, 0.75);

		// if (debug)
		logger.info("Vocab {}; Total {};", vocabL.size(), tknTotal);

		trainDocMap = new HashMap<>();
		funcs.forEach(func -> trainDocMap.put(func.id, new NodeWord(func.id, 1)));
		trainDocMap.values().forEach(node -> node.init(this.param.vec_dim, rl));
		
		/*for (String c : vocab.keySet())
		{
			System.out.println(c);
		}*/
	}

	public static class ShuffleWrapper<T> implements Iterable<T> {
		private List<T> ls;

		public ShuffleWrapper(List<T> ls) {
			this.ls = ls;
		}

		@Override
		public Iterator<T> iterator() {
			Collections.shuffle(this.ls);
			return this.ls.iterator();
		}
	}

	private void gradientDecend(final List<FuncTokenized> funcs, Map<String, NodeWord> funcMap, long numTkns,
			long alphaUpdateInterval, boolean updateWordVec, int iteration) {
		
		tknLastUpdate = 0;
		tknCurrent = 0;

		for (int it = 0; it < iteration; it++)
		{	
			Collections.shuffle(funcs);
			for (FuncTokenized func : funcs)
			{
				double[] bfIn = new double[param.vec_dim], bfNeul1e = new double[param.vec_dim];
				
				// update alpha:
				if (tknCurrent - tknLastUpdate > alphaUpdateInterval) {
					alpha = param.optm_initAlpha * (1.0 - 1.0 * tknCurrent / (numTkns * param.optm_iteration + 1));
					alpha = alpha < param.optm_initAlpha * 0.00001 ? param.optm_initAlpha * 0.00001 : alpha;
					tknLastUpdate = tknCurrent;
				}
				iterate(func.rep(this.param.num_rand_wlk, this.rl), funcMap.get(func.id), rl, bfIn, bfNeul1e, updateWordVec);
			}
		}
	}

	private void iterate(List<List<List<String>>> seqs, NodeWord docNode, RandL rl, double[] bfIn, double[] bfNeul1e,
			boolean updateWordVec) {

		
		for (List<List<String>> in_strs : seqs)
		{
			List<List<NodeWord>> ins = in_strs.stream()
					.map(in -> in.stream().map(tkn -> vocab.get(tkn.trim().toLowerCase()))//
							.filter(Objects::nonNull)//
							.peek(node -> tknCurrent++)//
							.collect(toList()))
					.filter(in -> in.size() > 0)//
					.collect(Collectors.toList());

			for (int k = 1; k < ins.size() - 1; ++k) {
				List<NodeWord> context = new ArrayList<>();
				context.addAll(ins.get(k - 1));
				context.addAll(ins.get(k + 1));
				//System.out.println(context);
				for (int j = 0; j < ins.get(k).size(); ++j) {
					NodeWord target = ins.get(k).get(j);
					EntryPair<NodeWord, List<NodeWord>> cont = new EntryPair<>(target, context);
					pred(cont, docNode, bfIn, bfNeul1e, updateWordVec);
				}
			}
		}

	}


	private void pred(EntryPair<NodeWord, List<NodeWord>> cont, NodeWord docNode, double[] bfIn,
			double[] neul1e, boolean updateWordVec) {
		double[] errors;
		errors = neul1e;
		Arrays.fill(bfIn, 0.0);
		Arrays.fill(errors, 0.0);
		cont.value.stream().forEach(src -> MathUtilities.add(bfIn, src.neuIn));
		
		MathUtilities.add(bfIn, docNode.neuIn);
		MathUtilities.div(bfIn, cont.value.size() + 1);
		ngSamp(cont.key, bfIn, errors, updateWordVec);
		
		if (updateWordVec)
		{
			cont.value.stream().forEach(src -> MathUtilities.add(src.neuIn, errors));
		}
		MathUtilities.add(docNode.neuIn, errors);
	}
	
	// Random number generation simplified
	private void ngSamp(NodeWord tar, double[] in, double[] neul1e, boolean updateWordVec) {
		for (int i = 0; i < param.optm_negSample + 1; ++i) {
			double label;
			double[] out;
			// NodeWord target;
			if (i == 0) {
				label = 1;
				out = tar.neuOut;
			} else {
				label = 0;
				int tarInd = this.rl.nextChoice(pTable.length); //(int) Long.remainderUnsigned(this.rl.nextR() >>> 16, pTable.length);
				NodeWord rtar = vocabL.get(pTable[tarInd]);
				if (rtar == tar)
					continue;
				out = rtar.neuOut;
			}
			double f = MathUtilities.exp(MathUtilities.dot(in, out));
			double g = (label - f) * alpha;
			MathUtilities.dxpay(neul1e, out, g);
			if (updateWordVec)
				MathUtilities.dxpay(out, in, g);
		}
	}

	public void train(List<FuncTokenized> funcs) throws InterruptedException, ExecutionException {
		alpha = param.optm_initAlpha;
		preprocess(funcs);
		gradientDecend(funcs, trainDocMap, tknTotal, param.optm_aphaUpdateInterval, true, param.optm_iteration);
	}
	
	/*public void cont_train(Iterable<FuncTokenized> funcs) throws InterruptedException, ExecutionException {
		gradientDecend(funcs, trainDocMap, tknTotal, param.optm_aphaUpdateInterval, true,  param.optm_iteration, param.optm_parallelism);
	}*/
	
	// Modified for simplicity
	public Map<String, double[]> infer(List<FuncTokenized> funcs) {
		alpha = param.optm_initAlpha;
		this.debug = false;
		try {

			HashMap<String, NodeWord> inferDocMap = new HashMap<>();
			funcs.forEach(doc -> inferDocMap.put(doc.id, new NodeWord(doc.id, 1)));

			inferDocMap.values().forEach(node -> node.init(this.param.vec_dim, this.rl));

			long tknTotalInDocs = StreamSupport.stream(funcs.spliterator(), false).flatMap(func -> func.blks.stream())
					.flatMap(blk -> blk.ins.stream()).flatMap(in -> in.stream()).filter(tkn -> vocab.containsKey(tkn))
					.count();
			
			int iteration = (int) (param.optm_iteration  * param.optm_iteration_test_ratio);
			if (iteration == 0)
			{
				iteration = 1;
			}
			
			gradientDecend(funcs, inferDocMap, tknTotalInDocs, 0, false, iteration);
			Map<String, double[]> result = inferDocMap.entrySet()
					.stream()
					.map(ent -> new EntryPair<>(ent.getKey(), ent.getValue().neuIn))
					.collect(Collectors.toMap(ent -> ent.key, ent -> MathUtilities.normalize(MathUtilities.cp(ent.value))));

			/*StreamSupport.stream(funcs.spliterator(), false)
					.map(doc -> trainDocMap.get(doc.id))
					.filter(node -> node != null)//
					.forEach(node -> result.put(node.token, MathUtilities.normalize(MathUtilities.cp(node.neuIn))));*/

			

			return result;
		} catch (Exception e) {
			logger.info("Failed to learn new doc vector.", e);
			return null;
		}
	}
/*
	public WordEmbedding produce() {
		WordEmbedding embedding = new WordEmbedding();
		embedding.vocabL = vocabL.stream().map(node -> new EntryPair<>(node.token, convertToFloat(node.neuIn)))
				.collect(toList());
		try {
			embedding.param = (new ObjectMapper()).writeValueAsString(this.param);
		} catch (Exception e) {
			logger.error("Failed to serialize the parameter. ", e);
		}
		return embedding;
	}
*/
	int last_doc_vec_map_ite = -1;

	public Map<String, double[]> produceNormalizedDocEmbdCpy() {
		Map<String, double[]> embd = this.produceDocEmbdCpy();
		return MathUtilities.normalize(embd);
	}

	public Map<String, double[]> produceDocEmbdCpy() {
		return trainDocMap.entrySet().stream().collect(toMap(ent -> ent.getKey(), ent -> MathUtilities.cp(ent.getValue().neuIn)));
	}

	public LearnerAsm2Vec(Asm2VecNewParam param) {
		this.param = param;
	}
}
