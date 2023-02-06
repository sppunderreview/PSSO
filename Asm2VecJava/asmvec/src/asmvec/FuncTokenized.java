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

import java.util.ArrayList;
import java.util.Arrays;
//import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.google.common.collect.Iterables;
//import com.google.common.collect.Lists;


public class FuncTokenized implements Iterable<FuncTokenized.BlockTokenized> {

	public String id;
	public String name;
	public List<BlockTokenized> blks = new ArrayList<>();
	public List<Long> calls = new ArrayList<>();
	public List<List<List<String>>> edgesCovering = null;

	public Document toDocument() {
		Document doc = new Document();
		doc.id = id;
		blks.stream().map(blk -> new Sentence(blk.ins.stream().flatMap(in -> in.stream()).collect(Collectors.toList())))
				.forEach(doc.sentences::add);
		return doc;
	}

	/**
	 * Lazy convertion.
	 * 
	 * @param binaries
	 * @param inline_threshold
	 * @return
	 */
	public static List<FuncTokenized> convert(Iterable<? extends BinaryMultiParts> binaries, double inline_threshold) {
		Iterable<List<FuncTokenized>> itb = Iterables.transform(Iterables.concat(binaries),
				bin -> convert(Arrays.asList(bin), inline_threshold));
		
		List<FuncTokenized> funcs = new ArrayList<FuncTokenized>();
	
		Iterator<List<FuncTokenized>> it = itb.iterator();
	      while(it.hasNext())
	      {
	    	  List<FuncTokenized> subList = (List<FuncTokenized>) it.next();
	    	  for (FuncTokenized f : subList)
	    	  {
	    		  funcs.add(f);
	    	  }
	      }
		//terable<FuncTokenized> funcs = Iterables.concat(itb);
		return funcs;
	}
	
	// Modified to fit better asm2vec paper
	public static List<FuncTokenized> convert(List<Binary> bins, double inline_threshold) {
		if (inline_threshold < 0)
			return bins.stream().flatMap(bin -> bin.functions.stream()).map(func -> new FuncTokenized(func))
					.collect(Collectors.toList());
		Map<String, FuncTokenized> func_map = bins.stream().flatMap(bin -> bin.functions.stream())
				.map(func -> new FuncTokenized(func)).collect(Collectors.toMap(func -> func.id, func -> func, (x1, x2) -> x1));

		Map<String, Integer> indegrees = new HashMap<>();

		func_map.values().stream().flatMap(func -> func.calls.stream())
				.forEach(call -> indegrees.compute(Long.toString(call), (k, v) -> v == null ? 1 : v + 1));

		return func_map.values().stream().map(func -> {

			FuncTokenized nfunc = new FuncTokenized();
			nfunc.id = func.id;
			nfunc.calls = func.calls;
			nfunc.name = func.name;
			nfunc.blks.addAll(func.blks);
			int lS = nfunc.blks.size();
			
			func.calls.stream().map(call -> func_map.get(Long.toString(call))).filter(call -> call != null)
					.filter(call -> {
						int in = indegrees.get(call.id);
						int ou = call.calls.size();
						double alpha = ou * 1.0 / (in + ou);
						
						int lC = call.blks.size();
						return alpha <= inline_threshold && ((lC < (lS * 0.6)) || lS < 10);
					}).forEach(call -> nfunc.blks.addAll(call.blks));
			
			nfunc.computeEdgesCovering();
			return nfunc;
		}).collect(Collectors.toList());
	}

	public FuncTokenized(Function func) {
		this.id = Long.toString(func.functionId);
		this.name = func.binaryName + "_" + func.functionName.toLowerCase() + "_" + this.id;
		this.blks = func.blocks.stream().map(blk -> new FuncTokenized.BlockTokenized(blk)).collect(Collectors.toList());
		this.calls = func.callingFunctionIds;
	}

	public FuncTokenized() {
	}

	@Override
	public Iterator<FuncTokenized.BlockTokenized> iterator() {
		return blks.iterator();
	}

