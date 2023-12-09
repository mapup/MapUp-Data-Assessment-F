import pandas as pd
import numpy as np
def calculate_distance_matrix(df):
    pivot_table = df.pivot_table(values='Distance', index='ID1', columns='ID2', fill_value=0)
    full_matrix = pivot_table.add(pivot_table.T, fill_value=0)
    np.fill_diagonal(full_matrix.values, 0)
    for col in full_matrix.columns:
        for idx in full_matrix.index:
            if full_matrix.loc[idx, col] == 0 and idx != col:
                connected_ids = [x for x in full_matrix.index if fu…
                                 
import pandas as pd
def unroll_distance_matrix(distance_matrix):
    distance_df = distance_matrix.rename_axis('id_start').reset_index()
    unrolled_df = distance_df.melt(id_vars='id_start', var_name='id_end', value_name='distance')
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled_df.reset_index(drop=True)

import pandas as pd
def find_ids_within_ten_percentage_threshold(df, reference_value):
    avg_distance_reference = df[df['id_start'] == reference_value]['distance'].mean()
    lower_bound = avg_distance_reference * 0.9
    upper_bound = avg_distance_reference * 1.1
    within_threshold = df[(df['id_start'] != reference_value) & 
                          (df['distance'] >= lower_bound) & 
                          (df['distance'] <= upper_bound)]['id_start'].unique()
    return sorted(within_threshold)
  
import pandas as pd
def calculate_toll_rate(distance_matrix):
    toll_df = distance_matrix.copy()
    toll_df['moto'] = toll_df.apply(lambda row: row * 0.8 if row.name != row.index else 0, axis=1)
    toll_df['car'] = toll_df.apply(lambda row: row * 1.2 if row.name != row.index else 0, axis=1)
    toll_df['rv'] = toll_df.apply(lambda row: row * 1.5 if row.name != row.index else 0, axis=1)
    toll_df['bus'] = toll_df.apply(lambda row: row * 2.2 if row.name != row.index else 0, axis=1)
    toll_df['truck'] = toll_df.apply(lambda row: row * 3.6 if row.name != row.index else 0, axis=1) 
    return toll_df

import pandas as pd
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
