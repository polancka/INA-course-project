import networkx as nx
import os

import xml.etree.ElementTree as ET

def parse_musicxml(data_path, save=False, save_label="music", multi=False):
	G = nx.MultiDiGraph()

	keys_major = ["F", "C", "G", "D", "A", "E", "B"]
	keys_minor = ["B", "E", "A", "D", "G", "C", "F"]

	for filename in os.listdir(data_path):
		if not (filename.endswith(".xml") or filename.endswith(".musicxml")):
			print(filename)
			continue
		#print(filename)
		file_path = data_path + "/" + filename
		#print(file_path)
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



if __name__ == "__main__":
	parse_musicxml("data/georgianFolk", save=True, save_label="georgianFolk")
	parse_musicxml("data/georgianFolk", save=True, save_label="georgianFolk_multi", multi=True)
