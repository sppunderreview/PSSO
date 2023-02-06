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

public class Counter {
	public volatile int count = 0;

	public void inc() {
		count++;
	}

	public int incRO() {
		count++;
		return count - 1;
	}

	public void inc(int val) {
		count += val;
	}

	public double percentage(int total) {
		return count * 1.0 / total;
	}

	public void dec(int val) {
		count -= val;
	}

	public void dec() {
		count--;
	}

	public int getVal() {
		return count;
	}

	public static Counter zero() {
		return new Counter();
	}
}
