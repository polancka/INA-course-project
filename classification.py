import numpy as np
import os
import xml.etree.ElementTree as ET
import networkx as nx

from networkx import graph_atlas_g
import matplotlib.pyplot as plt
from itertools import combinations


def graph_to_adjacency_list(G):
    """Convert a NetworkX graph to an adjacency list representation."""
    adj_list = {node: set(neighbors) for node, neighbors in G.adjacency()}
    return adj_list

#engfolk1-5 
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


        #changed from gf
        canonical_form = tuple(sorted(map(str,combo)))

        if canonical_form not in seen_subgraphs:
            if nx.is_isomorphic(subgraph, graphlet):
                seen_subgraphs.add(canonical_form)
                count += 1
    
    return count

def parse_musicxml(file_path, save=False, save_label="music", multi=False) -> nx.DiGraph | nx.MultiDiGraph:
	
    G = nx.MultiDiGraph()

    keys_major = ["F", "C", "G", "D", "A", "E", "B"]
    keys_minor = ["B", "E", "A", "D", "G", "C", "F"]
	
    tree = ET.parse(file_path)
    root = tree.getroot()

    prev_note = None
    chord = []

    key = int(root.find(".//key").findall(".//fifths")[0].text)
    key_changes = ""
    if key > 0:
        key_changes = keys_major[:key]
    elif key < 0:
        key_changes = keys_minor[:abs(key)]

    for part in root.findall(".//part"):
        #find all child elements with "measure" tag
        for measure in part.findall(".//measure"):
            #find all child elements with "note" tag
            for note in measure.findall(".//note"):
                pitch = note.find(".//pitch")
                beat = note.find(".//type")
                is_chord = note.find(".//chord") is not None

                if pitch is None and beat is not None:

                    label = ("rest", 0, 0, beat.text)

                    if label not in G.nodes:
                        G.add_node(label)
                    if prev_note is not None:
                        if (prev_note, label) not in G.edges or multi:
                            G.add_edge(prev_note, label)
                    prev_note = label

                elif pitch is not None and beat is not None:
                    step = pitch.find(".//step").text
                    octave = pitch.find(".//octave").text
                    alter = pitch.find(".//alter")

                    initial_alter = 0
                    if step in key_changes and key > 0:
                        initial_alter = 1
                    elif step in key_changes and key < 0:
                        initial_alter = -1

                    if alter is None:
                        alter = initial_alter
                    else:
                        alter = alter.text

                    #add to graph
                    if is_chord:
                        #print("found chord")
                        if len(chord) == 0:
                            chord.append(prev_note)
                        chord_prev = chord.copy()
                        chord.append((step, octave, alter, beat.text))
                        if len(chord) == 2:
                            mapping = {prev_note: tuple(chord)}
                        else:
                            mapping = {tuple(chord_prev): tuple(chord)}
                        #print(mapping)
                        G = nx.relabel_nodes(G, mapping, copy=False)

                    else:
                        if len(chord) != 0:
                            prev_note = tuple(chord)
                            chord = []



                        label = (step, octave, alter, beat.text)

                        if label not in G.nodes:
                            G.add_node(label)
                        if prev_note is not None:
                            if (prev_note, label) not in G.edges or multi:
                                G.add_edge(prev_note, label)
                        prev_note = label
                #print(step, octave)
    print(len(G.nodes))
    print(len(G.edges))
	#print(G.nodes)
	#for node in G.nodes:
	#	print(node)

	#save graph
    if save:
        nx.write_pajek(G, f"{save_label}_graph.net")
	#print(len(list(nx.connected_components(nx.Graph(G))))) #confirm that graph is connected
    if not multi:
        G = nx.DiGraph(G)
    return G

def read_graphlet_arrays(directory_path: str):
    graphlet_arrays = {}
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".npy"):
            graphlet_arrays[file_name.removesuffix('.npy')] = np.load(directory_path + file_name)
    return graphlet_arrays

