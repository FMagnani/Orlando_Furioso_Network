#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 14:54:15 2021

@author: FMagnani
GitHub repo: https://github.com/FMagnani
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import argparse 
from networkx.algorithms import bipartite as bp


### Argument parser ###

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--threshold", 
                    help="the minimum citation per chant needed to realize a link", 
                    type=int, default=0)
args = parser.parse_args();

#citation_threshold = args.threshold
citation_threshold = 0

### Import data ###

data = pd.read_csv("data.csv", index_col=0)



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

Saracens = [
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


# Change of the index

Chants = [
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',
    'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX',
    'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL',
    'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI'
    ]

data['Chants'] = Chants
data = data.set_index('Chants')



#
##
### Bipartite Graph ###
##
#

G = nx.Graph()


### Layers (nodes) ###

layers = [Christians, Chants, Saracens]
labels = ['Christians', 'Chants', 'Muslims']
colors = ['darkblue', 'black', 'darkred']

# Adding nodes in groups. Each group shares the 'layer' variable used by the layout function.

for i in range(3):
    G.add_nodes_from(layers[i], layer=i)
    

### Edges ###

# Creating weighted edges

for name in Christians:
    for chant in data.index.values:
        occurrences = data[name][chant]
        if (occurrences > citation_threshold):
            G.add_edge(name, chant, weight=occurrences)

for name in Saracens:
    for chant in data.index.values:
        occurrences = data[name][chant]
        if (occurrences > citation_threshold):
            G.add_edge(name, chant, weight=occurrences)


# Creating two class of edges, based on the faction to which the node belongs.

edges_blue = []
edges_red = []

for edge in G.edges:
    if ((str(edge[0]) in Christians) | (str(edge[1]) in Christians)):
             edges_blue.append(edge)
    else:
        edges_red.append(edge)


#
##
### Projected graphs 
##
#

characters = [ *Christians, *Saracens ]

G_char = bp.weighted_projected_graph(G, characters)







#
##
### Drawing
##
#

# General

fig, ax = plt.subplots(nrows=1, ncols=2)

### G - Bipartite Graph ###

pos = nx.multipartite_layout(G, subset_key='layer', align='vertical')

# Drawing nodes in groups, specifying colors and label (used by the legend).

for i in range(3):
    nx.draw_networkx_nodes(G, pos, nodelist=layers[i],
                            node_color=colors[i], node_size=20,
                            label=labels[i], ax=ax[0])


# Drawing edges. Width proportional to the weight. Divided in two groups with different colors.

width = [0.05*G[u][v]['weight'] for u,v in G.edges]

nx.draw_networkx_edges(G, pos, width=width, alpha=.9, 
                        edgelist=edges_red, edge_color='red', ax=ax[0])            

nx.draw_networkx_edges(G, pos, width=width, alpha=.9, 
                        edgelist=edges_blue, edge_color='blue', ax=ax[0])            


### Legend and title

# ax[0].legend(scatterpoints = 1, loc=1)
# ax[0].title("Citation threshold: "+str(citation_threshold))
#plt.show()


### Labels - optional ###
# Bad visualization but useful for debugging

# labels = {}
# for i in G.nodes:
#     labels[i] = str(i)

# nx.draw_networkx_labels(G, pos, labels, font_size=10)



### G_char - Projected Graph ###

char_edges_blue = []
char_edges_red = []
char_edges_black = []

for edge in G_char.edges:
    if ((str(edge[0]) in Christians) & (str(edge[1]) in Christians)):
        char_edges_blue.append(edge)
    if ((str(edge[0]) in Saracens) & (str(edge[1]) in Saracens)):
        char_edges_red.append(edge)
    else:
        char_edges_black.append(edge)

pos = nx.circular_layout(G_char)

width = [0.1*G_char[u][v]['weight'] for u,v in G_char.edges]

nx.draw_networkx_nodes(G_char, pos, nodelist=Christians,
                            node_color='darkblue', node_size=50, ax=ax[1])

nx.draw_networkx_nodes(G_char, pos, nodelist=Saracens,
                            node_color='darkred', node_size=50, ax=ax[1])

nx.draw_networkx_edges(G_char, pos, width=width, alpha=.8, 
                       edgelist=char_edges_red, edge_color='red', ax=ax[1])            

nx.draw_networkx_edges(G_char, pos, width=width, alpha=.8, 
                       edgelist=char_edges_blue, edge_color='blue', ax=ax[1])    

nx.draw_networkx_edges(G_char, pos, width=width, alpha=.9, 
                       edgelist=char_edges_black, edge_color='black', ax=ax[1])    




