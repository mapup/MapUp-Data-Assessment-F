import os
import pandas as pd
import datetime


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    pivot_table = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='sum', fill_value=0)
    distance_matrix = pivot_table + pivot_table.T
    return distance_matrix


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        distance_matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = distance_matrix.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    lower_bound = 0.9 * avg_distance
    upper_bound = 1.1 * avg_distance
    result_df = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]['id_start'].unique()
    return sorted(result_df)


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create a new DataFrame with only the required columns
    result_df = df[['id_start', 'id_end']]

    # Calculate toll rates for each vehicle and add columns to the result DataFrame
    for vehicle in rate_coefficients:
        result_df[vehicle] = df['distance'] * rate_coefficients[vehicle]

    return result_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    def get_discount_factor(hour, day):
        if day in ['Saturday', 'Sunday']:
            return 0.7
        elif 0 <= hour < 10 or 18 <= hour <= 23:
            return 0.8
        elif 10 <= hour < 18:
            return 1.2
        else:
            return 1.0

    # Extracting start_day, end_day, start_time, and end_time from id_start and id_end
    df['start_day'] = pd.to_datetime(df['id_start'].astype(str).str[:2], format='%d').dt.day_name()
    df['end_day'] = pd.to_datetime(df['id_end'].astype(str).str[:2], format='%d').dt.day_name()
    df['start_time'] = pd.to_datetime('2023-01-01 ' + df['id_start'].astype(str).str[2:], format='%Y-%m-%d %H%M%S').dt.time
    df['end_time'] = pd.to_datetime('2023-01-01 ' + df['id_end'].astype(str).str[2:], format='%Y-%m-%d %H%M%S').dt.time

    # Calculate the discount factor for each row based on start_time and start_day
    df['discount_factor'] = df.apply(lambda row: get_discount_factor(row['start_time'].hour, row['start_day']), axis=1)

    # Apply the discount factor to the toll rates for each vehicle
    vehicles = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle in vehicles:
        df[vehicle] *= df['discount_factor']

    # Drop unnecessary columns
    df = df.drop(columns=['discount_factor'])

    return df


# Example usage:
#df = pd.read_csv('C:/Users/anshu/Desktop/Assesement/MapUp-Data-Assessment-F/datasets/dataset-3.csv')
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the CSV file in the subdirectory
csv_file_path = os.path.join(script_dir, 'dataset', 'dataset-3.csv')

# Read the CSV file using the relative path
df = pd.read_csv(csv_file_path)
distance_matrix = calculate_distance_matrix(df)
unrolled_df = unroll_distance_matrix(distance_matrix)
result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, 1001402)
toll_rate_df = calculate_toll_rate(unrolled_df)
time_based_toll_df = calculate_time_based_toll_rates(toll_rate_df)

# Display the results
print("Distance Matrix:")
print(distance_matrix)
print("\nUnrolled Distance Matrix:")
print(unrolled_df[['id_start', 'id_end', 'distance']])
print("\nIDs within 10% Threshold of Reference Value 1001402:")
print(result_ids)
print("\nToll Rate DataFrame:")
print(toll_rate_df[['id_start', 'id_end', 'moto', 'car', 'rv', 'bus', 'truck']])
print("\nTime-Based Toll Rates DataFrame:")
print(time_based_toll_df[['id_start', 'id_end', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']])
