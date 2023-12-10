import pandas as pd
import networkx as nx

def calculate_distance_matrix():
    # Load the dataset into a DataFrame
    df = pd.read_csv('dataset-3.csv')

    # Create a directed graph to represent toll locations and distances
    G = nx.Graph()

    # Add edges with distances to the graph
    for row in df.itertuples(index=False):
        G.add_edge(row.id_start, row.id_end, distance=row.distance)
        G.add_edge(row.id_end, row.id_start, distance=row.distance)  # Bidirectional

    # Create a DataFrame to store distances
    distance_matrix = pd.DataFrame(index=G.nodes, columns=G.nodes, dtype=float)

    # Calculate cumulative distances between toll locations
    for source in G.nodes:
        for destination in G.nodes:
            # Update distance only if a path exists
            if nx.has_path(G, source, destination):
                distance_matrix.at[source, destination] = nx.shortest_path_length(G, source, destination, weight='distance')

    return distance_matrix


distance_matrix = calculate_distance_matrix()
print(distance_matrix)
