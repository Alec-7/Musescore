# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 13:44:16 2022

@author: Alec-7

This program was designed as a component of Musescore_Part_Splitter

This program processes all uncompressed Musescore files (.mscx file extension) in the same directory as this program
Each line of the original .mscx file is copied into several arrays, which are used to write new .mscx files
Lines that store clef or pitch information are altered as needed for each transposition
This program assumes the original file is written in C treble clef

"""

import os
for dirFile in os.listdir():
    if dirFile.endswith('.mscx'):
        
        #Print name of the file being copied
        print(dirFile)
        
        fileLen=len(open(dirFile,'r',encoding='utf-8').readlines())
        
        #Store the data for each new .mscx file
        
        #alto clef
        alto=[None]*fileLen
        #alto clef, transposed down an octave
        alto8vb=[None]*fileLen
        #bass clef
        bass=[None]*fileLen
        #Bb treble clef
        Bb=[None]*fileLen
        #Eb treble clef
        Eb=[None]*fileLen
        #F treble clef
        F=[None]*fileLen
        
        #Open original file
        file=open(dirFile,'r',encoding='utf-8')
        
        lineNum=0
        offset=0
        noClefLine=True
        voiceIndex=0
        #Each line in the original file is transferred to the arrays
        for line in file:

            if '<voice>' in line:
                voiceIndex=lineNum  
            #The following sections change the clef
            if '<concertClefType>G</concertClefType>' in line:
                bass[lineNum+offset]=line[:line.index('>G<')]+'>F8va</concertClefType>'
                alto[lineNum+offset]=line[:line.index('>G<')]+'>C3</concertClefType>'
                alto8vb[lineNum+offset]=line[:line.index('>G<')]+'>C3</concertClefType>'
                noClefLine=False
                Bb[lineNum]=line
                Eb[lineNum]=line
                F[lineNum]=line           
            elif '<transposingClefType>G</transposingClefType>' in line:
                bass[lineNum+offset]=line[:line.index('>G<')]+'>F8va</transposingClefType>'
                alto[lineNum+offset]=line[:line.index('>G<')]+'>C3</transposingClefType>'
                alto8vb[lineNum+offset]=line[:line.index('>G<')]+'>C3</transposingClefType>'
                noClefLine=False
                Bb[lineNum]=line
                Eb[lineNum]=line
                F[lineNum]=line            
            elif '</voice>' in line and noClefLine:
                lineSpace=line[:line.index('<')]
                bass=bass[:(voiceIndex+1)]+[lineSpace+'<Clef>',lineSpace+'  <concertClefType>F8va</concertClefType>',lineSpace+'  <transposingClefType>F8va</transposingClefType>',lineSpace +'  </Clef>']+bass[voiceIndex+1:]
                alto=alto[:(voiceIndex+1)]+[lineSpace+'<Clef>',lineSpace+'  <concertClefType>C3</concertClefType>',lineSpace+'  <transposingClefType>C3</transposingClefType>',lineSpace+'  </Clef>']+alto[voiceIndex+1:]
                alto8vb=alto8vb[:(voiceIndex+1)]+[lineSpace+'<Clef>',lineSpace+'  <concertClefType>C3</concertClefType>',lineSpace+'  <transposingClefType>C3</transposingClefType>',lineSpace+'  </Clef>']+alto8vb[voiceIndex+1:]
                offset=4
                bass[lineNum+offset]=line
                alto[lineNum+offset]=line
                alto8vb[lineNum+offset]=line
                noClefLine=False
                Bb[lineNum]=line
                Eb[lineNum]=line
                F[lineNum]=line
            
            #The following sections adjust the pitch for each transposition
            elif '<pitch>' in line:
                alto8vb[lineNum+offset]=line[:line.index('<pitch>')+7]+str(int(line[(line.index('<pitch>')+7):line.index('</pitch>')])-12)+line[line.index('</pitch>'):]
                bass[lineNum+offset]=line
                alto[lineNum+offset]=line
                Bb[lineNum]=line[:line.index('<pitch>')+7]+str(int(line[(line.index('<pitch>')+7):line.index('</pitch>')])+2)+line[line.index('</pitch>'):]
                Eb[lineNum]=line[:line.index('<pitch>')+7]+str(int(line[(line.index('<pitch>')+7):line.index('</pitch>')])-3)+line[line.index('</pitch>'):]
                F[lineNum]=line[:line.index('<pitch>')+7]+str(int(line[(line.index('<pitch>')+7):line.index('</pitch>')])-5)+line[line.index('</pitch>'):]
            
            elif '<tpc>' in line:
                bass[lineNum+offset]=line
                alto[lineNum+offset]=line
                alto8vb[lineNum+offset]=line
                Bb[lineNum]=line[:line.index('<tpc>')+5]+str(int(line[(line.index('<tpc>')+5):line.index('</tpc>')])+2)+line[line.index('</tpc>'):]
                Eb[lineNum]=line[:line.index('<tpc>')+5]+str(int(line[(line.index('<tpc>')+5):line.index('</tpc>')])-3)+line[line.index('</tpc>'):] 
                F[lineNum]=line[:line.index('<tpc>')+5]+str(int(line[(line.index('<tpc>')+5):line.index('</tpc>')])-5)+line[line.index('</tpc>'):]                                    
            
            #This section shifts the key signature 
            elif '<accidental>' in line:
                bass[lineNum+offset]=line
                alto[lineNum+offset]=line
                alto8vb[lineNum+offset]=line
                Bb[lineNum]=line[:line.index('<accidental>')+12]+str(int(line[(line.index('<accidental>')+12):line.index('</accidental>')])+2)+line[line.index('</accidental>'):] 
                Eb[lineNum]=line[:line.index('<accidental>')+12]+str(int(line[(line.index('<accidental>')+12):line.index('</accidental>')])-3)+line[line.index('</accidental>'):] 
                F[lineNum]=line[:line.index('<accidental>')+12]+str(int(line[(line.index('<accidental>')+12):line.index('</accidental>')])-5)+line[line.index('</accidental>'):]         
            
            #All other lines are unchanged from the original file
            else:
                bass[lineNum+offset]=line
                alto[lineNum+offset]=line
                alto8vb[lineNum+offset]=line
                Bb[lineNum]=line
                Eb[lineNum]=line
                F[lineNum]=line
            lineNum+=1
        
        #Write a new .mscx file for each transposition
        newFile=open(dirFile[:-5]+'_BassClef.mscx','w',encoding='utf-8')
        for newLine in bass:  
            newFile.write(newLine)
        newFile.close()
        
        newFile=open(dirFile[:-5]+'_AltoClef.mscx','w',encoding='utf-8')
        for newLine in alto:  
            newFile.write(newLine)
        newFile.close()
        
        newFile=open(dirFile[:-5]+'_AltoClef8vb.mscx','w',encoding='utf-8')
        for newLine in alto8vb:  
            newFile.write(newLine)
        newFile.close()
        
        newFile=open(dirFile[:-5]+'_Bb.mscx','w',encoding='utf-8')
        for newLine in Bb:  
            newFile.write(newLine)
        newFile.close()
        
        newFile=open(dirFile[:-5]+'_Eb.mscx','w',encoding='utf-8')
        for newLine in Eb:  
            newFile.write(newLine)
        newFile.close()
        
        newFile=open(dirFile[:-5]+'_F.mscx','w',encoding='utf-8')
        for newLine in F:  
            newFile.write(newLine)
        newFile.close()