	// Modified to fit better asm2vec paper
	public List<List<List<String>>> rep(int num_rand_wlk, RandL rand)
	{
		List<List<List<String>>> sequences = new ArrayList<List<List<String>>>(this.edgesCovering);
		//System.out.println("SIZE "+ sequences.size());
		for (int i = 0; i < num_rand_wlk; ++i)
			sequences.add(randomWalk(rand));
		return sequences;
	}

	// Modified to fit better asm2vec paper
	private  List<List<String>> randomWalk(RandL rand) {
		if (this.blks.size() < 1)
			return new ArrayList<>();
		Map<String, FuncTokenized.BlockTokenized> blks = this.blks.stream()
				.collect(Collectors.toMap(blk -> blk.id, blk -> blk));
		HashSet<String> blk_ids = new HashSet<>();
		List<FuncTokenized.BlockTokenized> walk = new ArrayList<>();
		FuncTokenized.BlockTokenized current = this.blks.get(0);
		while (current.callingBlocks.size() > 0 && !blk_ids.contains(current.id)) {
			walk.add(current);
			blk_ids.add(current.id);
			List<FuncTokenized.BlockTokenized> cblks = current.callingBlocks.stream().map(cid -> blks.get(cid))
					.collect(Collectors.toList());
			current = cblks.get(rand.nextChoice(cblks.size()));
		}
		return walk.stream().flatMap(blk -> blk.ins.stream()).collect(Collectors.toList());
	}
	
	// Added to fit better asm2vec paper
	private void computeEdgesCovering() 
	{
		Map<String, FuncTokenized.BlockTokenized> blks = this.blks.stream()
				.collect(Collectors.toMap(blk -> blk.id, blk -> blk));
		
		this.edgesCovering = new ArrayList<>();
		for (int i = 0; i < this.blks.size(); i++)
		{
			List<FuncTokenized.BlockTokenized> cblks = this.blks.get(i).callingBlocks.stream().map(cid -> blks.get(cid))
					.collect(Collectors.toList());
			
			for (FuncTokenized.BlockTokenized next : cblks)
			{
				List<FuncTokenized.BlockTokenized> walk = new ArrayList<>();
				walk.add(this.blks.get(i));
				walk.add(next);
				this.edgesCovering.add(walk.stream().flatMap(blk -> blk.ins.stream()).collect(Collectors.toList()));
			}
		}
	}

	public static class BlockTokenized implements Iterable<String> {
		public String id;
		public List<List<String>> ins = new ArrayList<>();
		public List<String> callingBlocks = new ArrayList<>();

		public BlockTokenized(Block blk) {
			this.id = Long.toString(blk.blockId);
			this.ins = blk.getAsmLines().stream().filter(in -> in.size() > 0)
					.map(in -> insToToken(in, blk.dat.get(Long.parseLong(in.get(0).replace("0x", ""), 16))))
					.collect(Collectors.toList());
			this.callingBlocks = blk.callingBlocks.stream().map(val -> Long.toString(val)).collect(Collectors.toList());
		}

		public BlockTokenized() {
			// TODO Auto-generated constructor stub
		}

		private static List<String> insToToken(List<String> ins, String dat) {
			ArrayList<String> n_tokens = ins.subList(1, ins.size()).stream()
					.flatMap(in -> Arrays.stream(in.split("[\\+\\-\\*\\\\\\[\\]:\\(\\)\\s]"))
							.peek(ele -> ele.toLowerCase().trim())
							.filter(ele -> ele.trim().length() > 0 && !ele.startsWith("loc_") && !ele.startsWith("sub_")
									&& !ele.startsWith("var_") && !ele.contains("word_")))
					.collect(Collectors.toCollection(ArrayList::new));
			if (dat != null && dat.length() > 0)
				n_tokens.add(dat);
			return n_tokens;
		}

		@Override
		public Iterator<String> iterator() {
			return ins.stream().flatMap(in -> in.stream()).iterator();
		}
	}
}