import numpy as np
import pandas as pd
from datetime import datetime, timedelta, time

dataset3 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-3.csv')

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    try:
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce') 
        df = df.dropna(subset=['distance'])

        unique_ids = sorted(set(df['id_start']).union(df['id_end']))
        distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids, dtype=float)

        for _, row in df.iterrows():
            start, end, distance = row['id_start'], row['id_end'], row['distance']
            distance_matrix.at[start, end] += distance
            distance_matrix.at[end, start] += distance

        np.fill_diagonal(distance_matrix.values, 0)
        distance_matrix = distance_matrix + distance_matrix.T

        return distance_matrix

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame(0, index=unique_ids, columns=unique_ids)

result_matrix = calculate_distance_matrix(dataset3)
print(result_matrix)

def unroll_distance_matrix(df) -> pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    try:
        triu_indices = np.triu_indices_from(df, k=1)
        values = df.values[triu_indices]
        unrolled_df = pd.DataFrame({
            'id_start': df.index[triu_indices[0]],
            'id_end': df.columns[triu_indices[1]],
            'distance': values
        })

        return unrolled_df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

unrolled_matrix = unroll_distance_matrix(result_matrix)
print(unrolled_matrix)

def find_ids_within_ten_percentage_threshold(df, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    try:
        reference_df = df[df['id_start'] == reference_id]
        avg_distance = reference_df['distance'].mean()
        lower_threshold = avg_distance - 0.1 * avg_distance
        upper_threshold = avg_distance + 0.1 * avg_distance
        result_df = df[
            (df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)
        ]
        sorted_df = result_df.sort_values(by='id_start')

        print(f"Reference ID: {reference_id}")
        print(f"Avg Distance: {avg_distance}")
        print(f"Threshold Range: {lower_threshold} - {upper_threshold}")
        print("DataFrame with IDs Within 10% Threshold:")
        print(sorted_df)

        return sorted_df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

all_ids = unrolled_matrix['id_start'].unique()
random_reference_value = np.random.choice(all_ids)
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_matrix, random_reference_value)

def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    try:
        df['moto'] = df['distance'] * 0.8
        df['car'] = df['distance'] * 1.2
        df['rv'] = df['distance'] * 1.5
        df['bus'] = df['distance'] * 2.2
        df['truck'] = df['distance'] * 3.6

        return df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

toll_rate_matrix = calculate_toll_rate(unrolled_matrix)
print(toll_rate_matrix)

def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    try:
        toll_rate_matrix = calculate_toll_rate(df)
        time_based_toll_rates = []

        for _, row in toll_rate_matrix.iterrows():
            id_start, id_end, distance, moto, car, rv, bus, truck = row

            time_ranges = [
                (time(0, 0), time(10, 0), 0.8),
                (time(10, 0), time(18, 0), 1.2),
                (time(18, 0), time(23, 59, 59), 0.8)
            ]

            for start_time, end_time, discount_factor in time_ranges:
                time_based_toll_rates.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance,
                    'start_day': 'Monday',  
                    'start_time': start_time,
                    'end_day': 'Sunday',    
                    'end_time': end_time,
                    'moto': moto * discount_factor,
                    'car': car * discount_factor,
                    'rv': rv * discount_factor,
                    'bus': bus * discount_factor,
                    'truck': truck * discount_factor
                })

        time_based_toll_rates_df = pd.DataFrame(time_based_toll_rates)

        return time_based_toll_rates_df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

time_based_toll_rates_df = calculate_time_based_toll_rates(unrolled_matrix)
print(time_based_toll_rates_df)

