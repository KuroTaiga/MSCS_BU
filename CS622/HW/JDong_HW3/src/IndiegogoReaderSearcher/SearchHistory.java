package IndiegogoReaderSearcher;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class SearchHistory{
	// class of objs that stores the SearchHistory
	// as stated in HW3, we need to store the frequency of the search, the timeStamp for each search
	private int frequency;
	private List<String> timeStamps;
	
	public SearchHistory() {
		this.frequency = 0;
		this.timeStamps = new ArrayList<>();
	}
	
	public void increaseFrequency() {
		this.frequency++;
	}
	public int getFrequency() {
		return this.frequency;
	}
	
	public void addTimeStamps() {
		//add a new timeStamp at the time of the search
		LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String timestamp = now.format(formatter);
		this.timeStamps.add(timestamp);		
	}
	public List<String> getTimeStamps(){
		return this.timeStamps;
	}
}
