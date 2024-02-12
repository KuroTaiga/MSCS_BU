package IndiegogoReaderSearcher;
import java.util.*;
public class UserGUI {
	// This is a basic user interface that makes the testing process easier
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		HistoryHandler historyHandler = new HistoryHandler();
		// right now I'm fixing the categories to be searched. In future of course I can make it into
		// some user input
		final String[] CATEGORIES = {"\"category\"","\"tags\"","\"category_url\"","\"tagline\""};
		// Build the files that used for getting the search
		System.out.println("Running merge file");
		try {
			MergerSearcher.runHW2();
			System.out.println("Merge passed");
		} catch(Exception e) {
			System.out.println("Merge failed");
			e.printStackTrace();
		}
		
		while(true) {
			System.out.println("Enter a keyword to search for: ");
			String inLine = scanner.nextLine();
			if("quit".equalsIgnoreCase(inLine.trim())) {
				//use quit to quit out of the loop
				System.out.println("Bye");
				break;
			} else if("OneWordHistory".equals(inLine.trim())) {
				//only prints out the history regarding the next keyword
				System.out.println("Keyword:");
				String keyword  = scanner.nextLine().trim();
				System.out.println(historyHandler.getKeywordHistory(keyword));
			} else if ("GetAll".equals(inLine.trim())){
				System.out.println(historyHandler.getAllHistory());
			} else {
				// not hitting any preset commands, must be searching for a keyword
				MergerSearcher.keywordSearcher(inLine, CATEGORIES);
				historyHandler.addSearchHistory(inLine);
			}
		}
		scanner.close();
	}
}
