# GenomeSequence Generator
## Overview
 This project is for HW4
 THe aim is to test the performace of single thread and multithreading when it comes to string generatation

 Classes:
 Main:
 You can change the constants at the beginning of the file to try different combination to see the performances
 This class handles the execution of the code
 It also handles creating each thread
 Performance is handled with system's nanoTime()

 GenomeThread:
 Impleaments 'Runnable' interface. 
 Generate the sequence as requested

 GenomeGenerator:
 Simple single thread generator for the sequence