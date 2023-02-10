#!/bin/bash
mkdir ../mscz_Files
cd ../mscz_Files
echo "Converting mscz files to .mscx files"
for file in ../*.mscz 
do 
	echo $file
	noX=$(echo $file | cut -c 4- | rev | cut -c 6- | rev) 
	mscore -o "${noX}.mscx" $file
done
cp ../MuseScore_Part_Splitter/Programs/MuseScore_Part_Splitter.py MuseScore_Part_Splitter.py
echo "Seperating Parts"
python3 MuseScore_Part_Splitter.py
rm MuseScore_Part_Splitter.py
cp ../MuseScore_Part_Splitter/Programs/MuseScore_Transpose.py MuseScore_Transpose.py
python3 MuseScore_Transpose.py
rm MuseScore_Transpose.py
for file in ./*
do
	if [ -d $file ]
	then 
		cd $file 
		cp ../../MuseScore_Part_Splitter/Programs/MuseScore_Transpose.py MuseScore_Transpose.py
		python3 MuseScore_Transpose.py
		rm MuseScore_Transpose.py
		cd ..
	fi 
done
mkdir ../PDF_Files
echo "Exporting as .mscz and .pdf files"
for file in ./*.mscx
do 
	echo $file
	noX=$(echo $file | cut -c 3- | rev | cut -c 6- | rev)
	mscore -o "${noX}.mscz" $file
	mscore -o "../PDF_Files/${noX}.pdf" $file
	rm $file
done
for file in ./*
do
	if [ -d $file ]
	then 
		cd $file 
		mkdir "../../PDF_Files/${file}" 
		for subFile in ./*.mscx 
		do
			noX=$(echo $subFile | cut -c 3- | rev | cut -c 6- | rev)
			mscore -o "${noX}.mscz" $subFile
			mscore -o "../../PDF_Files/${file}/${noX}.pdf" $subFile
			rm $subFile
		done
		cd ..
	fi 
done
cd ../Musescore_Part_Splitter