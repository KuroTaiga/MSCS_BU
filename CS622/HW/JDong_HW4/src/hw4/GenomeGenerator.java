package hw4;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
public class GenomeGenerator {
	private String source;
    private int seqLength;
    private int totalSeq;
    private boolean verbose;
    private List<String> allSequence;
        
    public GenomeGenerator(int seqLength,int totalSeq,String source,boolean verbose) {
    	this.seqLength = seqLength;
    	this.totalSeq = totalSeq;
    	this.source = source;
    	this.allSequence = new ArrayList<>();
    	this.verbose = verbose;
    }
    // calls to generate the number of sequence as requested
    public void runGenomeGenerator() {
    	for (int i=0;i<this.totalSeq;i++) {
    		String curr = this.generateRandomSequence();
    		allSequence.add(curr);
    		if (this.verbose) System.out.println(curr);
    	}
    }
	// randomly pick characters from the source and add it to the string sequence
	// return with the sequence
    private String generateRandomSequence() {
        StringBuilder sequence = new StringBuilder(this.seqLength);
        Random random = new Random();
        for (int i = 0; i < this.seqLength; i++) {
            sequence.append(this.source.charAt(random.nextInt(this.source.length())));
        }
        return sequence.toString();
    }
}
