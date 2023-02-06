/*******************************************************************************
BENOIT ?
?
2021
 *******************************************************************************/
package asmvec;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

public final class Main {
	
	/*
	public static void main(String[] args) throws Exception
	{
		String pathToData = "/home/?/Documents/Travail/?/Virus/samples/";	

		if (args.length == 1)
		{
			pathToData = args[0];
		}
		
		DisassemblyFactory factory  = DisassemblyFactory.getDefaultDisassemblyFactory();

		// Binary
		for (int i = 0; i < 474; i++)
		{
			long startTime = System.currentTimeMillis();
			
			File fTrain = new File(pathToData+i);
			DisassemblyFactory.disassembleSingle(fTrain,factory);
			long estimatedTime = System.currentTimeMillis() - startTime;
			
			System.out.println(i+" "+estimatedTime/1000.0);
			try
			{
			    FileWriter fw = new FileWriter("VirusJsons.csv",true);
			    fw.write(i+";"+ estimatedTime+"\n");
			    fw.close();
			}
			catch(IOException ioe)
			{
			    System.err.println("IOException: " + ioe.getMessage());
			}
		}
	}*/
	
	
	public static void main(String[] args) throws Exception
	{
		String pathToData = "/home/?/Documents/Travail/?/LinuxDataset/normal/motivating/programsASM/";	

		if (args.length == 1)
		{
			pathToData = args[0];
		}
		
		File folder = new File(pathToData);
		List<File> listOfNames = new ArrayList<File>(Arrays.asList(folder.listFiles()));
		listOfNames.removeIf((File f) -> f.getName().substring(f.getName().length()-3).equals("elf") == false);
		Collections.sort(listOfNames, (a, b) -> a.getName().compareTo(b.getName()));		
		Collections.shuffle(listOfNames, new Random(42));	
		DisassemblyFactory factory  = DisassemblyFactory.getSimpleDisassemblyFactory();
		
		
		int i = 0;
		for (File fTrain : listOfNames)
		{
			List<Binary> bListTrain = new ArrayList<Binary>();
			System.out.println(i);
			Binary bTrain = DisassemblyFactory.disassembleSingle(fTrain,factory).processRawBinarySurrogate().toBinary();		
			bListTrain.add(bTrain);
		
			BinaryMultiParts bMultiTrain = new BinaryMultiParts(bListTrain, bListTrain.size());
			List<BinaryMultiParts> binariesTrain = new ArrayList<BinaryMultiParts>();
			binariesTrain.add(bMultiTrain);
			
			List<FuncTokenized> funcList = FuncTokenized.convert(binariesTrain, -1);
			Set<String> functionsToRemove = new HashSet<String>();
	
			for (FuncTokenized f : funcList)
			{
				String nameF = f.name;
				int numsBlocks = f.blks.size();
							
				boolean toRemove = false;
				
				if (numsBlocks  == 0)
				{
					toRemove = true;
				}
				else if (numsBlocks == 1)
				{
					if (f.blks.get(0).ins.size() == 1)
					{
						toRemove = true;
					}
				}
				
				if (toRemove)
				{
					functionsToRemove.add(nameF);
				}
			}
			
	
			try (Writer writer = new BufferedWriter(new OutputStreamWriter(
		              new FileOutputStream("FTM/FTR_M_"+i+".txt"), "utf-8")))
			{
				writer.write(functionsToRemove.toString());
			}
			i+=1;
		}
	}
	