def cos_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def graphlet_calculations():
    genre_graphlet_arrays = []
    save_dir = 'data/test_graphlets/'
    for file_name in os.listdir("graphlet_arrays"):
        if file_name.endswith(".net.npy"):
            with open("./graphlet_arrays/" + file_name, "r") as f:
                genre_graphlet_arrays.append(np.load("./graphlet_arrays/" + file_name))
            print(np.load("./graphlet_arrays/" + file_name))
    print("Loaded Arrays:\n", genre_graphlet_arrays)
    #np.save(save_dir + 'test', genre_graphlet_arrays[0])

    #dictionary for graphs
    graphs = {}
    graphlet_dic = {}
    for file_name in os.listdir("data/test"):
        if file_name.endswith(".xml"):
            print(file_name.removesuffix('.xml'))
            G = parse_musicxml("data/test/" + file_name)
            #print(file)
            #print("Graph:", G.nodes)
            graphs[file_name.removesuffix('.xml')] = G
            save_dir = "data/test_graphlets/"
            adj_list = graph_to_adjacency_list(G)
            atlas = nx.graph_atlas_g()
            
            graphelets = [G for G in atlas if 2 <= len(G) <= 4 and nx.is_connected(G)]
            graphlet_counts = {}
            for graphlet in graphelets:
                graphlet_counts[graphlet.name] = count_graphlet_occurrences(adj_list, graphlet)
            
            sorted_keys = sorted(graphlet_counts.keys(),key=lambda x: int(x[1:]))

            sorted_values = [graphlet_counts[key] for key in sorted_keys]

            array = np.array(sorted_values)
            graphlet_dic[file_name.removesuffix('.xml')] = array
            np.save(save_dir + file_name.removesuffix('.xml'), array)
            print("Graphlet Array:\n", len(array))


def cos_distance(a, b):
    return 1 - cos_similarity(a, b)

def overall_classification_accuracy(results: dict):
    
    correct = 0
    total = 0
    for sample, genre in results.items():
        if sample.startswith('classical') and genre.startswith('classic'):
            correct += 1
        elif sample.startswith('engfolk') and genre.startswith('englishFolk'):
            correct += 1
        elif sample.startswith('GCH') and genre.startswith('georgianFolk'):
            correct += 1
        elif sample.startswith('modern') and genre.startswith('modern'):
            correct += 1
        elif sample.startswith('scotlute') and genre.startswith('scotishLute'):
            correct += 1
        
        total += 1
    return correct / total
    
def cosine_results() -> dict:
    genre_graphlets_dic = {}
    test_graphlets_dic = {}
    genre_graphlets_dic = read_graphlet_arrays("graphlet_arrays/")
    print(genre_graphlets_dic)
    test_graphlets_dic = read_graphlet_arrays("data/test_graphlets/")
    print(len(test_graphlets_dic))
    results = {}
    classification = {}

    for sample_name, sample_arr in test_graphlets_dic.items():
        results[sample_name] = {}
        for genre_name, genre_arr in genre_graphlets_dic.items():
            results[sample_name][genre_name] = cos_distance(sample_arr, genre_arr)
        print(results[sample_name])
        classification[sample_name] = min(results[sample_name], key=results[sample_name].get)
    return classification

def genre_classification_accuracy(classification: dict):
    classic_correct = 0
    classic_total = 0
    englishFolk_correct = 0
    englishFolk_total = 0
    georgianFolk_correct = 0
    georgianFolk_total = 0
    modern_correct = 0
    modern_total = 0
    scotishLute_correct = 0
    scotishLute_total = 0
    accuracy = {}
    for sample, genre in classification.items():
        if sample.startswith('classical') and genre.startswith('classic'):
            classic_correct += 1
        elif sample.startswith('engfolk') and genre.startswith('englishFolk'):
            englishFolk_correct += 1
        elif sample.startswith('GCH') and genre.startswith('georgianFolk'):
            georgianFolk_correct += 1
        elif sample.startswith('modern') and genre.startswith('modern'):
            modern_correct += 1
        elif sample.startswith('scotlute') and genre.startswith('scotishLute'):
            scotishLute_correct += 1
        if sample.startswith('classical'):
            classic_total += 1
        elif sample.startswith('engfolk'):
            englishFolk_total += 1
        elif sample.startswith('GCH'):
            georgianFolk_total += 1
        elif sample.startswith('modern'):
            modern_total += 1
        elif sample.startswith('scotlute'):
            scotishLute_total += 1
    accuracy['classic'] = classic_correct / classic_total
    accuracy['englishFolk'] = englishFolk_correct / englishFolk_total
    accuracy['georgianFolk'] = georgianFolk_correct / georgianFolk_total
    accuracy['modern'] = modern_correct / modern_total
    accuracy['scotishLute'] = scotishLute_correct / scotishLute_total

    return accuracy


def main():
    classification = cosine_results()
    accuracy = overall_classification_accuracy(classification)
    genre_acc = genre_classification_accuracy(classification)
    print(f'Overall accuracy :{accuracy}')
    for k in genre_acc:
        print(f'{k} accuracy: {genre_acc[k]}')


main()