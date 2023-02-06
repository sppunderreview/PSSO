/*******************************************************************************
BENOIT ?
?
2021
 *******************************************************************************/
package asmvec;

import java.io.File;
//import java.io.FileNotFoundException;
import java.util.ArrayList;
//import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
//import java.util.regex.Matcher;
//import java.util.regex.Pattern;
//import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class DisassemblyFactorySimple extends DisassemblyFactory {

	private static Logger logger = LoggerFactory.getLogger(DisassemblyFactory.class);

	public DisassemblyFactorySimple(int bathSize) {
		this.batchSize = bathSize;
	}

	public DisassemblyFactorySimple() {
		this(10000);
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

	@Override
	public BinarySurrogateMultipart loadAsMultiPart(String binaryPath, String name, int batchSize, boolean rebase,
			boolean cleanStack) throws Exception {
		try {

			//File script = new File("/home/?/Documents/Travail/?/asm2veck/ExtractBinaryViaIDA2.py");

			List<File> parts = this.selectOutputFiles(binaryPath);
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
