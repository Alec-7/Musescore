Version Completed 10/29/22

Dependancies: MuseScore 3, Python 3

These programs takes a Musescore file written in C treble clef, creates seperate parts, and transposes each part into every commonly used key (Bb, Eb, F treble clef) and clef (C alto clef, bass clef). Chords in the original part are broken up across parts, so that each part has a single note. Enough parts are created so that each note of each chord is in a part.

Setup: Download all files in this repository. Move all files into a folder labeled Musescore_Part_Splitter. Within Musescore_Part_Splitter, move all .sh files, MuseScore_Part_Splitter.py, and MuseScore_Transpose.py into a folder labeled Programs. 

Running:

Input: Any number of Musescore (.mscz) files

How to run this program:
1. Move all of the .mscz files you want to process into the same directory as the "Musescore_Part_Splitter" folder.
2. Go into the "Musescore_Part_Splitter" folder, and double click the appropiate PartSplitter_Runner.py file. Choose the file that matches the version of MuseScore you installed, which largely depends on your operating system.
3. If needed, make any edits needed to the individual parts in the "mscz_Files" folder. Then, run the appropiate RedoPDFs file to automatically generate new .pdf files

Note: This program should work with Musescore 4, but this is currently untested.
