#!/bin/bash
cd ../mscz_Files
mkdir ../PDF_Files_Redo
for file in ./*.mscz 
do 
	echo $file
	noX=$(echo $file | cut -c 3- | rev | cut -c 6- | rev)
	mscore-portable -o "../PDF_Files_Redo/${noX}.pdf" $file
done
for file in ./*
do
	if [ -d $file ]
	then
		cd $file
		echo $file
		mkdir "../../PDF_Files_Redo/${file}"
		for subFile in ./*.mscz
		do
			noX=$(echo $subFile | cut -c 3- | rev | cut -c 6- | rev)
			mscore-portable -o "../../PDF_Files_Redo/${file}/${noX}.pdf" $subFile
		done
	cd ..
	fi
done
cd ../Musescore_Part_Splitter