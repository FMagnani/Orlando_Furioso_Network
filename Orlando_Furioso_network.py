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


#%%

data.index = range(47)[1:]

G = nx.Graph()

G.add_nodes_from( data.index.values )
pos = nx.circular_layout(G)

for name in data.columns:

    selector = (data[name] != 0)

    values = data.loc[selector, name].index.values

    for i in range(len(values)-1):
        G.add_edge(values[i], values[i+1])
        
nx.draw_networkx_nodes(G, pos, node_size=30)
nx.draw_networkx_edges(G, pos)

labels = {}
for i in G.nodes:
    
    labels[i] = str(i)
    
nx.draw_networkx_labels(G, pos, labels, font_size=12)
















