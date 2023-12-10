import pandas as pd
import datetime
import numpy as np
import os

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.
    Args:
        df (pandas.DataFrame)
    Returns:
        pandas.DataFrame: Distance matrix
    """

    ids = []
    ids.extend(list(df['id_start']))
    ids.extend(list(df['id_end']))
    ids = set(ids)
    ids = list(ids)
    ids.sort()
    ids1 =ids
    ids = pd.Series(ids)
    matrix = [[0 for _ in range(len(ids))] for _ in range(len(ids))]

    for index, row in df.iterrows():
        row_index = list(ids).index(row['id_start'])
        col_index = list(ids).index(row['id_end'])
        matrix[row_index][col_index] = row['distance']
        matrix[col_index][row_index] = row['distance']


    distance_matrix = pd.DataFrame(matrix, index=ids, columns=ids)

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if distance_matrix.iloc[i, j] == 0:
                non_zero = distance_matrix.iloc[i, :].replace(0, np.nan).dropna()
                if len(non_zero) > 0:
                    distance_matrix.iloc[i, j] = non_zero.values[0] + distance_matrix.iloc[ids1.index(non_zero.index[0]), j]
                    distance_matrix.iloc[j, i] = distance_matrix.iloc[i, j]

    return distance_matrix

def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Input DataFrame with distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_data = []
    for i in range(len(df.index)):
        for j in range(i + 1, len(df.columns)):
            id_start = df.index[i]
            id_end = df.columns[j]
            distance = df.iloc[i, j]

            # Excluding entries where id_start is the same as id_end
            if id_start != id_end:
                # Appending the data to the list
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Creating a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): DataFrame with columns 'id_start', 'id_end', and 'distance'.
        reference_id (int): Reference ID for which the average distance is calculated.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Calculating the average distance for the reference_id
    reference_row = df[df['id_start'] == reference_id]
    reference_avg = reference_row['distance'].mean()

    # Calculating the lower and upper thresholds
    lower_threshold = reference_avg - 0.1 * reference_avg
    upper_threshold = reference_avg + 0.1 * reference_avg

    # Filtering rows where the average distance is within the 10% threshold
    result = df.groupby('id_start')['distance'].mean().reset_index()
    result = result[(result['distance'] >= lower_threshold) & (result['distance'] <= upper_threshold)]

    # Sorting the result by 'id_start'
    result = result.sort_values(by='id_start')

    return result

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    #Creating the columns in the data frame
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type in rate_coefficients.keys():
        df[vehicle_type] = 0.0
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df


def calculate_time_based_toll_rates(df):
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    weekday_morning = pd.to_datetime('10:00:00').time()
    weekday_evening = pd.to_datetime('18:00:00').time()
    def apply_discount(row):
        if row['start_time'].weekday() < 5:  # Weekdays (Monday - Friday)
            if row['start_time'].time() < weekday_morning:
                return row * 0.8
            elif row['start_time'].time() < weekday_evening:
                return row * 1.2
            else:
                return row * 0.8
        else: 
            return row * 0.7
    vehicles = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle in vehicles:
        df[vehicle] = df[vehicle].apply(apply_discount)
    days_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['start_day'] = df['start_time'].dt.weekday.map(days_of_week)
    df['end_day'] = df['end_time'].dt.weekday.map(days_of_week)
    df['start_time'] = df['start_time'].dt.time
    df['end_time'] = df['end_time'].dt.time
    return df

