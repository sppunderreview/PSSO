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

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class DisassemblyFactoryIDA extends DisassemblyFactory {

	private static Logger logger = LoggerFactory.getLogger(DisassemblyFactory.class);

	public static String PATH_IDA;
	private static File idaw64;
	private static File idaw32;

	public DisassemblyFactoryIDA(String idaPath, int bathSize) {
		this.batchSize = bathSize;
		PATH_IDA = idaPath;
				
		File file = new File(PATH_IDA + "/idaw64.exe");
		if (file.exists())
			idaw64 = file;
		file = new File(PATH_IDA + "/idal64");
		if (file.exists())
			idaw64 = file;
		file = new File(PATH_IDA + "/idat64.exe");
		if (file.exists())
			idaw64 = file;
		file = new File(PATH_IDA + "/idat64");
		if (file.exists())
			idaw64 = file;
		if (idaw64 == null) {
			logger.warn(
					"The IDAw/t/l 64bit version does not exist. The engine wont be able to process .i64 file. Path {}",
					PATH_IDA);
		}

		file = new File(PATH_IDA + "/idaw.exe");
		if (file.exists())
			idaw32 = file;
		file = new File(PATH_IDA + "/idal32");
		if (file.exists())
			idaw32 = file;
		file = new File(PATH_IDA + "/idat.exe");
		if (file.exists())
			idaw32 = file;
		file = new File(PATH_IDA + "/idat");
		if (file.exists())
			idaw32 = file;
		if (idaw32 == null) {
			logger.warn("Cannot find IDAw/t/l 32 bit version. The engine wont be able to process .idb file. Path {} ",
					PATH_IDA);
		}

	}

	public DisassemblyFactoryIDA(String k) {
		this(k, 10000);
	}

	public void clean(String binaryFile) {
		File

		// f1 = new File(binaryFile + ".tmp");
		// if (f1.exists())
		// f1.delete();

		f1 = new File(binaryFile.substring(0, binaryFile.lastIndexOf('.')) + ".i64");
		if (f1.exists())
			f1.delete();
	}

	@Override
	public void init() {

	}

	@Override
	public void close() {

	}

	public List<File> selectOutputFiles(String binaryPath) {
		File binary = new File(binaryPath);
		int i = 0;
		ArrayList<File> files = new ArrayList<>();
		String fileName = binary.getName();
		// for ida 7+
		while (true) {
			File candidate = new File(binary.getParentFile().getAbsolutePath() + "/" + fileName + ".tmp" + i + ".json");
			if (!candidate.exists())
				break;
			files.add(candidate);
			i++;
		}
		// for ida < 7 (only if it contains '.'; otherwise duplicated file in list)
		if (fileName.contains(".")){
			fileName = fileName.substring(0, fileName.lastIndexOf('.'));
			while (true) {
				File candidate = new File(binary.getParentFile().getAbsolutePath() + "/" + fileName + ".tmp" + i + ".json");
				if (!candidate.exists())
					break;
				files.add(candidate);
				i++;
			}
		}
		return files;
	}
	
	// Modified for simplicity
	@Override
	public BinarySurrogateMultipart loadAsMultiPart(String binaryPath, String name, int batchSize, boolean rebase,
			boolean cleanStack) throws Exception {

		if (idaw64 == null || !idaw64.exists()) {
			throw new FileNotFoundException(
					"Failed to locate IDAPRO. The engine will not be able to disassemble. Check configuration or Try other implementation.");
		}

		String fname = (new File(binaryPath)).getName();
				
		try {

			File script = new File("/home/?/Documents/Travail/?/asm2veck/ExtractBinaryViaIDA2.py");
			
			

			List<File> parts = this.selectOutputFiles(binaryPath);
			String[] arg = null;
			if (parts == null || parts.size() < 1) {
				if (fname.endsWith(".i64"))
					arg = new String[] { idaw64.getAbsolutePath(), "-A", "-S" + script.getAbsolutePath(), binaryPath };
				else if (fname.endsWith(".idb"))
					arg = new String[] { idaw32.getAbsolutePath(), "-A", "-S" + script.getAbsolutePath(), binaryPath };
				else
					arg = new String[] { idaw64.getAbsolutePath(), "-A", "-S" + script.getAbsolutePath(), binaryPath };

				System.out.println(StringResources.JOINER_TOKEN.join(arg));

				ProcessBuilder pBuilder = new ProcessBuilder(arg);
				pBuilder.directory(script.getParentFile());
				pBuilder.environment().put("K_BATCHSIZE", Integer.toString(batchSize));
				pBuilder.environment().put("K_REBASE", Integer.toString(rebase ? 1 : 0));
				pBuilder.environment().put("K_CLEANSTACK", cleanStack ? Integer.toString(1) : Integer.toString(0));
				Process p = pBuilder.start();
				p.waitFor();
				parts = this.selectOutputFiles(binaryPath);
			} else {
				//logger.info("Found existing binary surrogate. Skip disassembling for {}", binaryPath);
			}
		
			if (parts == null || parts.size() < 1) {
				logger.error("Failed to parse the assembly file. The output file parts cannot be located.");
				throw new Exception("Failed to disasemble the given file.");
			}

			// clean(binaryPath);
			List<File> newParts = parts;
			Iterable<BinarySurrogate> surrogateParts = () -> new Iterator<BinarySurrogate>() {

				Iterator<File> ite = newParts.iterator();

				@Override
				public boolean hasNext() {
					return this.ite.hasNext();
				}

				@Override
				public BinarySurrogate next() {
					BinarySurrogate binarySurrogate;
					try {
						binarySurrogate = BinarySurrogate.load(ite.next());
						binarySurrogate.name = name;
						binarySurrogate.processRawBinarySurrogate();
						return binarySurrogate;
					} catch (Exception e) {
						logger.error("Failed to parse the output json file.", e);
						return null;
					}

				}
			};

			return new BinarySurrogateMultipart(surrogateParts, newParts.size());

		} catch (Exception e) {
			logger.error("Failed to parse the assembly file.", e);
			throw e;
		}
	}

}
