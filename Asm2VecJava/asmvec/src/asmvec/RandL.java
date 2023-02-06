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
package asmvec;

import java.util.Random;

public class RandL {
	
	private Random generator = new Random();

	public RandL() {
		long seed = this.generator.nextLong();
		this.generator.setSeed(seed);
		System.out.println("Seed RANDOM: "+seed);
	}
	
	public RandL(long seed) {
		this.generator =  new Random(seed);
		System.out.println("Seed : "+seed);
	}

	public long nextR() {
		return generator.nextLong();
	}

	/*public int nextResidue(int max) {
		return (int) Long.remainderUnsigned(this.nextR(), max);
	}*/
	
	public int nextChoice(int size)
	{
		return generator.nextInt(size);
	}

	public double nextF() {
		return generator.nextDouble();
	}

	/*public static void main(String[] args) {
		RandL rl = new RandL(0);
		for (int i = 0; i < 1000; ++i) {
			System.out.println(rl.nextF());
		}
	}*/
}
