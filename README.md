# sentece-simplification
# Note about iSimp

This script needs iSimp for simplificable constructs' identification. You can find information about iSimp here: http://research.bioinformatics.udel.edu/isimp/. We used a version provided by Yifan Peng.


# RUN

This is a linux shell script that can be run with the following command:

```./sentence-simplification-main.sh```

Please note that the script will expect iSimp to be stored in the same path ```sentence-simplification-main.sh``` is. 

# INPUT

The script expects tokenized text with one sentence per line, in files ```*.txt``` stored in ```10pack_sentences```.
The script will analize all files with a shared keyword, specified in ```BATCH_KEYWORD```in ```sentence-simplification-main.sh```.

# OUTPUT 

Simplified sentences will be stored one sentence per file under ```algorithm_sentences```.
