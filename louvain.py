import numpy as np
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
# from scipy.cluster.hierarchy import dendrogram
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community import louvain_communities
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz
from sklearn import metrics
from functools import reduce
# from scipy.cluster import hierarchy

#########################################
## CREATE GRAPH ##
#########################################
# Read cities' names from files
cities = []
with open("subelj_euroroad/ent.subelj_euroroad_euroroad.city.name", "r") as f:
    cities = f.read().splitlines()

print("Number of nodes in the network:", len(cities))
print("First 5 nodes\n", cities[:5])

# Read edges from files and apply "name" for them
edges = []

with open("subelj_euroroad/out.subelj_euroroad_euroroad", "r") as f:
    for edge in f:
        if edge.startswith('%'):
            continue
        edge = edge.rstrip().split(' ')
        edge = [cities[int(i)-1] for i in edge]
        edges.append(edge)

print("Number of edges in the network:", len(edges))
print("First 5 edges\n", edges[:5])

#########################################
## PROCESSING ##
#########################################

# Make Graph
G = nx.Graph()
G.add_edges_from(edges)

start = time.time()
partition = community.louvain_communities(G)
run_time = time.time() - start

print("\nThe Louvain algorithm finished in {}s".format(run_time))
print("The number of group in the network is: ", len(partition))
# print("All partitions detected: ")
# for p in partition:
#     print(p)

# Calculate modularity of partition
mod = community.modularity(G, partition)
print("Modularity of all partitions detected is", mod)

# Calculate coverage and performance of partition
(cov, perf) = community.partition_quality(G, partition)
print("Coverage of all partitions detected is", cov)
print("Performance of all partitions detected is", perf)

count = reduce(lambda x, y: x + len(y), partition, 0)
print("Number of city in communities", count)

duplicate = False
exist = dict()
for idx, p in enumerate(partition):
    for idx, city in enumerate(p):
        if city in exist:
            duplicate = True
            break
        else:
            exist[city] = True

print('duplicate' if duplicate else 'no duplicate')

#########################################
## DRAW GRAPH ##
#########################################
# Add color for the community
node_mapping = {}
map_v = 0
for node in G.nodes():
    node_mapping[node] = map_v
    map_v += 1

color_list_community = [[] for i in range(len(G.nodes()))]

for i in G.nodes():
    for j, p in enumerate(partition):
        if i in p:
            color_list_community[node_mapping[i]] = j

fig = plt.figure(figsize=(13, 7))

pos = graphviz_layout(G)
im = nx.draw_networkx_nodes(G, pos, node_size=30,  # len(G.nodes()),
                            node_color=color_list_community, cmap='jet', vmin=0,
                            vmax=len(partition))
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=3, font_color="black")

plt.xticks([])
plt.yticks([])
plt.colorbar(im)
# plt.show(block=True)
