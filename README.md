# sentece-simplification
# Note about iSimp

This script needs iSimp for simplificable constructs' identification. You can find information about iSimp here: http://research.bioinformatics.udel.edu/isimp/. We used a version provided by Yifan Peng.

iSimp needs to be stored in the same path the main shell script is. 

# RUN

This is a linux shell script that can be run with the following command:

```./main_shell_script```

# INPUT

The script expects tokenized text with one sentence per line, in files ```*.txt``` stored in ```10pack_sentences```
The script will analize all files with a shared keyword, specified in ```BATCH_KEYWORD```in ```main_shell_script```

# OUTPUT 

Simplified sentences will be stores one sentence per file under ```algorithm_sentences```
