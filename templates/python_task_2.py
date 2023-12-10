import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    df = pd.read_csv(file_path)


    distances = {}

   
    for _, row in df.iterrows():
        origin = row['origin']
        destination = row['destination']
        distance = row['distance']

       
        if (origin, destination) in distances:
            distances[(origin, destination)] += distance
        else:
            distances[(origin, destination)] = distance

      
        if (destination, origin) in distances:
            distances[(destination, origin)] = distances[(origin, destination)]

    
    distance_matrix = pd.DataFrame(index=df['origin'].unique(), columns=df['origin'].unique())

    for (origin, destination), distance in distances.items():
        distance_matrix.loc[origin, destination] = distance

 
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    # Convert values to numeric
    distance_matrix = distance_matrix.apply(pd.to_numeric, errors='coerce')

    return distance_matrix


distance_matrix = calculate_distance_matrix('dataset-3.csv')
print(distance_matrix)

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    def unroll_distance_matrix(distance_matrix):

    indices = distance_matrix.index

  
    id_start_list = []
    id_end_list = []
    distance_list = []


    for i, row_index in enumerate(indices):
        for j, col_index in enumerate(indices):
            if i != j:  
                id_start_list.append(row_index)
                id_end_list.append(col_index)
                distance_list.append(distance_matrix.loc[row_index, col_index])

    
    unrolled_df = pd.DataFrame({
        'id_start': id_start_list,
        'id_end': id_end_list,
        'distance': distance_list
    })

    return unrolled_df


distance_matrix = generate_car_matrix()  
unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df)

    return df


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
    # Write your logic here

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
   def find_ids_within_ten_percentage_threshold(df, reference_value):
 
    reference_rows = df[df['id_start'] == reference_value]

  
    average_distance = reference_rows['distance'].mean()

   
    lower_threshold = average_distance - (average_distance * 0.1)
    upper_threshold = average_distance + (average_distance * 0.1)

    
    filtered_ids = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]['id_start'].unique()


    sorted_filtered_ids = sorted(filtered_ids)

    return sorted_filtered_ids


reference_value = 123  # Replace with your actual reference value
result = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(result)

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
 import numpy as np
from datetime import datetime, time, timedelta

def calculate_time_based_toll_rates(df):
  
    time_ranges_weekdays = [(time(0, 0), time(10, 0)), (time(10, 0), time(18, 0)), (time(18, 0), time(23, 59, 59))]
    time_ranges_weekends = [(time(0, 0), time(23, 59, 59))]
    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7

   
    df['start_day'] = df['start_datetime'].dt.day_name()
    df['end_day'] = df['end_datetime'].dt.day_name()
    df['start_time'] = df['start_datetime'].dt.time
    df['end_time'] = df['end_datetime'].dt.time

    
    def calculate_toll_rate(row):
        if row['start_day'] in ['Saturday', 'Sunday']:
            return row['distance'] * discount_factor_weekends
        else:
            for time_range, discount_factor in zip(time_ranges_weekdays, discount_factors_weekdays):
                start_time, end_time = time_range
                if start_time <= row['start_time'] <= end_time and start_time <= row['end_time'] <= end_time:
                    return row['distance'] * discount_factor


    df['time_based_toll'] = df.apply(calculate_toll_rate, axis=1)

    return df


result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_based_toll_rates)

