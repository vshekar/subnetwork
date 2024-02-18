#%%
from networkx import DiGraph
from networkx.algorithms.simple_paths import all_simple_paths
from networkx.algorithms.shortest_paths import has_path
from max_lambda2 import Graph
import xml.etree.ElementTree as ET
from tqdm import trange, tqdm
import sumolib
import json
import operator

#%%
tree = ET.parse('../scenario/lust.net.xml')
root = tree.getroot()
network_rep = Graph()
for edge in root.findall("edge"):
    if 'from' in edge.attrib:
        network_rep.addEdge(edge.attrib['from'], edge.attrib['to'],edge.attrib['id'])

min_subnet = {}
max_lmbd = 0
net = sumolib.net.readNet('../scenario/lust.net.xml')
vulnerable_edges = [e for e in net.getEdges() if e.getLaneNumber()>2]

for disrupted_edge in tqdm(vulnerable_edges):
    disrupted_edge = disrupted_edge.getID()
    loop = trange(1,62, leave=False)
    for lmbd in loop:
        loop.set_description(f"Edge: {disrupted_edge}  lambda:{lmbd}")
        loop.refresh()
        subnetwork_edges = network_rep.getSubnet(disrupted_edge, lmbd)

        G = DiGraph()
        for edge in subnetwork_edges:
            if disrupted_edge != edge:
                G.add_edge(*network_rep.nodes[edge])
        source, dest = network_rep.nodes[disrupted_edge]
        #if len(list(all_simple_paths(G, source, dest))) > 0:
        try:
            if has_path(G, source=source, target=dest):
                min_subnet[disrupted_edge] = lmbd 
                if lmbd > max_lmbd:
                    max_lmbd = lmbd
                break
            
        except:
            pass

print(max_lmbd)
json.dump(min_subnet, open('min_subnet.json', 'w'))
#%%

lmbds = json.load(open('lambdas.json'))
min(lmbds.items(), key=operator.itemgetter(1))
# %%
lmbd_values = list(lmbds.values())
sum(lmbd_values)/len(lmbd_values)
# %%
min_subnet = json.load(open('min_subnet.json'))
print(len(min_subnet))
net = sumolib.net.readNet('../scenario/lust.net.xml')
vulnerable_edges = [e for e in net.getEdges() if e.getLaneNumber()>2]
print(len(vulnerable_edges))
# %%
