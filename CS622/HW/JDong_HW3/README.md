# INDIEGOGO FILE MERGER AND SEARCHER
## Overview
 This project build on the HW2
 Minor modifications were made to the HW2:
 1. Using GUI to handle the search
 2. Search now takes in a 'categories' list of strings, instead of searching the entire string
 3. more printlines for errors
 
 Additions for HW3:
 
 UserGUI:
    Simple terminal GUI that handles the functionalities of this homework
    Automatically merges files
 SearchHistory:
    Class that stores frequency and timestamps for each search. Each Keyword should have a corresponding SearchHistory
 HistoryHandler:
    Stores a hasmap of each keyword and its corresponding SearchHistory.
    Provides functions that returns frequency and timestamps for all keywords or a certain keyword
