import pandas as pd
import networkx as nx
import datetime

# Load the dataset-3
df_distance = pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-3.csv')

# Load the dataset-2 if applicable
df_schedule = pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-2.csv')

def calculate_distance_matrix(df):
    # Create a directed graph to represent routes
    G = nx.DiGraph()

    # Add edges and their distances to the graph
    for index, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], distance=row['distance'])
        G.add_edge(row['id_end'], row['id_start'], distance=row['distance'])  # Account for bidirectional distances

    # Calculate cumulative distances along known routes
    distance_matrix = nx.floyd_warshall_numpy(G, weight='distance')

    # Create a DataFrame from the distance matrix
    distance_df = pd.DataFrame(distance_matrix, index=G.nodes(), columns=G.nodes())

    return distance_df

# Example usage
result = calculate_distance_matrix(df_distance)
print("Distance Matrix DataFrame:")
print(result)

def unroll_distance_matrix(distance_df):
    # Extract node IDs from the index of the distance DataFrame
    nodes = distance_df.index.tolist()

    # Initialize an empty list to store unrolled data
    unrolled_data = []

    # Iterate over node combinations and distances in the distance DataFrame
    for id_start in nodes:
        for id_end in nodes:
            if id_start != id_end:
                distance = distance_df.loc[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a new DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Example usage with the result DataFrame from Question 1
result_unrolled_distance = unroll_distance_matrix(result)
print("Unrolled Distance Matrix DataFrame:")
print(result_unrolled_distance)

def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Filter rows based on the reference value
    reference_rows = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_avg_distance = reference_rows['distance'].mean()

    # Calculate the threshold range (10% of the average distance)
    threshold = 0.1 * reference_avg_distance

    # Filter rows within the threshold range
    within_threshold_rows = df[
        (df['distance'] >= reference_avg_distance - threshold) &
        (df['distance'] <= reference_avg_distance + threshold)
    ]

    # Get unique values from the 'id_start' column and sort them
    result_ids = within_threshold_rows['id_start'].unique()
    result_ids.sort()

    return result_ids.tolist()

# Example usage with the unrolled DataFrame from Question 2 and a reference value
reference_value = 1001402  # Replace this with your desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distance, reference_value)
print(f"IDs within 10% threshold of reference value {reference_value}:")
print(result_within_threshold)

def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Example usage with the unrolled DataFrame from Question 2
result_with_toll_rates = calculate_toll_rate(result_unrolled_distance)
print("Toll Rates DataFrame:")
print(result_with_toll_rates)

def calculate_time_based_toll_rates(df_distance, df_schedule):
    # Merge distance and schedule DataFrames on 'id_start' and 'id_end'
    merged_df = pd.merge(df_distance, df_schedule, left_on=['id_start', 'id_end'], right_on=['id', 'id_2'], how='left')

    # Convert 'startTime' and 'endTime' columns to datetime.time type
    merged_df['startTime'] = pd.to_datetime(merged_df['startTime']).dt.time
    merged_df['endTime'] = pd.to_datetime(merged_df['endTime']).dt.time

    # Initialize new columns for start_day, start_time, end_day, end_time, and discounted_distance
    merged_df['start_day'] = ''
    merged_df['end_day'] = ''
    merged_df['start_time'] = datetime.time()
    merged_df['end_time'] = datetime.time()
    merged_df['discounted_distance'] = 0.0

    # Define time ranges and corresponding discount factors
    time_ranges_weekdays = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0), 0.8),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0), 1.2),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0.8)
    ]

    time_ranges_weekends = [
        (datetime.time(0, 0, 0), datetime.time(23, 59, 59), 0.7)
    ]

    # Iterate through rows in the merged DataFrame
    for index, row in merged_df.iterrows():
        for start_range, end_range, discount_factor in time_ranges_weekdays:
            # Apply discount factor based on the time range for weekdays
            if row['startDay'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and \
               start_range <= row['startTime'] <= end_range:
                merged_df.at[index, 'start_day'] = row['startDay']
                merged_df.at[index, 'end_day'] = row['endDay']
                merged_df.at[index, 'start_time'] = start_range
                merged_df.at[index, 'end_time'] = end_range
                merged_df.at[index, 'discounted_distance'] = row['distance'] * discount_factor
                break  # Exit the loop after finding the appropriate range

        for start_range, end_range, discount_factor in time_ranges_weekends:
            # Apply constant discount factor for weekends
            if row['startDay'] in ['Saturday', 'Sunday'] and \
               start_range <= row['startTime'] <= end_range:
                merged_df.at[index, 'start_day'] = row['startDay']
                merged_df.at[index, 'end_day'] = row['endDay']
                merged_df.at[index, 'start_time'] = start_range
                merged_df.at[index, 'end_time'] = end_range
                merged_df.at[index, 'discounted_distance'] = row['distance'] * discount_factor
                break  # Exit the loop after finding the appropriate range

    # Drop unnecessary columns
    merged_df = merged_df[['id_start', 'id_end', 'distance', 'moto', 'car', 'start_day', 'end_day', 'start_time', 'end_time', 'discounted_distance']]

    return merged_df

# Example usage with the unrolled DataFrame from Question 2 and a reference value
reference_value = 1001402  # Replace this with your desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distance, reference_value)
print(f"IDs within 10% threshold of reference value {reference_value}:")
print(result_within_threshold)

# Example usage with the result DataFrame from Question 3
result_time_based = calculate_time_based_toll_rates(result_unrolled_distance, df_schedule)

# Uncomment the following line to print the result
print("Time-Based Toll Rates DataFrame:")
pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
print(result_time_based)