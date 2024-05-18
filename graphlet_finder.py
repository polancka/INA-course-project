
import networkx as nx
from networkx import graph_atlas_g
import random
import matplotlib.pyplot as plt
from itertools import combinations

def graph_to_adjacency_list(G):
    """Convert a NetworkX graph to an adjacency list representation."""
    adj_list = {node: set(neighbors) for node, neighbors in G.adjacency()}
    return adj_list

def draw_histogram(graphlet_counts):
    # Extract graphlet names and counts
    graphlet_names = list(graphlet_counts.keys())
    counts = list(graphlet_counts.values())

    # Create a histogram
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(graphlet_counts)), counts, tick_label=graphlet_names, color='skyblue')
    plt.xlabel('Graphlet')
    plt.ylabel('Count')
    plt.title('Graphlet Counts')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def count_graphlet_occurrences(adj_list, graphlet):
    count = 0
    graphlet_size = len(graphlet.nodes)
    seen_subgraphs = set() 
    
    # Iterate over all combinations of nodes of size equal to the graphlet
    for combo in combinations(adj_list.keys(), graphlet_size):
        #print("__________________________________________")
        #print(combo)
        subgraph_edges = set()
        for u, v in combinations(combo, 2):
            #print(u,v)
            #print(v)
            #print(adj_list[u])
            if v in adj_list[u]:
                subgraph_edges.add((u, v))
        #print(subgraph_edges)
        #print("--------------------------------------------")  
        subgraph = nx.Graph()
        subgraph.add_edges_from(subgraph_edges)
        # Get a canonical form of the subgraph (sorted edge list)
        canonical_form = tuple(sorted(combo))

        if canonical_form not in seen_subgraphs:
            if nx.is_isomorphic(subgraph, graphlet):
                seen_subgraphs.add(canonical_form)
                count += 1
    
    return count

def main():
    print("counting graphlets") 
    graph = nx.read_pajek("graphs/notes_graph.net")
    adj_list = graph_to_adjacency_list(graph)
    atlas = nx.graph_atlas_g()
    graphlets = [G for G in atlas if 2 <= len(G) <= 5 and nx.is_connected(G)]
   
    graphlet_counts = {}
    list_nodes = graph.nodes
    for graphlet in graphlets:
        print(f"graphlet {graphlet}")
        graphlet_str = nx.generate_edgelist(graphlet)
        graphlet_counts[graphlet_str] = count_graphlet_occurrences(adj_list, graphlet)
        print(graphlet_counts[graphlet_str])

    for graphlet, count in graphlet_counts.items():
        print(f"Graphlet:\n{graphlet}\nCount: {count}\n")

    draw_histogram(graphlet_counts)

# if __name__ == "__main__":
#     main()

main()