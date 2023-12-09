import pandas as pd
from datetime import time


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = distance_matrix + distance_matrix.T
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    
    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = df.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

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
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= reference_avg_distance - threshold) & 
                          (result_df['distance'] <= reference_avg_distance + threshold)]

    return  result_df 


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

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
    weekday_discount_factors = pd.cut(df.index.get_level_values(1).dayofweek, bins=[-1, 0, 10, 18, 24],
                                      labels=[0.8, 1.2, 0.8, 0.8], right=False).astype(float)
    weekend_discount_factors = 0.7
    df['start_day'] = df.index.get_level_values(1).strftime('%A')
    df['end_day'] = df['start_day']
    df['start_time'] = time(0, 0)
    df['end_time'] = time(23, 59, 59)
    df['moto'] = df['moto'] * weekday_discount_factors
    df['car'] = df['car'] * weekday_discount_factors
    df['rv'] = df['rv'] * weekday_discount_factors
    df['bus'] = df['bus'] * weekday_discount_factors
    df['truck'] = df['truck'] * weekday_discount_factors
    weekend_mask = (df['start_day'].isin(['Saturday', 'Sunday']))
    df.loc[weekend_mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factors


    return df