	/*
	public static void main(String[] args) throws Exception
	{
		String nameEXP = "motivating";
		Integer id = 0;
		Integer P = 200;
		String pathToData = "/home/?/Documents/Travail/?/LinuxDataset/normal/motivating/programsASM/";	
		Integer epochs = 1;
		
		double learningRate = 0.05;
		double modeTrainEpochs = 1;
		
		if (args.length == 4)
		{
			pathToData = args[0];
			id = Integer.parseInt(args[1]);
			P = Integer.parseInt(args[2]);	
			epochs = Integer.parseInt(args[3]);
		}
		
		// Seek files
		File folder = new File(pathToData);
		List<File> listOfNames = new ArrayList<File>(Arrays.asList(folder.listFiles()));		
		listOfNames.removeIf((File f) -> f.getName().substring(f.getName().length()-3).equals("elf") == false);
		Collections.sort(listOfNames, (a, b) -> a.getName().compareTo(b.getName()));		
		Collections.shuffle(listOfNames, new Random(42));
		
		// Select chunk
		List<File> chunk = new ArrayList<File>();
		for (int i = 0; i < listOfNames.size(); i++)
		{
			if (i % P == id)
			{
				chunk.add(listOfNames.get(i));
			}
		}
		listOfNames = null;
		
		// Split into train and test sets
		List<File> listTrain = new ArrayList<File>();
		List<File> listTest = new ArrayList<File>();
		for (int i = 0; i < chunk.size(); i++)
		{
			if (i % 2 == 0)
			{
				listTrain.add(chunk.get(i));
				continue;
			}
			listTest.add(chunk.get(i));
		}

		
		
		DisassemblyFactory factory  = DisassemblyFactory.getSimpleDisassemblyFactory();

		// Train
		List<Binary> bListTrain = new ArrayList<Binary>();
		for (File fTrain : listTrain)
		{
			Binary bTrain = DisassemblyFactory.disassembleSingle(fTrain,factory).processRawBinarySurrogate().toBinary();		
			bListTrain.add(bTrain);
		}
				
		BinaryMultiParts bMultiTrain = new BinaryMultiParts(bListTrain, bListTrain.size());
		List<BinaryMultiParts> binariesTrain = new ArrayList<BinaryMultiParts>();
		binariesTrain.add(bMultiTrain);
		
		// Test
		List<Binary> bListTest = new ArrayList<Binary>();
		for (File fTest : listTest)
		{
			Binary bTest = DisassemblyFactory.disassembleSingle(fTest,factory).processRawBinarySurrogate().toBinary();		
			bListTest.add(bTest);
		}
				
		BinaryMultiParts bMultiTest = new BinaryMultiParts(bListTest, bListTest.size());
		List<BinaryMultiParts> binariesTest = new ArrayList<BinaryMultiParts>();
		binariesTest.add(bMultiTest);
		
		// Experience
		Asm2VecCloneDetector detector = Asm2VecCloneDetector.getDefaultDetector();
		detector.param.optm_iteration = epochs;
		detector.param.optm_initAlpha = learningRate;
		detector.param.optm_iteration_test_ratio = modeTrainEpochs;

		
		Map<String, double[]>  vectors = detector.experience(binariesTrain, binariesTest);
		
		
		try (Writer writer = new BufferedWriter(new OutputStreamWriter(
	              new FileOutputStream("experiment_"+nameEXP+"_"+id+".txt"), "utf-8")))
		{
			writer.write(epochs +"\n");
			writer.write(learningRate +"\n");
			writer.write(modeTrainEpochs +"\n");
			
			for (Map.Entry<String, double[]> entry : vectors.entrySet())
			{
				String nameF = entry.getKey();
				double[] vector = entry.getValue();
				writer.write(nameF +"\n");
				for (Double l : vector)
				{
					writer.write(l +"\n");
				}
			    //System.out.println(nameF + "/" + vector.length);
			}
		}
		 System.out.println("END EXPERIMENT");
	}
	*/
	
