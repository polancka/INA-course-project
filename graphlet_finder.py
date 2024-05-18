
import networkx as nx
from networkx import graph_atlas_g
import random
import matplotlib.pyplot as plt
from itertools import combinations

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

def count_graphlet_occurrences(G, graphlet):
    count = 0
    graphlet_size = len(graphlet.nodes)
    nodes = list(G.nodes())
    
    # Convert the graphlet into a networkx graph object
    graphlet = nx.Graph(graphlet)
    
    # Iterate over all combinations of nodes in G of size equal to the graphlet
    for combo in combinations(nodes, graphlet_size):
        mutli_subgraph = G.subgraph(combo)
        subgraph = nx.Graph(mutli_subgraph)
        if nx.is_isomorphic(subgraph, graphlet):
            count += 1
    
    return count

def main():
    print("counting graphlets") 
    graph = nx.read_pajek("notes_graph.net")
    atlas = nx.graph_atlas_g()
    graphlets = [G for G in atlas if 2 <= len(G) <= 5 and nx.is_connected(G)]
    graphlet_counts = {}
    #print(graphlets)

    for graphlet in graphlets:
        print(f"graphlet {graphlet}")
        graphlet_str = nx.generate_edgelist(graphlet, data=False)
        graphlet_counts[graphlet_str] = count_graphlet_occurrences(graph, graphlet)
        print(graphlet_counts[graphlet_str])

    for graphlet, count in graphlet_counts.items():
        print(f"Graphlet:\n{graphlet}\nCount: {count}\n")

    draw_histogram(graphlet_counts)

# if __name__ == "__main__":
#     main()

main()