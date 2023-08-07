/*******************************************************************************
BENOIT Tristan
These
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
	public static void main(String[] args) throws Exception
	{
		String nameEXP = "test";
		String nameId = "1";
		String pathToData = "/home/tristan/Documents/Travail/These/Basic/BigCorrection/BOC/"; //"/home/tristan/Documents/Travail/These/BigC/BOC/";	
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
	}
}
