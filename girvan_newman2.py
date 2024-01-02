import time
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
from networkx.drawing.nx_agraph import graphviz_layout


node_limit = 10000
louvain_community_count = 46
#########################################
## CREATE GRAPH ##
#########################################
# Read cities' names from files
cities = []
with open("subelj_euroroad/ent.subelj_euroroad_euroroad.city.name", "r") as f:
    cities = f.read().splitlines()
print("Number of origin nodes in the network:", len(cities))

cities = cities[:node_limit]
print("Number of nodes in the network:", len(cities))
print("First 5 nodes\n", cities[:5])

# Read edges from files and apply "name" for them
edges = []

with open("subelj_euroroad/out.subelj_euroroad_euroroad", "r") as f:
    for edge in f:
        if edge.startswith('%'):
            continue
        edge = edge.rstrip().split(' ')
        if (int(edge[0]) < node_limit and int(edge[1]) < node_limit):
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
comp = community.girvan_newman(G)

partition = []
ahead_partitions = list(next(comp))  # first commutities
for c in next(comp):
    ahead_partitions = list(next(comp))
    if len(ahead_partitions) > louvain_community_count:
        break
    partition = ahead_partitions

run_time = time.time() - start

print("\nThe Girvan-Newman algorithm finished in {}s".format(run_time))
print("The number of group in the network is: ", len(partition))

# Calculate modularity of partition
mod = community.modularity(G, partition)
print("Modularity of all partitions detected is", mod)

# Calculate coverage and performance of partition
(cov, perf) = community.partition_quality(G, partition)
print("Coverage of all partitions detected is", cov)
print("Performance of all partitions detected is", perf)

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

fig = plt.figure(figsize=(16, 10))

pos = graphviz_layout(G)

im = nx.draw_networkx_nodes(G, pos, node_size=30,
                            node_color=color_list_community, cmap='jet', vmin=0,
                            vmax=len(partition))
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=3, font_color="black")

plt.xticks([])
plt.yticks([])
plt.colorbar(im)
plt.show(block=True)
