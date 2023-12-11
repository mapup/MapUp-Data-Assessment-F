import pandas as pd
import numpy as np

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    return distance_matrix


def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = df.unstack().reset_index(name='distance').rename(columns={'level_0': 'id_start', 'id_end': 'id_end'})
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    avg_distance_reference = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * avg_distance_reference
    
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= (avg_distance_reference - threshold)) & 
                          (result_df['distance'] <= (avg_distance_reference + threshold))]
    return result_df


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['toll_rate'] = np.where(df['vehicle_type'] == 'car', df['distance'] * 0.1,
                               np.where(df['vehicle_type'] == 'truck', df['distance'] * 0.2, 0))
    return df


def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    bins = [0, 6, 12, 18, 24]
    labels = ['night', 'morning', 'afternoon', 'evening']
    
    df['time_interval'] = pd.cut(df['timestamp'].dt.hour, bins=bins, labels=labels, include_lowest=True)
    
    df['time_based_toll_rate'] = np.where(df['time_interval'] == 'night', df['distance'] * 0.05,
                                          np.where(df['time_interval'] == 'morning', df['distance'] * 0.1,
                                                   np.where(df['time_interval'] == 'afternoon', df['distance'] * 0.15,
                                                            np.where(df['time_interval'] == 'evening', df['distance'] * 0.2, 0))))
    
    return df
