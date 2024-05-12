import networkx as nx
import random
# Traverses an nx graph with a random walk of certain length and tracks visited nodes (names and durations of notes)

# random walk
def random_walk(graph, walk_length):

    current_node = random.choice(list(graph.nodes()))  # Start from a random node
    walk = [(current_node, graph.nodes[current_node]['duration'])]  # Initialize the walk with the start node and duration 0
    
    steps_taken = 0
    while steps_taken < walk_length - 1:
        # Get the neighbors of the current node
        neighbors = list(graph.neighbors(current_node))
        
        if neighbors:
            # Choose a random neighbor
            next_node = random.choice(neighbors)
            # Update the current node and add it to the walk
            current_node = next_node
            walk.append((current_node, graph.nodes[current_node]['duration']))
            
            steps_taken += 1
        else:
            # If the current node has no neighbors, break the loop
            break
    
    return walk


def main(graph, walk_length):
    path_made = random_walk(graph, walk_length)
    print(path_made)


if __name__ == "__main__":
    #Test mini graph
    graph = nx.Graph()
    for i in range(10):
        node_name = 60 + i  # Starting from MIDI pitch 60
        duration = random.choice([1.0, 0.5, 0.25])  # Randomly chooses duration
        
        # Add node with name and duration attribute
        graph.add_node(node_name, duration=duration)
    nodes = list(graph.nodes())
    for i, node in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.4:
                graph.add_edge(node, nodes[j])

    #give graph and step limit for the walk
    main(graph, 4)
