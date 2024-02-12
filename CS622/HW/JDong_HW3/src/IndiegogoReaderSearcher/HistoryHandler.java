package IndiegogoReaderSearcher;

import java.util.*;

public class HistoryHandler {
	//This is the handler class for fetching and writing to the search history
	
	//map between the keyword as keys to their corresponding SearchHistory objs
	private Map<String, SearchHistory> searchHistory;
	
	public HistoryHandler() {
		//initialize an empty history
		this.searchHistory = new HashMap<>();
	}
		
	public void addSearchHistory(String keyword) {
		SearchHistory history;
		if (searchHistory.containsKey(keyword)){
			// has already searched for this keyword
			history = searchHistory.get(keyword);
			
		} else {
			// new keyword, haven't been searched previously
			history = new SearchHistory();
		}
		// Increase the frequency and add a new timeStamp now
		history.addTimeStamps();
		history.increaseFrequency();
		
		searchHistory.put(keyword, history);
	}
	
	public String getKeywordHistory(String keyword) {
		//this function returns a string that contains the keyword, the frequency and all the time stamps
		// associated with that keyword
		StringBuilder summary = new StringBuilder("Regarding the keyword"+keyword+": \n");
		if (searchHistory.containsKey(keyword)) {
			SearchHistory currHistory = searchHistory.get(keyword);
			summary.append("Frequency: ").append(currHistory.getFrequency()).append(", Timestamps: ").append(currHistory.getTimeStamps()).append("\n");
		} else {
			// in case the keyword is not in the searchHistory
			summary.append("There's no history for this keyword.");
		}
		return summary.toString();
	}
	
	public String getAllHistory() {
		// this function is the quick way of returning all search history
		StringBuilder summary = new StringBuilder("Number of unique search terms: " + searchHistory.size() + "\n");
		// append each search history
		for (Map.Entry<String, SearchHistory> entry : searchHistory.entrySet()) {
			String currKey = entry.getKey();
			SearchHistory currHistory = entry.getValue();
			summary.append("Key: '").append(currKey).append("', Frequency: ").append(currHistory.getFrequency()).append(", Timestamps: ").append(currHistory.getTimeStamps()).append("\n");
		}
		return summary.toString();
	}
	
	
	
	
}
