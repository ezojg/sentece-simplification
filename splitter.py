import fileinput
import re
import sys

if ( len( sys.argv ) < 3 ):
    sys.stderr.write( "E: usage: " +sys.argv[0] + " <input_file> <output_file> \n" )
    sys.stderr.flush();

    exit( 2 );
else:
    print("Ok.")

#LEER ARCHIVO
text_file = open( sys.argv[1], "r" )
dato = text_file.read().splitlines()
text_file.close()

#QUITA EXTENSION DE NOMBRE DE ARCHIVO
split_line = sys.argv[2]
split_line = split_line[:-8]
line_name=""

#ESCRIBIR lineas individuales en cada archivo
indice=1
for line in dato:
    line_name = split_line + "_" + str(indice) + ".spt.txt"
 #   line_name = re.sub('\.san', '.spt.txt' , line.rstrip())
    save_file = open( line_name , "w" )
    save_file.write(line)
    save_file.close()
    indice=indice+1

