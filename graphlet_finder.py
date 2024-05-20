
import networkx as nx
from networkx import graph_atlas_g
import random
import matplotlib.pyplot as plt
from itertools import combinations
import json 
import os

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

def draw_line_graph(data):
    # Extract unique x-labels (assuming all lines have the same x-labels for simplicity)
    x_labels = list(data['classic_multi_graph.net'].keys())

    # Creating the line graph for each entry in the dictionary
    for line_label, values_dict in data.items():
        y_values = [values_dict[label] for label in x_labels]
        plt.plot(x_labels, y_values, marker='o', label=line_label)

    # Adding title and labels
    plt.title('Graphlets based on genre')
    plt.xlabel('Graphlets')
    plt.ylabel('Genre graphs')

    # Adding a legend
    plt.legend()

    # Display the graph
    plt.show()

def count_graphlet_occurrences(adj_list, graphlet):
    count = 0
    graphlet_size = len(graphlet.nodes)
    seen_subgraphs = set() 
    
    # Iterate over all combinations of nodes of size equal to the graphlet
    for combo in combinations(adj_list.keys(), graphlet_size):
        subgraph_edges = set()
        for u, v in combinations(combo, 2):
            if v in adj_list[u]:
                subgraph_edges.add((u, v))
 
        subgraph = nx.Graph()
        subgraph.add_edges_from(subgraph_edges)

        canonical_form = tuple(sorted(combo))

        if canonical_form not in seen_subgraphs:
            if nx.is_isomorphic(subgraph, graphlet):
                seen_subgraphs.add(canonical_form)
                count += 1
    
    return count

def main():

    directory_path = 'graphs/'
    json_save_directory = 'graphlet_jsons/'
    end_graphlets = {}
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(file_path)

        print("counting graphlets") 
        graph = nx.read_pajek(file_path)
        adj_list = graph_to_adjacency_list(graph)
        atlas = nx.graph_atlas_g()
        graphlets = [G for G in atlas if 2 <= len(G) <= 4 and nx.is_connected(G)]

        graphlet_counts = {}
        list_nodes = graph.nodes
        for graphlet in graphlets:
            print(f"graphlet {graphlet.name}")
            graphlet_str = nx.generate_edgelist(graphlet)
            graphlet_counts[graphlet.name] = count_graphlet_occurrences(adj_list, graphlet)
            print(graphlet_counts[graphlet.name])

        for graphlet, count in graphlet_counts.items():
            print(f"Graphlet:\n{graphlet}\nCount: {count}\n")
        
        #draw_histogram(graphlet_counts) #TODO: change from histogram to line graph
        end_graphlets[filename] = graphlet_counts # save for later visualisation
        # Convert and write JSON object to file
        json_filename = f"{filename}.json"
        json_file_path = os.path.join(json_save_directory, json_filename)
        with open(json_file_path, 'w') as json_file:
            json.dump(graphlet_counts, json_file, indent=4)

        #TODO: line graph for all netwroks at once
    draw_line_graph(end_graphlets)

# if __name__ == "__main__":
#     main()

main()