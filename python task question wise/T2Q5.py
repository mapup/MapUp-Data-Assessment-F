import pandas as pd
import networkx as nx
import numpy as np
from datetime import time

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

def calculate_toll_rate(distance_matrix):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Add columns for each vehicle type with their respective toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        distance_matrix[vehicle_type] = distance_matrix['distance'] * rate_coefficient

    return distance_matrix


distance_matrix = calculate_distance_matrix()
unrolled_df = unroll_distance_matrix(distance_matrix)
result_with_toll_rates = calculate_toll_rate(unrolled_df)




def calculate_time_based_toll_rates(input_df):
    # Create a copy of the input DataFrame to avoid modifying the original
    df = input_df.copy()

    # Define time ranges and discount factors
    time_ranges = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]
    
    weekend_discount_factor = 0.7

    # Randomly assign start_day, end_day, start_time, and end_time values
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Ensure that start_day is lower than end_day
    df['start_day'] = np.random.choice(days_of_week, size=len(df))
    df['end_day'] = [np.random.choice([day for day in days_of_week if days_of_week.index(day) >= days_of_week.index(start_day)])
                     for start_day in df['start_day']]
    
    # Ensure that start_time is lower than end_time
    df['start_time'] = [np.random.choice([tr[0] for tr in time_ranges]) for _ in range(len(df))]
    df['end_time'] = [np.random.choice([tr[1] for tr in time_ranges if tr[1] > start_time])
                     for start_time in df['start_time']]

    # Iterate through time ranges and apply discount factors
    for start_time, end_time, discount_factor in time_ranges:
        mask = (df['start_time'] >= start_time) & (df['end_time'] <= end_time)
        for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
            df.loc[mask, vehicle_type] *= discount_factor

    # Apply constant discount factor for weekends
    weekend_mask = (df['start_day'].isin(['Saturday', 'Sunday']))
    for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
        df.loc[weekend_mask, vehicle_type] *= weekend_discount_factor

    return df

result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)

# Display the resulting DataFrame with randomly assigned time-based toll rates
print(result_with_time_based_toll_rates)



