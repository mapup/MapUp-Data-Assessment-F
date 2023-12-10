#1
import pandas as pd
import networkx as nx

def calculate_distance_matrix(file_path):
 
    df = pd.read_csv(file_path)

    source_col = df.columns[0]
    target_col = df.columns[1]
    distance_col = df.columns[2]

    G = nx.from_pandas_edgelist(df, source=source_col, target=target_col, edge_attr=[distance_col], create_using=nx.DiGraph())

    nodes = list(G.nodes)
    node_pairs = [(node1, node2) for i, node1 in enumerate(nodes) for node2 in nodes[i + 1:]]

    distances = {}
    for pair in node_pairs:
        try:
            distance = nx.shortest_path_length(G, pair[0], pair[1], weight=distance_col)
            distances[pair] = distance
        except nx.NetworkXNoPath:
            print(f"No path between {pair[0]} and {pair[1]}")

    distance_df = pd.DataFrame(index=nodes, columns=nodes)
    for pair, distance in distances.items():
        distance_df.at[pair[0], pair[1]] = distance
        distance_df.at[pair[1], pair[0]] = distance

    distance_df.values[[range(distance_df.shape[0])]*2] = 0

    return distance_df

file_path = 'dataset-3.csv'
result_matrix = calculate_distance_matrix(file_path)
print(result_matrix)



#2
import pandas as pd

def unroll_distance_matrix(input_matrix):
    
    columns = input_matrix.columns

    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for id_start in columns:
        for id_end in columns:
            if id_start != id_end:
            
                distance = input_matrix.at[id_start, id_end]

                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

    return unrolled_df

result_unrolled = unroll_distance_matrix(result_matrix)
print(result_unrolled)



#3
import pandas as pd
def find_ids_within_ten_percentage_threshold(input_df, reference_value):
    # Filter the DataFrame for rows with the reference value in the id_start column
    reference_rows = input_df[input_df['id_start'] == reference_value]

    average_distance = reference_rows['distance'].mean()

    lower_threshold = average_distance - 0.1 * average_distance
    upper_threshold = average_distance + 0.1 * average_distance

    within_threshold_rows = input_df[(input_df['distance'] >= lower_threshold) & (input_df['distance'] <= upper_threshold)]

    sorted_ids_within_threshold = sorted(within_threshold_rows['id_start'].unique())

    return sorted_ids_within_threshold

result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled, reference_value)
print(result_within_threshold)




#4
import pandas as pd

def calculate_toll_rate(input_df):
    
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        input_df[vehicle_type] = input_df['distance'] * rate_coefficient

    return input_df

result_with_toll_rates = calculate_toll_rate(result_unrolled)
print(result_with_toll_rates)




#5
import pandas as pd

def multiply_matrix(input_df):
    # Make a copy of the input DataFrame to avoid modifying the original
    modified_df = input_df.copy()

    # Apply the multiplication logic
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df

# Example usage (assuming you already have the result_df from Question 1)
file_path = 'path/to/dataset-1.csv'
result_df = generate_car_matrix(file_path)  # Replace this with the actual generation logic
modified_result_df = multiply_matrix(result_df)
print(modified_result_df)
