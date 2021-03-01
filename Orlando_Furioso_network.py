#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:07:50 2021

@author: FMagnani
GitHub repo: https://github.com/FMagnani
"""

import sys
import pandas as pd

#%%

### Clean data from the notes at top and bottom of the page. ###
with open("Orlando_Furioso.txt", "r") as file:
    with open("Orlando_Furioso_text.txt", "w") as output:
        
        for line in file:
            if not (("Letteratura italiana" in line) | 
                    ("Ludovico Ariosto" in line)):
                output.write(line)
            
#%%

### Create dictionary with segmentation by chapter (Canto) ###

Canti_segmentation = {}

with open("Orlando_Furioso_text.txt") as file:
    
    for num, line in enumerate(file, 1):
        if ( ("CANTO" in line.upper()) & (len(line.split())==2) ):
            
            nome_canto = "CANTO " + line.split()[1]
            Canti_segmentation.update( {nome_canto:num} )

#%%

### Characters to track ###
# Without the last letter: Ariosto often names them in such a way

Characters_to_track = [
    'Agramant',
    'Angelic',
    'Aquilant',
    'Astolf',
    'Bradamant',
    'Brandimart',
    'Dudon',
    'Ferra',
    'Gradass',
    'Grifon',
    'Mandricard',
    'Marfis',
    'Olivier',
    'Orland',
    'Rinald',
    'Rodomont',
    'Ruggier',
    'Sacripant',
    'Sobrin',
    'Zerbin',
    ]

# Initialize a dictionary of empty lists.
# Keys are the name of the characters, values are the list of the lines in
# which that name is found.

Characters = { name:[] for name in Characters_to_track }

with open("Orlando_Furioso_text.txt") as file:
    
    for num, line in enumerate(file, 1):
        for name in Characters.keys():
            if (name in line):
                
                Characters[name].append(num)


















        

