package IndiegogoReaderSearcher;

import java.io.*;


public class MergerSearcher {	
	// The following functions are taken from HW2 with modifications based on the comments/feedbacks
	public MergerSearcher() {
		// constructor place holder
		// can be modified in the future when need arrives
	}
	
	public static void runHW2() {
		// main function that runs the whole show
		// It calls the merge and search function
		String outputPath = "mergedIndiegogo.txt";
		String[] inputFiles = {"Indiegogo_2023-09-15T20_40_31_339Z.json","Indiegogo_2023-10-17T11_11_05_408Z.json",
				"Indiegogo_2023-11-17T20_40_31_433Z.json","Indiegogo_2023-12-15T20_40_32_423Z.json",
				"Indiegogo_2024-01-15T14_13_29_668Z.json"};
		
		mergeFiles(inputFiles,outputPath);
		
		//String[] categories = {"\"category\"","\"tags\"","\"category_url\"","\"tagline\""};
		//Legacy code from HW2
		
		//System.out.println("Merged files");
		
		// testing the searcher function
		//String[] keywords = {"fitness","wearable"};
		//for(String keyword : keywords) {
		//  	keywordSearcher(keyword,outputPath,categories);
		//}
	}
	
	// This function merges a list of files and write the result into a single output file
	// 2/11: included more info about when error occurred in the catch lines
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
					System.out.println("Error in reading the file: "+currPath);
					e.printStackTrace();
				}
			}
		} catch (IOException e) {
			System.out.println("Error in merging the files");
			e.printStackTrace();
		}
	}
	
	public static void keywordSearcher(String keyword, String[] categories) {
		// Updated so that it searches in the correct categories
		// fixing the path that we are searching for this assignment
		String outputPath = "mergedIndiegogo.txt";
		Boolean found = false;
		
		try (BufferedReader reader = new BufferedReader(new FileReader(outputPath))){
			String currLine;
			while ((currLine = reader.readLine())!=null) {
				// Splitting the line into different parts
				Boolean foundInLine = false;
				String[] currSplit = currLine.split(",");
				for (String currSection : currSplit) {
					// The search stops if the current line already has a match or partial match
					if (foundInLine) {
						break;
					}
					for (String currCategory: categories){
						if((currSection.contains(keyword)) && (currSection.contains(currCategory))){
							//Using the java default method for finding the keyword
							//Not messing around to write a more efficient search method
							//Prints the category that the keyword is found
							found = true;
							foundInLine = true;
							System.out.println(String.format("Keyword (%s) (or partial match) here: %s",keyword,currSection));
							linePrinter(currLine);
						}
					}
				}
			}
			if (!found){
				System.out.println("No match or partial match of keyword");
			}
		} catch (IOException e) {
			System.out.println("Exception happened during search");
			e.printStackTrace();
		}
	}
	// Print out the desired search result for the 2 categories 
	public static void linePrinter(String line) {
		String[] splitLine = line.split(",");
		for (String curr : splitLine) {
			if(curr.contains("funds_raised_percent") || curr.contains("close_date")) {
				System.out.print(curr);
			}
		}
		System.out.println();
	}
}

