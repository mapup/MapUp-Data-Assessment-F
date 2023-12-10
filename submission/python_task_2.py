
import pandas as pd
import numpy as np

# Define a function to calculate the distance matrix
def calculate_distance_matrix (csv_file):
  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv (csv_file)

  # Get the unique IDs from the id_start and id_end columns
  ids = np.unique (df [['id_start', 'id_end']].values)

  # Create an empty matrix of size len(ids) x len(ids)
  matrix = np.zeros ((len (ids), len (ids)))

  # Loop through the rows of the DataFrame
  for index, row in df.iterrows ():
    # Get the id_start, id_end and distance values
    id_start = row ['id_start']
    id_end = row ['id_end']
    distance = row ['distance']

    # Find the indices of id_start and id_end in the ids array
    i = np.where (ids == id_start) [0] [0]
    j = np.where (ids == id_end) [0] [0]

    # Update the matrix with the distance value at (i, j) and (j, i) positions
    matrix [i, j] = distance
    matrix [j, i] = distance

  # Create a pandas DataFrame from the matrix with ids as index and columns.
  df_matrix = pd.DataFrame (matrix, index=ids, columns=ids)

  # Return the DataFrame
  return df_matrix

# Test the function with a sample CSV file
df_matrix = calculate_distance_matrix ('D:\prateek\MapUp-Data-Assessment-F\datasets\dataset-3.csv')

# Print the DataFrame
print (df_matrix)


def unroll_distance_matrix(distance_matrix):
    # Create an empty list to store the unrolled distance matrix
    unrolled_data = []

    # Iterate over the rows and columns of the distance matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            # Skip entries where id_start is equal to id_end
            if id_start == id_end:
                continue

            # Get the distance value for the combination of id_start and id_end
            distance = distance_matrix.loc[id_start, id_end]

            # Append the data to the list
            unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the list of dictionaries
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df


result_unrolled_distance = unroll_distance_matrix(df_matrix)

# Print the resulting unrolled DataFrame
print(result_unrolled_distance)



def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Filter rows based on the reference value in the 'id_start' column
    reference_rows = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    average_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper thresholds within 10% of the average distance
    lower_threshold = average_distance - (0.1 * average_distance)
    upper_threshold = average_distance + (0.1 * average_distance)

    # Filter rows where the distance is within the threshold
    within_threshold = df[(df['id_start'] != reference_value) & 
                          (df['distance'] >= lower_threshold) & 
                          (df['distance'] <= upper_threshold)]

    # Get unique values from the 'id_start' column and sort them
    result_ids = sorted(within_threshold['id_start'].unique())

    return result_ids

# Assuming result_unrolled_distance is the DataFrame created in the previous step
reference_value = 1001400  # Replace with the desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distance, reference_value)

# Print the resulting list of values within the 10% threshold
print(result_within_threshold)


import pandas as pd

def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        # Create a new column with the calculated toll rate for each vehicle type
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Assuming result_unrolled_distance is the DataFrame created in the previous step
result_with_toll_rates = calculate_toll_rate(result_unrolled_distance)

# Print the resulting DataFrame with toll rates
print(result_with_toll_rates)



from datetime import time

def calculate_time_based_toll_rates(df):
    # Define time ranges and discount factors for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]
    
    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))
    
    # Create a new DataFrame to store time-based toll rates
    result_df = pd.DataFrame(columns=df.columns)

    # Iterate through each unique ('id_start', 'id_end') pair
    unique_pairs = df[['id_start', 'id_end']].drop_duplicates()
    
    for index, row in unique_pairs.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']

        # Filter rows for the current ('id_start', 'id_end') pair
        pair_rows = df[(df['id_start'] == id_start) & (df['id_end'] == id_end)]

        # Iterate through each time range
        for start_time, end_time in weekday_time_ranges:
            # Apply discount factor based on the time range for weekdays
            mask_weekday = (pair_rows['start_time'].dt.time >= start_time) & (pair_rows['start_time'].dt.time < end_time)
            pair_rows.loc[mask_weekday, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8 if start_time == time(0, 0, 0) else 1.2

        # Apply discount factor for the weekend time range
        mask_weekend = (pair_rows['start_time'].dt.dayofweek >= 5)
        pair_rows.loc[mask_weekend, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7

        # Append the modified rows to the result DataFrame
        result_df = pd.concat([result_df, pair_rows])

    return result_df


# Assuming result_unrolled_distance is the DataFrame created in the previous step
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_unrolled_distance)

# Print the resulting DataFrame with time-based toll rates
print(result_with_time_based_toll_rates)
