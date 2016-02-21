import json
import networkx as nx
import random
import heapq
import matplotlib.pyplot as plt
filename = r"C:\Users\manasa\Documents\Caltech\CS144\Pandemaniac\Pandemaniac\2.10.12.json"
out_file = "C:\Users\manasa\Documents\Caltech\CS144\Pandemaniac\Pandemaniac\output.txt"

data = {}
def bet_cen(num_seeds):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)
#    plt.figure(num=None, figsize=(20, 20), dpi=80)
#    plt.axis('off')
#    fig = plt.figure(1)
#    pos = nx.spring_layout(G)
#    nx.draw_networkx_nodes(G,pos)
#    nx.draw_networkx_edges(G,pos)
#    nx.draw_networkx_labels(G,pos)
#
#    cut = 1.00
#    xmax = cut * max(xx for xx, yy in pos.values())
#    ymax = cut * max(yy for xx, yy in pos.values())
#    plt.xlim(0, xmax)
#    plt.ylim(0, ymax)
#
#    plt.show(fig)
    connected_components = list(nx.connected_component_subgraphs(G))

    largest_component = connected_components[0]
    
    bet_cen = nx.betweenness_centrality(largest_component)
    max_nodes = heapq.nlargest(num_seeds, bet_cen, key = bet_cen.get)
    return max_nodes
    
def clo_cen(num_seeds):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)

    connected_components = list(nx.connected_component_subgraphs(G))

    largest_component = connected_components[0]
    
    clo_cen = nx.closeness_centrality(largest_component)
    max_nodes = heapq.nlargest(num_seeds, clo_cen, key = clo_cen.get)
    return max_nodes
def eig_cen(num_seeds):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)

    connected_components = list(nx.connected_component_subgraphs(G))

    largest_component = connected_components[0]
    
    eig_cen = nx.closeness_centrality(largest_component)
    max_nodes = heapq.nlargest(num_seeds, eig_cen, key = eig_cen.get)
    return max_nodes
    
def avg_neigh_degree(num_seeds):
    G = nx.Graph()
    avg_deg = {}
    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)
    for n in G.nodes():
        if G.degree(n):
            avg_deg[n] = float(sum(G.degree(i) for i in G[n]))/G.degree(n)
    return heapq.nlargest(num_seeds, avg_deg, key = avg_deg.get)
    
def get_important(lst1, lst2, lst3):
    common = list(set(lst1) & set(lst2))
    final = list(set(common) | set(lst3))
    return list(set(final))
    
def get_seed_nodes(num_seeds):
    max_nodes = bet_cen(num_seeds)
    max_clo = clo_cen(num_seeds)
    max_eig = eig_cen(num_seeds)
    print max_nodes
    print max_clo
    print max_eig
    #print avg_neigh_degree(num_seeds)
    node_choices = get_important(max_nodes, max_clo, max_eig)
    print node_choices
    text_file = open(out_file, "w")
    for rnd in range(50):
        for i in range(0,num_seeds):
            text_file.write(str(node_choices[i]) + "\n")
    text_file.close()

def main():
    global data
    json_data = open(filename).read()
    
    data = json.loads(json_data)


    get_seed_nodes(10)

if __name__ == "__main__":
    main()