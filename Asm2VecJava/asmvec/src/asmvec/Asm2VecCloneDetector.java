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

import java.io.Serializable;
//import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
//import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
//import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//import com.google.common.collect.Iterables;
//import com.google.common.collect.Lists;

public class Asm2VecCloneDetector implements Serializable {

	private static final long serialVersionUID = 9037582236777128453L;
	
	// Modified for simplicity
	public static Asm2VecCloneDetector getDefaultDetector() {
		LearnerAsm2Vec.Asm2VecNewParam param = new LearnerAsm2Vec.Asm2VecNewParam();
		return getDefaultDetector(param);
	}

	public static Asm2VecCloneDetector getDefaultDetector(LearnerAsm2Vec.Asm2VecNewParam param) {
		if (MathUtilities.expTable == null)
			MathUtilities.createExpTable();
		Asm2VecCloneDetector detector = new Asm2VecCloneDetector(param);
		return detector;
	}

	private static Logger logger = LoggerFactory.getLogger(Asm2VecCloneDetector.class);

	public LearnerAsm2Vec asm2vec = null;
	public LearnerAsm2Vec.Asm2VecNewParam param;
	public Consumer<Integer> hood = null;

	public Asm2VecCloneDetector(LearnerAsm2Vec.Asm2VecNewParam param) {
		this.param = param;
	}

	/*private boolean isExtern(Function func) {
		return func.blocks.get(0).codes.get(0).get(1).trim().equalsIgnoreCase("extrn");
	}*/



	public transient List<Binary> last_index;

	// New experience function
	public Map<String, double[]>  experience(Iterable<? extends BinaryMultiParts> binariesTrain, Iterable<? extends BinaryMultiParts> binariesTest)
			throws Exception {

		asm2vec = new LearnerAsm2Vec(param);
		asm2vec.debug = false;
		asm2vec.iterationHood = this.hood;
		
		List<FuncTokenized> funcListTrain = FuncTokenized.convert(binariesTrain, 0.01);
		Collections.shuffle(funcListTrain);
		logger.info("TRAIN PHASE");
		logger.info("Total {} documents", funcListTrain.size());
		
		long startTime = System.currentTimeMillis();
		asm2vec.train(funcListTrain);
		long estimatedTime = System.currentTimeMillis() - startTime;
		System.out.println("LEARNING "+(estimatedTime/1000.0) + "s.");
		
	
		Map<String, double[]> vectorsTrain =   asm2vec.produceNormalizedDocEmbdCpy();
		Map<String, double[]> result = new HashMap<String, double[]>();
		
		for (FuncTokenized f : funcListTrain)
		{
				result.put(f.name, vectorsTrain.get(f.id));
		}
		
		logger.info("TEST PHASE");
		
		List<FuncTokenized> funcListTest = FuncTokenized.convert(binariesTest, 0.01);
		Collections.shuffle(funcListTest);
		logger.info("Total {} documents", funcListTest.size());
		
		startTime = System.currentTimeMillis();
		Map<String, double[]> vectorsTest =   asm2vec.infer(funcListTest);
		estimatedTime = System.currentTimeMillis() - startTime;
		System.out.println("LEARNING "+(estimatedTime/1000.0) + "s.");
				
		for (FuncTokenized f : funcListTest)
		{
				result.put(f.name, vectorsTest.get(f.id));
		}
		
		return result;
	}
	
	protected void indexFuncsToBeImplByChildren(long appId, List<Binary> binaries)
			throws Exception {

		throw new UnsupportedOperationException();
	}



}
