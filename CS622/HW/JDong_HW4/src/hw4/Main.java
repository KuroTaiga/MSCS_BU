package hw4;
import java.lang.System;
public class Main {
	private static long runtime;
	// the total number of sequences to generate
    private static final int TOTAL_SEQUENCES = 10000;
    // length of each sequence
    private static final int SEQ_LENGTH = 10;
    // all the characters the sequence is drawing from
    private static final String SOURCE = "ATGC";
    // list of number of thread we want to try to run
    private static final int[] THREAD_COUNTS = {5,10,20,50,100};
    // number of runs we are taking average of to get the performance/runtime
    private static final int RUNCOUNT = 100;
    // calling or not calling the println funciton for each sequence generated
    // might want to set it to false when generating a lot of sequences
    private static final boolean VERBOSE = false;
    public static void main(String[] args) {    	
        // Trying different number of threads, see the performance, and each number of thread is run a number times
    	// taking the ave of the runs as the result for each thread numbers
    	System.out.println("Running Single thread");
    	long singlesRuntime = 0;
    	for (int i =0;i<RUNCOUNT;i++) {
    		singlesRuntime += runSingleThread()/RUNCOUNT;
    	}
    	// for each numer of threads, create threads and records runtime
    	long[] multiThreadingRuntime = new long[THREAD_COUNTS.length];
    	for (int i = 0;i<THREAD_COUNTS.length;i++) {
    		long currThreadsRuntime = 0;
    		for (int j=0;j<RUNCOUNT;j++) {
    			currThreadsRuntime += runMultipleThreads(THREAD_COUNTS[i])/RUNCOUNT;
    		}
    		multiThreadingRuntime[i] = currThreadsRuntime;
    	}
    	// printing out conclusions
    	System.out.println("Runtime for single thread: "+String.valueOf(singlesRuntime));
    	for (int i=0;i<THREAD_COUNTS.length;i++) {
    		System.out.println("Runtime for "+String.valueOf(THREAD_COUNTS[i])+" threads: "+String.valueOf(multiThreadingRuntime[i]));
    	}
    	
    }
    // function to handle running multi-threads, returns the runtime
    public static long runMultipleThreads(int threadCount) {
    	System.out.println("Starting running multi threading with: "+String.valueOf(threadCount)+" threads");
    	runtime = System.nanoTime();
        int sequencesPerThread = TOTAL_SEQUENCES/threadCount;
        //GenomeThread[] threads = new GenomeThread[threadCount];
        for (int i=0;i<threadCount;i++) {
        	//System.out.println(String.valueOf(i));
        	GenomeThread currThread = new GenomeThread((char) i, SEQ_LENGTH, SOURCE,sequencesPerThread, VERBOSE);
        	currThread.run();
        }
        return System.nanoTime()-runtime;
    }
    // function to handle running just 1 thread, returns runtime
    public static long runSingleThread() {
        GenomeGenerator generator = new GenomeGenerator(SEQ_LENGTH, TOTAL_SEQUENCES, SOURCE, VERBOSE);
        runtime = System.nanoTime();
        generator.runGenomeGenerator();
        return System.nanoTime()-runtime;
    }
}
