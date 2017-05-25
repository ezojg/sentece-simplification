import fileinput
import re
import sys

if ( len( sys.argv ) < 3 ):
    sys.stderr.write( "E: usage: " +sys.argv[0] + " <input_file> <output_file> \n" )
    sys.stderr.flush();

    exit( 2 );
else:
    print("Ok.")

#LEER ARCHIVO INPUT
text_file = open( sys.argv[1], "r" )
dato = text_file.read().splitlines()
text_file.close()


#QUITA EXTENSION DE NOMBRE DE ARCHIVO
split_line = sys.argv[2]
split_line = split_line[:-4]
file_name=""
file_name = split_line + ".san.txt"
open( file_name , 'w').close()

#ESCRIBIR REGEX EN ARGV 2
for line in dato:
    line = re.sub('[\(][^\(|^\)]*\s[0-9]+\s[^\(|^\)]*[\)]', '', line.rstrip()) #elimina (_num_)
    line = re.sub('[\(][^\(|^\)]*\s[0-9]+\.[0-9]+\s[^\(|^\)]*[\)]', '', line.rstrip()) #elimina (_num.num_)
    line = re.sub('[\[][^\(|^\)]*\s[0-9]+\s[^\(|^\)]*[\]]', '', line.rstrip()) #elimina [_num_]
    line = re.sub('[\[][^\(|^\)]*\s[0-9]+\.[0-9]+\s[^\(|^\)]*[\]]', '', line.rstrip()) #elimina [_num.num_]
    line = re.sub('[\(][^\(|^\)]*\s(fig\s\.|figure|e\s\.\sg\s\.|table)\s[^\(|^\)]*[\)]', '', line.rstrip(), flags=re.I) #
    #print(line)


    save_file = open( file_name, "a" )
    save_file.write(line)
    save_file.write("\n")
    save_file.close()

