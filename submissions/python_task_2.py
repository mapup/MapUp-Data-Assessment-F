import pandas as pd
import numpy as np
from datetime import time


def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the distance matrix based on the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'ID1', 'ID2', and 'Distance'.

    Returns:
        pd.DataFrame: Distance matrix with 'ID1' and 'ID2' as indices and columns.
    """
    # Pivot the DataFrame to create a matrix of distances between pairs of IDs
    df_pivot = df.pivot(index='ID1', columns='ID2', values='Distance')
    distance_matrix = df_pivot.add(df_pivot.transpose(), fill_value=0)
    
    # Fill diagonal with zeros to represent distance from an ID to itself
    np.fill_diagonal(distance_matrix.values, 0)
    
    # Fill missing values by finding the minimum distance path
    for i in range(len(distance_matrix)):
        for j in range(i+1, len(distance_matrix)):
            if np.isnan(distance_matrix.iloc[i, j]):
                distance_matrix.iloc[i, j] = distance_matrix.iloc[i, :j].add(distance_matrix.iloc[:j, j]).min()
                distance_matrix.iloc[j, i] = distance_matrix.iloc[i, j]

    return distance_matrix


def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unrolls the distance matrix into a DataFrame with columns 'id_start', 'id_end', and 'distance'.

    Args:
        df (pd.DataFrame): Input DataFrame representing a distance matrix.

    Returns:
        pd.DataFrame: Unrolled DataFrame with columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for i in df.columns:
        for j in df.columns:
            if i != j:
                unrolled_df = unrolled_df.append({'id_start': i, 'id_end': j, 'distance': df.loc[i, j]}, ignore_index=True)

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Finds IDs with average distances within 10% threshold of the reference ID.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'id_start', 'id_end', and 'distance'.
        reference_id: ID for which to find nearby IDs.

    Returns:
        List: IDs within the 10% threshold.
    """
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    lower_threshold = reference_avg_distance * 0.9
    upper_threshold = reference_avg_distance * 1.1

    ids_within_threshold = df.groupby('id_start').filter(lambda x: lower_threshold <= x['distance'].mean() <= upper_threshold)

    return sorted(ids_within_threshold['id_start'].unique())


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates toll rates based on distance and vehicle type.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'id_start', 'id_end', 'distance', and 'vehicle'.

    Returns:
        pd.DataFrame: Input DataFrame with additional columns for toll rates based on vehicle type.
    """
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate

    return df


def calculate_time_based_toll_rates(df):
    """
    Calculates time-based toll rates based on weekdays, weekends, and time intervals.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'start_day', 'start_time', 'end_time', and 'vehicle'.

    Returns:
        pd.DataFrame: Input DataFrame with updated toll rates based on time intervals.
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Saturday', 'Sunday']
    time_intervals = [(time(0, 0), time(10, 0), 0.8), 
                      (time(10, 0), time(18, 0), 1.2), 
                      (time(18, 0), time(23, 59, 59), 0.8)]
    weekend_discount = 0.7

    # Update toll rates based on time intervals and weekdays
    for start_day in weekdays + weekends:
        for start_time, end_time, discount in time_intervals:
            mask = (df['start_day'] == start_day) & (df['start_time'] >= start_time) & (df['end_time'] <= end_time)
            df.loc[mask, 'vehicle'] *= discount

    # Apply weekend discount
    for start_day in weekends:
        df.loc[df['start_day'] == start_day, 'vehicle'] *= weekend_discount

    return df
