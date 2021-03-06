import json
import networkx as nx
import random
import heapq
import matplotlib.pyplot as plt
from input_output import filename, out_file
import random

data = {}


def bet_cen(num_seeds):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)
            
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

# Compute importance of node based on the average degree of its neighbors
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

# Get common nodes between 3 lists
def get_important(lst1, lst2, lst3):
    common = list(set(lst1) & set(lst2))
    final = list(set(common) | set(lst3))
    return list(set(final))


# Degree distance centrality algorithm
# Adapted from "Improving detection of influential nodes in complex networks"
def degree_distance_centrality(num_seeds, threshold=2):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)
    # Compute degree of all nodes in G
    degrees = G.degree()

    seeds = []

    max_nodes = sorted(degrees, None, degrees.get, reverse=True)
    
    while len(seeds) < num_seeds:
        # Randomness to allow for other teams selecting the same nodes in 
        # competition
        seed = max_nodes[random.randint(0, 5)]
        seeds.append(seed)
        max_nodes.remove(seed)
        for n in nx.single_source_shortest_path(G, seed, threshold - 1):
            if n in max_nodes:
                max_nodes.remove(n)             
    return seeds


# Betweenness centrality distance algorithm with threshold 2
# similar to degree distance centrality algorithm
def bet_distance_centrality(num_seeds):
    G = nx.Graph()

    for node in data:
        for neighbor in data[node]:
            G.add_edge(node,neighbor)
    bet_cen = nx.betweenness_centrality(G)
    num_check = num_seeds
    while num_check < len(bet_cen) and num_check < 100 * num_seeds:
        num_check *= 1.5

    seeds = []
    max_nodes = heapq.nlargest(int(num_check), bet_cen, key=bet_cen.get)

    while len(seeds) < num_seeds:
        seed = max_nodes[0]
        seeds.append(seed)
        max_nodes.remove(seed)
        for n in G.neighbors(seed):
            if n in max_nodes:
                max_nodes.remove(n)             
    return seeds       


def get_seed_nodes(num_seeds):
    seeds = degree_distance_centrality(num_seeds, 3)
    # Other measures of selecting seed nodes that we tried
    # seeds = bet_distance_centrality(num_seeds)
    # print seeds
    #max_nodes = bet_cen(num_seeds)
    #max_clo = clo_cen(num_seeds)
    #max_eig = eig_cen(num_seeds)
    #node_choices = get_important(max_nodes, max_clo, max_eig)
    text_file = open(out_file, "w")
    for rnd in range(50):
        for i in range(0,num_seeds):
            text_file.write(str(seeds[i]) + "\n")
    text_file.close()


def main():
    global data
    json_data = open(filename).read()
    
    data = json.loads(json_data)


    get_seed_nodes(20)

if __name__ == "__main__":
    main()