# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 15:31:54 2022

@author: Alec-7

This program was designed as a component of Musescore_Part_Splitter

This program processes all uncompressed Musescore files (.mscx file extension) in the same directory as this program
This program creates multiple parts from an original score with chords, so that each part has only one note of each chord
The number of parts is equal to the size of the biggest chord, so that every note of the original chord is covered
For smaller chords, multiple parts are assigned the same note

This program is fairly computationally intensive, and multiple opportunities exist to improve effeciency
-
"""
makeNewDir=True

import os
for dirFile in os.listdir():
    if dirFile.endswith('.mscx'):
        
        file=open(dirFile,'r',encoding='utf-8')
        
        #Print name of the file being copied
        print(dirFile)
        
        #Find number of lines and biggest chord in the original file
        fileLen=0
        numParts=1
        numChords=0
        notesInChord=0
        for line in file:
            #Find beginnning of chord
            if '<Chord>' in line:
                #Store number of notes in the chord
                notesInChord=0
                numChords+=1
            #Find each note in the chord
            elif '<Note>' in line:
                notesInChord+=1
            #Find end of chord
            elif '</Chord>' in line:
                #Checks if this is the biggest chord so far
                if notesInChord>numParts:
                    numParts=notesInChord
            fileLen+=1
        
        #If there are no chords, then new parts are not needed
        if numParts>1:
            
            #Create new folder for parts
            if makeNewDir:
                folderName=dirFile[:-5]
                underscoreVar=1
                if os.path.exists(folderName):
                    while os.path.exists(folderName+'_'+str(underscoreVar)):
                        underscoreVar+=1
                    os.mkdir(folderName+'_'+str(underscoreVar))
                    os.chdir(folderName+'_'+str(underscoreVar))
                else:
                    os.mkdir(folderName)
                    os.chdir(folderName)
                
            #Holds each part
            allParts=[[None]*fileLen for h in range(numParts)]
            
            #Holds all chords
            allChords= [[[ [] for _ in range(100)] for _ in range(numParts)] for _ in range(numChords)]
    
            #Tracks which part is being edited
            partTracker=0
            
            #Tracks whether a note is being added
            inNote=False
            
            #Tracks the location of line in the original file
            lineCount=0        
            
            #Tracks which line of the note is being used
            noteLine=0
            
            #Tracks which chord is being broken up
            chordNumber=-1
            
            file=open('../'+dirFile,'r',encoding='utf-8')
            
            for line in file:
                #Start of chord
                if '<Chord>' in line:
                    partTracker=0
                    chordNumber+=1
                #Start of note
                elif '<Note>' in line:
                   inNote=True
                   noteLine=0
                if inNote:
                    #For each part, fill in the sections where the note would be with None
                    for partNum in range(len(allParts)):
                        allParts[partNum][lineCount]=None
                    #Store data for each note, with each note going to a different part.
                    allChords[chordNumber][partTracker][noteLine]=line
                    noteLine+=1
                else:
                    for partNum in range(len(allParts)):
                        allParts[partNum][lineCount]=line
                if '</Note>' in line:
                    inNote=False
                    allChords[chordNumber][partTracker]=allChords[chordNumber][partTracker][:noteLine]
                    partTracker+=1
                lineCount=lineCount+1
            
            #Sort each note in each chord by the part that will get that note
            #TEMPORARY FIX: 1 and 2 correct, 3 and 4 hard coded (potentially changed by Ejay), 5+ based on formula (placeholder before Ejay decides) 
            
            for chords in range(len(allChords)):
                numNotes=numParts
                for chordPart in range(1,len(allChords[chords])):
                    if allChords[chords][chordPart]==[[] for _ in range(100)]:
                        numNotes+=-1
                if numNotes<numParts:                   
                    if numNotes==1:
                        for chordP in range(1,len(allChords[chords])):
                            allChords[chords][chordP]=allChords[chords][0].copy()
                    
                    elif numParts==3:
                        #Part distribution: 1 1 2
                        allChords[chords][2]=allChords[chords][1].copy()
                        allChords[chords][1]=allChords[chords][0].copy()
                    
                    elif numParts==4:
                        if numNotes==3:
                            allChords[chords][3]=allChords[chords][2].copy()
                            allChords[chords][2]=allChords[chords][1].copy()
                            allChords[chords][1]=allChords[chords][0].copy()
                        else:
                            allChords[chords][2]=allChords[chords][0].copy()
                            allChords[chords][3]=allChords[chords][1].copy()
                    else:
                        newChord=[None]*numParts
                        for aPart in range(numParts):
                            newChord[aPart]=allChords[chords][(10-aPart)%numNotes].copy()
                        allChords[chords]=newChord
                    
            
            
            chordToInsert=0
            inInsert=False
            linesBeforeInsert=0
            inChord=False
            #Insert each note into the part
            for lin in range(len(allParts[0])):
                if allParts[0][lin] is None:
                    inChord=True
                    for partNum in range(len(allParts)):
                        if linesBeforeInsert<len(allChords[chordToInsert][partNum]):
                            allParts[partNum][lin]=allChords[chordToInsert][partNum][linesBeforeInsert]
                    linesBeforeInsert+=1
                else:
                    linesBeforeInsert=0
                    if inChord:
                        chordToInsert+=1
                        inChord=False
            #Remove Nones
            for partN in range(len(allParts)):
                for lin in range(len(allParts[partN])):
                    if lin<len(allParts[partN]):
                        while allParts[partN][lin] is None:
                            allParts[partN]=allParts[partN][:lin]+allParts[partN][lin+1:]
                                
            #Write new .mscx files
            for f in range(len(allParts)):
                newFile=open(dirFile[:-5]+'_Part'+str(len(allParts)-f)+'.mscx','w',encoding='utf-8')
                for newLine in allParts[f]:  
                    newFile.write(newLine)
                newFile.close()
            file.close()
            if makeNewDir:
                os.rename('../'+dirFile, dirFile)
                os.chdir('..')
        else:
            print('Only one part')
        
try:
    file.close()
except:
    pass
            
        
            
        