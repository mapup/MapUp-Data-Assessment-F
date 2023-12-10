import pandas as pd
import networkx as nx
import numpy as np

def calculate_distance_matrix():
    # Load the dataset into a DataFrame
    df = pd.read_csv('dataset-3.csv')

    # Create a directed graph to represent toll locations and distances
    G = nx.Graph()

    # Add edges with distances to the graph
    for row in df.itertuples(index=False):
        G.add_edge(row.id_start, row.id_end, distance=row.distance)
        G.add_edge(row.id_end, row.id_start, distance=row.distance)  # Bidirectional

    # Create a symmetric DataFrame to store distances
    distance_matrix = pd.DataFrame(index=G.nodes, columns=G.nodes, dtype=float)

    # Calculate cumulative distances between toll locations
    for source in G.nodes:
        for destination in G.nodes:
            # Update distance only if a path exists
            if nx.has_path(G, source, destination):
                distance_matrix.at[source, destination] = nx.shortest_path_length(G, source, destination, weight='distance')

    # Ensure the matrix is symmetric
    distance_matrix = (distance_matrix + distance_matrix.T) / 2

    return distance_matrix

def unroll_distance_matrix(distance_matrix):
    # Extract the upper triangular part of the matrix (excluding the diagonal)
    upper_triangle = distance_matrix.where(np.triu(np.ones(distance_matrix.shape), k=1).astype(bool))

    # Reset the index and rename columns for the melted DataFrame
    unrolled_df = upper_triangle.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df

def find_ids_within_ten_percentage_threshold(distance_matrix, reference_value):
    # Calculate average distance for the reference value
    average_distance = distance_matrix.loc[distance_matrix['id_start'] == reference_value, 'distance'].mean()

    # Find values within 10% threshold
    threshold_min = 0.9 * average_distance
    threshold_max = average_distance + 0.1 * average_distance 

    # Filter values within the threshold and return a sorted list
    result_values = sorted(distance_matrix.loc[(distance_matrix['distance'] >= threshold_min) & (distance_matrix['distance'] <= threshold_max), 'id_start'].unique())

    return result_values


distance_matrix = calculate_distance_matrix()
unrolled_df = unroll_distance_matrix(distance_matrix)

# Assuming reference_value is a specific ID from the id_start column
reference_value = 1001400

result = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(result)
