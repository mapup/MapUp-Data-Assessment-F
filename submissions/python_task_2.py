import pandas as pd
import numpy as np
from datetime import time


def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df_pivot = df.pivot(index='ID1', columns='ID2', values='Distance')
    distance_matrix = df_pivot.add(df_pivot.transpose(), fill_value=0)
    np.fill_diagonal(distance_matrix.values, 0)
    for i in range(len(distance_matrix)):
        for j in range(i+1, len(distance_matrix)):
            if np.isnan(distance_matrix.iloc[i, j]):
                distance_matrix.iloc[i, j] = distance_matrix.iloc[i, :j].add(distance_matrix.iloc[:j, j]).min()
                distance_matrix.iloc[j, i] = distance_matrix.iloc[i, j]

    return distance_matrix


def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:

    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for i in df.columns:
        for j in df.columns:
            if i != j:
                unrolled_df = unrolled_df.append({'id_start': i, 'id_end': j, 'distance': df.loc[i, j]}, ignore_index=True)

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id):
    
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    lower_threshold = reference_avg_distance * 0.9
    upper_threshold = reference_avg_distance * 1.1

    ids_within_threshold = df.groupby('id_start').filter(lambda x: lower_threshold <= x['distance'].mean() <= upper_threshold)

    return sorted(ids_within_threshold['id_start'].unique())


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    
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

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Saturday', 'Sunday']
    time_intervals = [(time(0, 0), time(10, 0), 0.8), 
                      (time(10, 0), time(18, 0), 1.2), 
                      (time(18, 0), time(23, 59, 59), 0.8)]
    weekend_discount = 0.7
    
    for start_day in weekdays + weekends:
        for start_time, end_time, discount in time_intervals:
            mask = (df['start_day'] == start_day) & (df['start_time'] >= start_time) & (df['end_time'] <= end_time)
            df.loc[mask, 'vehicle'] *= discount

    for start_day in weekends:
        df.loc[df['start_day'] == start_day, 'vehicle'] *= weekend_discount

    return df
