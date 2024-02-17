package hw4;

import java.util.Random;

public class GenomeThread implements Runnable {
    private String source;
    private int seqLength;
    private boolean verbose;
	private char ThreadID;
	private int sequencesToGenerate;
	// constructer for each thread
	public GenomeThread(char ThreadID, int seqLength, String source, int sequencesToGenerate, boolean verbose){
		this.ThreadID = ThreadID;
		this.seqLength = seqLength;
		this.source = source;
		this.sequencesToGenerate = sequencesToGenerate;
		this.verbose = verbose;
	}
	
	//Getters
	public char getID() {
		return this.ThreadID;
	}
	
	public int getSeqToGen() {
		return this.sequencesToGenerate;
	}
	
	//setters
	public void setSeqToGen(int sequencesToGenerate) {
		this.sequencesToGenerate = sequencesToGenerate;
	}
	
	@Override
	//function for running each thread, generate the number of sequence as assigned to
	public void run() {
		for (int i= 0 ; i<this.sequencesToGenerate;i++) {
			String curr = generateRandomSequence();
			if (this.verbose) {
				System.out.println(curr);
			}	
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