	/*
	public static void main(String[] args) throws Exception
	{
		String nameEXP = "test";
		String nameId = "1";
		String pathToData = "/home/?/Documents/Travail/?/BigC/BOC/";	
		Integer epochs = 1;
		String part0 = "O0";
		String part1 = "O1";
		
		double learningRate = 0.05;
		double modeTrainEpochs = 1;
		
		if (args.length == 6)
		{
			nameEXP = args[0];
			nameId = args[1];
			pathToData = args[2];
			epochs = Integer.parseInt(args[3]);
			part0 = args[4];
			part1 = args[5];
		}
		
		List<Integer> part0Files = new ArrayList<Integer>();
		List<Integer> part1Files = new ArrayList<Integer>();
		
		
		// Select options / versions
		BufferedReader reader;
		try
		{
			reader = new BufferedReader(new FileReader(
					pathToData+"samples.txt"));
			String line = reader.readLine();
			
			line = reader.readLine();
			while (line != null)
			{
				int idS;
				try {
					idS = Integer.parseInt(line);
				}
				catch (NumberFormatException e)
				{
					idS = 0;
				}
								
				line = reader.readLine();
				
				if (line.contains(part0))
				{
					part0Files.add(idS);
				}
				else if (line.contains(part1))
				{
					part1Files.add(idS);
				}
				
				line = reader.readLine();
			}
			reader.close();
		}
		catch (IOException e) 
		{
			e.printStackTrace();
		}
		
		//System.out.println(args.length);		
		DisassemblyFactory factory  = DisassemblyFactory.getSimpleDisassemblyFactory();

		// Train
		List<Binary> bListTrain = new ArrayList<Binary>();
		for (int i : part1Files)
		{
			File fTrain = new File(pathToData+"json/"+i);
			Binary bTrain = DisassemblyFactory.disassembleSingle(fTrain,factory).processRawBinarySurrogate().toBinary();		
			bListTrain.add(bTrain);
		}
		
		BinaryMultiParts bMultiTrain = new BinaryMultiParts(bListTrain, bListTrain.size());
		List<BinaryMultiParts> binariesTrain = new ArrayList<BinaryMultiParts>();
		binariesTrain.add(bMultiTrain);
		
		// Test
		
		List<Binary> bListTest = new ArrayList<Binary>();
		for (int i : part0Files)
		{
			File fTest = new File(pathToData+"/json/"+i);
			Binary bTest = DisassemblyFactory.disassembleSingle(fTest,factory).processRawBinarySurrogate().toBinary();		
			bListTest.add(bTest);
		}

		BinaryMultiParts bMultiTest = new BinaryMultiParts(bListTest, bListTest.size());
		List<BinaryMultiParts> binariesTest = new ArrayList<BinaryMultiParts>();
		binariesTest.add(bMultiTest);
		
		// Experience
		Asm2VecCloneDetector detector = Asm2VecCloneDetector.getDefaultDetector();
		detector.param.optm_iteration = epochs;
		detector.param.optm_initAlpha = learningRate;
		detector.param.optm_iteration_test_ratio = modeTrainEpochs;

		
		Map<String, double[]>  vectors = detector.experience(binariesTrain, binariesTest);
		
		
		try (Writer writer = new BufferedWriter(new OutputStreamWriter(
	              new FileOutputStream("experiment_"+nameEXP+"_"+nameId+".txt"), "utf-8")))
		{
			writer.write(epochs +"\n");
			writer.write(learningRate +"\n");
			writer.write(modeTrainEpochs +"\n");
			
			for (Map.Entry<String, double[]> entry : vectors.entrySet())
			{
				String nameF = entry.getKey();
				double[] vector = entry.getValue();
				writer.write(nameF +"\n");
				for (Double l : vector)
				{
					writer.write(l +"\n");
				}
			    //System.out.println(nameF + "/" + vector.length);
			}
		}
		 System.out.println("END EXPERIMENT");
	}*/
	
	
	
	/*
	public static void main(String[] args) throws Exception
	{
		String pathToData = "/home/?/Documents/Travail/?/BigOptions/samples/";	

		if (args.length == 1)
		{
			pathToData = args[0];
		}
		
		Set<String> functionsToRemove = new HashSet<String>();

		DisassemblyFactory factory  = DisassemblyFactory.getDefaultDisassemblyFactory();


		// Binary
		List<Binary> bList = new ArrayList<Binary>();
		List<Integer> toCorrect = new ArrayList<Integer>();
		toCorrect.add(5);
		toCorrect.add(6);
		toCorrect.add(12);
		
		for (int i : toCorrect)
		{
			File fTrain = new File(pathToData+i);
			Binary bTrain = DisassemblyFactory.disassembleSingle(fTrain,factory).processRawBinarySurrogate().toBinary();		
			bList.add(bTrain);
		}
		
		BinaryMultiParts bMulti = new BinaryMultiParts(bList, bList.size());
		List<BinaryMultiParts> bMList = new ArrayList<BinaryMultiParts>();
		bMList.add(bMulti);
		
		List<FuncTokenized> funcList = FuncTokenized.convert(bMList, -1);
		
		for (FuncTokenized f : funcList)
		{
			String nameF = f.name;
			int numsBlocks = f.blks.size();
						
			boolean toRemove = false;
			
			if (numsBlocks  == 0)
			{
				toRemove = true;
			}
			else if (numsBlocks == 1)
			{
				if (f.blks.get(0).ins.size() == 1)
				{
					toRemove = true;
				}
			}
			
			if (toRemove)
			{
				functionsToRemove.add(nameF);
			}
		}
		

		try (Writer writer = new BufferedWriter(new OutputStreamWriter(
	              new FileOutputStream("functionsToRemoveBOCorrected.txt"), "utf-8")))
		{
			writer.write(functionsToRemove.toString());
		}

	}*/

}
