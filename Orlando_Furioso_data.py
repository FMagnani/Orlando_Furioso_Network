#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:07:50 2021

@author: FMagnani
GitHub repo: https://github.com/FMagnani
"""

import pandas as pd


### Clean data from the notes at top and bottom of the pages. ###
with open("Orlando_Furioso.txt", "r") as file:
    with open("Orlando_Furioso_clean.txt", "w") as output:
        
        length = 0
        
        for line in file:
            if not (("Letteratura italiana" in line) | 
                    ("Ludovico Ariosto" in line)):
                output.write(line)
                length += 1
            


### Create dictionary with segmentation by chapters ###

chapters_dict = {}

with open("Orlando_Furioso_clean.txt") as file:
    
    for num, line in enumerate(file, 1):
        if ( ("CANTO" in line.upper()) & (len(line.split())==2) ):
        
            name_chapter = "Canto " + line.split()[1]
            name_chapter = name_chapter.title()
            chapters_dict.update( {name_chapter:num} )


### Create DataFrame from dictionary ###
        
chapters_df = pd.DataFrame(chapters_dict.values(), index=chapters_dict.keys())

chapters_df.columns = ['first_line']

last_line = list(chapters_df['first_line'][1:])
last_line.append(length)

chapters_df['last_line'] = last_line



# Characters to track

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

### Find all occurrences of these names in the file and the lines in which they appear ###

# tot_occurrencies is a dict with keys = characters' names, 
# values = list of the lines in which they appear

tot_occurrences = { name:[] for name in Characters_to_track }

with open("Orlando_Furioso_clean.txt") as file:
    
    for num, line in enumerate(file, 1):
        for name in tot_occurrences.keys():
            if (name in line):
                
                tot_occurrences[name].append(num)


### Count how many occurrences-per-chapter a character does have ###

chapter_occurrences = { name:[] for name in Characters_to_track }

for name in tot_occurrences:
    
    for first, last in zip(chapters_df['first_line'], chapters_df['last_line']):
            
        count = 0
        for value in tot_occurrences[name]:
            
            if ( value in range(first, last) ):
                count += 1
            
        chapter_occurrences[name].append(count)


### Save data to csv


data = pd.DataFrame(chapter_occurrences, index=chapters_df.index)

data.to_csv("data.csv", index=True)












        

