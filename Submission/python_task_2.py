import pandas as pd
import numpy as np
def calculate_distance_matrix(data):
    # Assuming 'ID', 'Start', 'End', and 'Distance' are the column names in the DataFrame
    # Read the CSV file if 'data' is a file path
    if isinstance(data, str):
        data = pd.read_csv(data)

    # Create a DataFrame with 'Start' and 'End' columns as indices and 'Distance' as values
    distance_df = data.pivot(index='Start', columns='End', values='distance')

    # Fill NaN values with 0 and set diagonal values to 0
    distance_df = distance_df.fillna(0)
    distance_df.values[[range(len(distance_df))]*2] = 0

    # Ensure the matrix is symmetric
    distance_df = distance_df + distance_df.T

    # Calculate cumulative distances along known routes
    for col in distance_df.columns:
        for row in distance_df.index:
            if distance_df.at[row, col] == 0 and row != col:
                # If distance is unknown, calculate as the sum of known distances
                known_distances = distance_df.loc[row, distance_df.loc[row] != 0]
                for known_col in known_distances.index:
                    distance_df.at[row, col] += distance_df.at[row, known_col]

    return distance_df

# Example usage:
dataset_path = 'datasets/dataset-3.csv'
result_distance_matrix = calculate_distance_matrix(dataset_path)
print(result_distance_matrix)



def unroll_distance_matrix(distance_matrix):
    # Assuming 'ID' is the index of the distance_matrix DataFrame
    # Create a DataFrame with three columns: id_start, id_end, and distance
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate over the rows and columns of the distance_matrix to populate the unrolled DataFrame
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                                 ignore_index=True)

    return unrolled_df

# Example usage:
# Assuming result_distance_matrix is the DataFrame from Question 1
result_unrolled_distance = unroll_distance_matrix(result_distance_matrix)
print(result_unrolled_distance)



def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    # Filter rows for the given reference_value in the 'id_start' column
    reference_rows = distance_df[distance_df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    avg_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper bounds for the 10% threshold
    lower_bound = avg_distance - (avg_distance * 0.1)
    upper_bound = avg_distance + (avg_distance * 0.1)

    # Filter rows where the distance is within the 10% threshold
    within_threshold = distance_df[(distance_df['id_start'] != reference_value) &
                                   (distance_df['distance'] >= lower_bound) &
                                   (distance_df['distance'] <= upper_bound)]

    # Get unique values from the 'id_start' column and sort them
    result_ids = sorted(within_threshold['id_start'].unique())

    return result_ids

# Example usage:
# Assuming result_unrolled_distance is the DataFrame from Question 2
reference_value = 123  # Replace with the desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distance, reference_value)
print(result_within_threshold)




def calculate_toll_rate(distance_df):
    # Assuming 'distance' is the column name in the DataFrame
    # Create new columns for each vehicle type with their respective rate coefficients
    distance_df['moto'] = distance_df['distance'] * 0.8
    distance_df['car'] = distance_df['distance'] * 1.2
    distance_df['rv'] = distance_df['distance'] * 1.5
    distance_df['bus'] = distance_df['distance'] * 2.2
    distance_df['truck'] = distance_df['distance'] * 3.6

    return distance_df

# Example usage:
# Assuming result_unrolled_distance is the DataFrame from Question 2
result_with_toll_rate = calculate_toll_rate(result_unrolled_distance)
print(result_with_toll_rate)


import datetime

def calculate_time_based_toll_rates(distance_df):
    # Assuming 'start_time' and 'end_time' are columns in the DataFrame
    # Convert 'start_time' and 'end_time' columns to datetime.time() type
    distance_df['start_time'] = pd.to_datetime(distance_df['start_time']).dt.time
    distance_df['end_time'] = pd.to_datetime(distance_df['end_time']).dt.time

    # Create columns for start_day and end_day as strings with day values
    distance_df['start_day'] = pd.to_datetime(distance_df['startDay']).dt.day_name()
    distance_df['end_day'] = pd.to_datetime(distance_df['endDay']).dt.day_name()

    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(datetime.time(0, 0, 0), datetime.time(10, 0, 0)),
                           (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
                           (datetime.time(18, 0, 0), datetime.time(23, 59, 59))]
    weekend_time_ranges = [(datetime.time(0, 0, 0), datetime.time(23, 59, 59))]

    # Apply discount factors based on time ranges and day types
    for index, row in distance_df.iterrows():
        for time_range in weekday_time_ranges:
            if time_range[0] <= row['start_time'] <= time_range[1]:
                discount_factor = 0.8 if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 0.7
                distance_df.at[index, 'distance'] *= discount_factor
                break
        for time_range in weekend_time_ranges:
            if time_range[0] <= row['start_time'] <= time_range[1]:
                discount_factor = 0.7
                distance_df.at[index, 'distance'] *= discount_factor
                break

    return distance_df

# Example usage:
# Assuming result_unrolled_distance is the DataFrame from Question 3
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_unrolled_distance)
print(result_with_time_based_toll_rates)
