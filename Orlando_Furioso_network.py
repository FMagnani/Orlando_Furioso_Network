#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 14:54:15 2021

@author: FMagnani
GitHub repo: https://github.com/FMagnani
"""

import pandas as pd
import networkx as nx

#%%

### Import data ###

data = pd.read_csv("Characters_per_chapter.csv", index_col=0)

# Factions (as they are at the beginning)

Christians = [
    'Aquilant',
    'Astolf',
    'Bradamant',
    'Brandimart',
    'Grifon',
    'Olivier',
    'Orland',
    'Rinald',
    'Zerbin'
    ]

Muslims = [
    'Agramant', 
    'Angelic',
    'Dudon', 
    'Ferra', 
    'Gradass', 
    'Mandricard', 
    'Marfis', 
    'Rodomont', 
    'Ruggier', 
    'Sacripant',
    'Sobrin'
    ]

Chants = [
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',
    'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX',
    'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL',
    'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI'
    ]

data['Chants'] = Chants
data = data.set_index('Chants')

#%%

G = nx.Graph()

### Layers (nodes)

layers = [Christians, data.index.values, Muslims]
colors = ['darkblue', 'black', 'darkred']

for i in range(3):
    G.add_nodes_from(layers[i], node_color=colors[i], layer=i)
    
pos = nx.multipartite_layout(G, subset_key='layer', align='vertical')

for i in range(3):
    nx.draw_networkx_nodes(G, pos, nodelist=layers[i],
                           node_color=colors[i], node_size=20)


### Edges

for name in Christians:
    for chant in data.index.values:
        w = data[name][chant]
        if (w > 10):
            G.add_edge(name, chant, weight=w)

for name in Muslims:
    for chant in data.index.values:
        w = data[name][chant]
        if (w > 10):
            G.add_edge(name, chant, weight=w)


weights = [0.05*G[u][v]['weight'] for u,v in G.edges]

edges_blue = []
edges_red = []

for edge in G.edges:
    if ((str(edge[0]) in Christians) | (str(edge[1]) in Christians)):
             edges_blue.append(edge)
    else:
        edges_red.append(edge)


nx.draw_networkx_edges(G, pos, width=weights, alpha=.9, 
                       edgelist=edges_red, edge_color='red')            

nx.draw_networkx_edges(G, pos, width=weights, alpha=.9, 
                       edgelist=edges_blue, edge_color='blue')            


### Labels












