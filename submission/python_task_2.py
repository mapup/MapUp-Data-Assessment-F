import pandas as pd
from datetime import datetime, time, timedelta

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distances = {}

    for _, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']

        distances[(id_start, id_end)] = distance

        distances[(id_end, id_start)] = distance

    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))

    distance_matrix = [[0.0] * len(unique_ids) for _ in range(len(unique_ids))]

    for i in range(len(unique_ids)):
        for j in range(i + 1, len(unique_ids)):
            id_i, id_j = unique_ids[i], unique_ids[j]

            if (id_i, id_j) in distances:
                distance_matrix[i][j] = distances[(id_i, id_j)]
                distance_matrix[j][i] = distances[(id_i, id_j)]

    distance_df = pd.DataFrame(distance_matrix, index=unique_ids, columns=unique_ids)

    return distance_df


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    ids = distance_matrix.index

    unrolled_data = []


    for id_start in ids:
        for id_end in ids:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    unrolled_df = pd.DataFrame(unrolled_data)

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
    # Write your logic here
    reference_df = df[(df['id_start'] == reference_id) & (df['distance'] > 0)]

    average_distance = reference_df['distance'].mean()

    threshold_lower = 0.9 * average_distance
    threshold_upper = 1.1 * average_distance

    filtered_df = df[(df['id_start'] != reference_id) & (df['distance'] > 0) & (df['distance'] >= threshold_lower) & (df['distance'] <= threshold_upper)]

    result_ids = sorted(filtered_df['id_start'].unique())

    return result_ids


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type in rate_coefficients.keys():
        df[vehicle_type] = 0.0

    for index, row in df.iterrows():
        distance = row['distance']

        for vehicle_type, rate_coefficient in rate_coefficients.items():
            df.at[index, vehicle_type] = distance * rate_coefficient

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    time_intervals = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]


    weekend_discount_factor = 0.7

    df['start_day'] = ''
    df['start_time'] = pd.to_datetime('1900-01-01')
    df['end_day'] = ''
    df['end_time'] = pd.to_datetime('1900-01-01')

    for index, row in df.iterrows():
        start_time = pd.to_datetime(row['start_time'])
        end_time = pd.to_datetime(row['end_time'])

        df.at[index, 'start_day'] = start_time.strftime('%A')
        df.at[index, 'end_day'] = end_time.strftime('%A')
        df.at[index, 'start_time'] = start_time.time()
        df.at[index, 'end_time'] = end_time.time()

        for interval_start, interval_end, discount_factor in time_intervals:
            if interval_start <= start_time.time() <= interval_end:
                df.at[index, 'distance'] *= discount_factor
                break

        if start_time.weekday() >= 5 or end_time.weekday() >= 5:
            df.at[index, 'distance'] *= weekend_discount_factor

    return df
