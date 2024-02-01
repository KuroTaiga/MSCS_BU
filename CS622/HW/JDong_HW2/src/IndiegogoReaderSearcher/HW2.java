package IndiegogoReaderSearcher;

import java.io.*;


public class HW2 {	
	public static void main(String[] args) {
		String outputPath = "mergedIndiegogo.txt";
		String[] inputFiles = {"Indiegogo_2023-09-15T20_40_31_339Z.json","Indiegogo_2023-10-17T11_11_05_408Z.json",
				"Indiegogo_2023-11-17T20_40_31_433Z.json","Indiegogo_2023-12-15T20_40_32_423Z.json",
				"Indiegogo_2024-01-15T14_13_29_668Z.json"};
		mergeFiles(inputFiles,outputPath);
		System.out.println("Merged files");
		String[] keywords = {"fitness","wearable"};
		for(String keyword : keywords) {
			keywordSearcher(keyword,outputPath);
		}
	}
	
	public static void mergeFiles(String[] inputFiles, String outputFile) {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))){ 
			//Saw this try-with-resource when doing research on how to write the hw, thought it would be cool
			for(String currPath : inputFiles) {
				try (BufferedReader reader = new BufferedReader(new FileReader(currPath))) {
					String line;
					while((line = reader.readLine()) != null) {
						writer.write(line);
						writer.newLine();
					}
				}catch(IOException e) {
					e.printStackTrace();
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void keywordSearcher(String keyword, String path) {
		try (BufferedReader reader = new BufferedReader(new FileReader(path))){
			String currLine;
			while ((currLine = reader.readLine())!=null) {
				if(currLine.contains(keyword)) {
					//Using the java default method for finding the keyword
					//Not messing around to write a more efficient search method
					System.out.println(currLine);
					lineParser(currLine);
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void lineParser(String line) {
		String[] splitLine = line.split(",");
	
		for (String curr : splitLine) {
			if(curr.contains("funds_raised_percent") || curr.contains("close_date")) {
				System.out.print(curr);
			}
		}
		System.out.println();
	}
}

