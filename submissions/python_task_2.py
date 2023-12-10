#Question:1=Distance Matrix Calcuation:

import pandas as pd
import networkx as nx

def calculate_distance_matrix(dataframe):
    graph = nx.DiGraph()

    for _, row in dataframe.iterrows():
        source = row['id_start']
        target = row['id_end']
        distance = row['distance']

        graph.add_edge(source, target, weight=distance)
        graph.add_edge(target, source, weight=distance)

    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(graph))

    # Create a DataFrame to store the distance matrix
    locations = sorted(graph.nodes())
    distance_matrix = pd.DataFrame(index=locations, columns=locations)

    for source in locations:
        for target in locations:
            if source == target:
                distance_matrix.loc[source, target] = 0
            else:
                distance_matrix.loc[source, target] = shortest_paths[source][target]

    return distance_matrix


dataset = pd.read_csv(r"C:\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv")
result = calculate_distance_matrix(dataset)
print(result.head())


#Question:2=Unroll Distance Matrix:
def unroll_distance_matrix(distance_matrix):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        distance_matrix (pandas.DataFrame): Distance matrix DataFrame.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    ids = distance_matrix.index
    unrolled_data = []

    for i, id_start in enumerate(ids):
        for id_end in ids[i + 1:]:
            distance = distance_matrix.at[id_start, id_end]
            unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    return pd.DataFrame(unrolled_data)
dataset = pd.read_csv("C:\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv")
distance_matrix = calculate_distance_matrix(dataset)
result_matrix = unroll_distance_matrix(distance_matrix)
print("Unrolled Distance Matrix:")
print(result_matrix.head())

#Question:3=Finding IDs within Percentage Threshold:
def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): DataFrame containing distance information.
        reference_id (int): Reference ID.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    avg_dist = df.loc[df['id_start'] == reference_id, 'distance'].mean()

    # Define 10% threshold range
    thresh_min = 0.9 * avg_dist
    thresh_max = avg_dist + 0.1 * avg_dist

    # Filter values within the threshold and return a DataFrame
    filtered_values = df.loc[(df['distance'] >= thresh_min) & (df['distance'] <= thresh_max)].sort_values(by='id_start')

    return filtered_values
reference_id = 1001412  # You can change this to any valid reference_id
filtered_values = find_ids_within_ten_percentage_threshold(result_matrix, reference_id)
print(f"IDs within 10% of average distance for reference_id {reference_id}:")
print(filtered_values.head())

#Question:4=Calculate Toll Rate
def calculate_toll_rate(distance_matrix):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        distance_matrix (pandas.DataFrame): DataFrame containing distance information.

    Returns:
        pandas.DataFrame: DataFrame with toll rates for each vehicle type.
    """
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create a copy to avoid modifying the original DataFrame
    result_matrix = distance_matrix.copy()

    # Add columns for each vehicle type with their respective toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        result_matrix[vehicle_type] = result_matrix['distance'] * rate_coefficient

    return result_matrix
toll_rate_matrix = calculate_toll_rate(result_matrix)
print("Toll Rate Matrix:")
print(toll_rate_matrix.head())