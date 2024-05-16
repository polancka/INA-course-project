import networkx as nx
import random
import midi_player
# Traverses an nx graph with a random walk of certain length and tracks visited nodes (names and durations of notes)

# random walk
def random_walk(graph, walk_length):

    current_node = random.choice(list(graph.nodes()))  # Start from a random node
    walk = [(current_node)]  # Initialize the walk with the start node and duration 0
    
    steps_taken = 0
    while steps_taken < walk_length - 1:
        # Get the neighbors of the current node
        neighbors = list(graph.neighbors(current_node))
        
        if neighbors:
            # Choose a random neighbor
            next_node = random.choice(neighbors)
            # Update the current node and add it to the walk
            current_node = next_node
            walk.append(current_node)
            
            steps_taken += 1
        else:
            # If the current node has no neighbors, break the loop
            break
    
    return walk


def main(graph, walk_length):
    path_made = random_walk(graph, walk_length)
    print(path_made)
   # print(graph.nodes)

    midi_player.main(path_made)


if __name__ == "__main__":
    graph = nx.read_pajek("notes_graph.net")
    main(graph, 5) #adjust the length of the song


