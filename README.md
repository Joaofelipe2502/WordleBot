# WordleBot
Gets the "best guess" for the game wordle. Built in python & not optimized, it's slow, really slow, 1-2 minutes to calculate with just 60 words remaining slow.
WordleList.txt contains all valid guesses, while answer_list.txt contains all valid answers. Both files are necessary to run
Follow the instructions after running main.py, it should walk you through the options on how to use
This was made as a novelty for my use only, while I tried to make it usable, documentation and proper errors will be lacking

NOT the optimal aproach mathematically -
This minimizes the expected number of valid words remaining after a guess, it does NOT minimize number guesses, even if these 2 are correlated.

Given the slow speed of this tool I went ahead and calculated the first rounds ideal guess, and stored the information in the corresponding file.
This took over an hour on my computer, thats with all 2,000+ guesses remaining, the fewer guesses remaining the less time it will take to run. (Again not at all optimized)
