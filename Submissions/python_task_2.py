import pandas as pd
import numpy as np
from itertools import product
from datetime import time
import warnings
warnings.filterwarnings('ignore')

# Question 1: Distance Matrix Calculation
def calculate_distance_matrix(df):
    """
        Calculate a distance matrix based on the dataframe, df.

        Args:
            df (pandas.DataFrame): DataFrame containing columns: ID, Start, End, Distance

        Returns:
            pandas.DataFrame: Distance matrix
        """
# Create an empty DataFrame to store the distance matrix
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(np.zeros((len(unique_ids), len(unique_ids))), index=unique_ids, columns=unique_ids)

# Populate the distance matrix
    for index, row in df.iterrows():
        start = row['id_start']
        end = row['id_end']
        distance = row['distance']

# Update distance values in the matrix
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance

# Calculate cumulative distances
    for i in unique_ids:
        for j in unique_ids:
            for k in unique_ids:
                if distance_matrix.at[i, j] == 0 and i != j and i != k and j != k:
                    if distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

# Set diagonal values to 0
    np.fill_diagonal(distance_matrix.values, 0)

    return distance_matrix


# Question 2: Unroll Distance Matrix
def unroll_distance_matrix(distance_matrix):
    """
        Unroll a distance matrix to a DataFrame in the style of the initial dataset.

        Args:
            distance_matrix (pandas.DataFrame): Distance matrix generated from calculate_distance_matrix function.

        Returns:
            pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
        """
# Get unique IDs from the distance matrix
    unique_ids = distance_matrix.index

# Create an empty DataFrame to store unrolled data
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

# Generate combinations of IDs and retrieve distances from the matrix
    for i in range(len(unique_ids)):
        for j in range(i + 1, len(unique_ids)):
            id_start = unique_ids[i]
            id_end = unique_ids[j]
            distance = distance_matrix.at[id_start, id_end]

# Append the data to the DataFrame
            unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                             ignore_index=True)

    return unrolled_df


# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
       Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

       Args:
           df (pandas.DataFrame): DataFrame containing columns 'id_start', 'id_end', and 'distance'.
           reference_id (int): Reference ID for which the threshold will be calculated.

       Returns:
           pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                             of the reference ID's average distance.
       """
# Calculate average distance for the reference ID
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

# Calculate threshold values
    threshold_min = reference_avg_distance - (reference_avg_distance * 0.1)
    threshold_max = reference_avg_distance + (reference_avg_distance * 0.1)

# Filter IDs within the 10% threshold
    filtered_ids = df.groupby('id_start')['distance'].mean().reset_index()
    filtered_ids = filtered_ids[
        (filtered_ids['distance'] >= threshold_min) & (filtered_ids['distance'] <= threshold_max)]

# Sort and return the resulting DataFrame
    result_df = filtered_ids.sort_values(by='id_start')
    return result_df


# Question 4: Calculate Toll Rate
def calculate_toll_rate(df):
    """
        Calculate toll rates for each vehicle type based on the unrolled DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame containing columns 'id_start', 'id_end', 'distance', and 'vehicle_type'

        Returns:
            pandas.DataFrame: DataFrame with added columns for toll rates for each vehicle type
        """
# Define rate coefficients for different vehicle types
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

# Calculate toll rates for each vehicle type based on distance
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

# Drop the 'distance' column
    #df = df.drop(columns='distance')

    return df

# Question 5: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(input_df):
    # Define time ranges
    time_ranges = {
        'weekday': [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))],
        'weekend': [(time(0, 0, 0), time(23, 59, 59))]
    }

    # Create DataFrames for time ranges
    dfs = {}
    for time_range, ranges in time_ranges.items():
        df = pd.DataFrame(ranges, columns=['start_time', 'end_time'])
        df = pd.concat([df] * len(input_df), ignore_index=True)
        df['id_start'] = input_df['id_start']
        df['id_end'] = input_df['id_end']
        dfs[time_range] = df

    result_df = pd.merge(input_df, dfs['weekday'], on=['id_start', 'id_end'])

    # Define the days of the week and create day combinations
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekends = ['Saturday', 'Sunday']
    day_combinations = {
        'weekdays': list(product(weekdays, repeat=2)),
        'weekends': list(product(weekends, repeat=2))
    }

    # Create DataFrames for day combinations
    day_combination_dfs = {}
    for day_comb, combinations in day_combinations.items():
        df = pd.DataFrame(combinations, columns=['start_day', 'end_day'])
        df = pd.concat([df] * len(input_df), ignore_index=True)
        df['id_start'] = input_df['id_start']
        df['id_end'] = input_df['id_end']
        day_combination_dfs[day_comb] = df

    result_df = pd.merge(result_df, day_combination_dfs['weekdays'], on=['id_start', 'id_end'])
    weekend_comb = pd.merge(dfs['weekend'], day_combination_dfs['weekends'], on=['id_start', 'id_end'])
    result_df1 = pd.merge(result_df[['id_start', 'id_end', 'distance', 'moto', 'car', 'rv', 'bus', 'truck']], weekend_comb,
                          on=['id_start', 'id_end'])
    final_df = pd.concat([result_df, result_df1], axis=0)

    # Adjust start and end times based on weekends
    final_df['start_time'] = np.where((final_df['start_day'].isin(['Saturday', 'Sunday'])) & (
            final_df['end_day'].isin(['Saturday', 'Sunday'])), time(0, 0, 0), final_df['start_time'])
    final_df['end_time'] = np.where((final_df['start_day'].isin(['Saturday', 'Sunday'])) & (
            final_df['end_day'].isin(['Saturday', 'Sunday'])), time(23, 59, 59), final_df['end_time'])

    # Apply coefficients and adjust toll rates
    def get_coeff(row):
        if row['start_day'] in ['Saturday', 'Sunday']:
            return 0.7
        else:
            if row['start_time'] == time(0, 0, 0):
                return 0.8
            elif row['start_time'] == time(10, 0, 0):
                return 1.2
            else:
                return 0.8

    final_df['coeff'] = final_df.apply(get_coeff, axis=1)
    for col in ['moto', 'car', 'rv', 'bus', 'truck']:
        final_df[col] = final_df[col] * final_df['coeff']
    del final_df['coeff']

    final_df = final_df.drop_duplicates()

    return final_df

# Read the dataset
data = pd.read_csv(r'C:\Users\iftik\MapUp\MapUp-Data-Assessment-F\datasets\dataset-3.csv')

# Calculate distance matrix
resulting_distance_matrix = calculate_distance_matrix(data)
print("Distance Matrix Calculation:\n",resulting_distance_matrix)

# Unroll the distance matrix
unrolled_data = unroll_distance_matrix(resulting_distance_matrix)
print("Unroll Distance Matrix:\n",unrolled_data)

# Find IDs within the 10% threshold of the reference ID
reference_value = 1001404  # Replace with the desired reference ID
resulting_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_data, reference_value)
print("Finding IDs within Percentage Threshold:\n",resulting_ids_within_threshold)

# Calculate toll rates for each vehicle type
result_with_toll_rates = calculate_toll_rate(unrolled_data)
print("Calculate Toll Rate:\n",result_with_toll_rates)

# Calculate Time-Based Toll Rates
time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print("Calculate Time-Based Toll Rate:\n",time_based_toll_rates)