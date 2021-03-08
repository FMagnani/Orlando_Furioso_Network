#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:07:50 2021

@author: FMagnani
GitHub repo: https://github.com/FMagnani
"""

import sys
import pandas as pd



### Clean data from the notes at top and bottom of the page. ###
with open("Orlando_Furioso.txt", "r") as file:
    with open("Orlando_Furioso_text.txt", "w") as output:
        
        length = 0
        
        for line in file:
            if not (("Letteratura italiana" in line) | 
                    ("Ludovico Ariosto" in line)):
                output.write(line)
                length += 1
            


### Create dictionary with segmentation by chapters ###

chapters_dict = {}

with open("Orlando_Furioso_text.txt") as file:
    
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



### Characters to track ###

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


### Count how many occurrences-per-chapter a character does have ###

Character_occurrences = { name:[] for name in Characters_to_track }

for name in Characters:
    
    for first, last in zip(chapters_df['first_line'], chapters_df['last_line']):
            
        count = 0
        for value in Characters[name]:
            
            if ( first <= value < last ):
                count += 1
            
        Character_occurrences[name].append(count)


### Save data to csv


data = pd.DataFrame(Character_occurrences, index=chapters_df.index)

data.to_csv("data.csv", index=True)












        

