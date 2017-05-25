#!/bin/bash
#El script está en carpeta superior que los archivos de texto
SCRIPT_PATH=/home/elwe/Documents/Pipeline_iSimp
#Define aquí la palabra clave del grupo de oraciones a simplificar.
BATCH_KEYWORD=ejemplo

cd $SCRIPT_PATH


#clearfile
#ELIMINAR FORMATO DE ARTÍCULO CON "SANITIZADOR"
echo "Sanitizing text for $BATCH_KEYWORD batch..."
rm ./sanitized_sentences/*
cd ./10pack_sentences
for i in $(\ls $BATCH_KEYWORD*)
do
	echo $i
	python2 $SCRIPT_PATH/regex.py $SCRIPT_PATH/10pack_sentences/$i $SCRIPT_PATH/sanitized_sentences/$i
done
cd $SCRIPT_PATH



#SEPARA EN ORACIONES INDIVIDUALES
echo "Splitting..."
rm ./split_sentences/*
cd ./sanitized_sentences
for l in $(\ls $BATCH_KEYWORD*)
do
	echo $l
	python2 $SCRIPT_PATH/splitter.py $SCRIPT_PATH/sanitized_sentences/$l $SCRIPT_PATH/split_sentences/$l	
done
cd $SCRIPT_PATH



#ANALIZAR EN ISIMP
echo "Analysing in iSimp..."
rm ./iSimp_sentences/*
cd ./split_sentences
for j in $(\ls $BATCH_KEYWORD*)
do
	echo $j
	$SCRIPT_PATH/isimp_v2/simplify.sh $SCRIPT_PATH/split_sentences/$j $SCRIPT_PATH/iSimp_sentences/$j	
done
cd $SCRIPT_PATH



#ALIMENTAR A ALGORITMO #dará error a menos que se le dé de a una oración
echo "Analysing in Algorithm..."
cd ./iSimp_sentences
for k in $(\ls $BATCH_KEYWORD*)
do
	echo $k
	python2 $SCRIPT_PATH/simplifier.py $SCRIPT_PATH/iSimp_sentences/$k $SCRIPT_PATH/algorithm_sentences/$k
#el programa de josé suelta las oraciones en el mismo directorio, hacer que las lleve a ./algorithm_sentences
done
cd $SCRIPT_PATH

