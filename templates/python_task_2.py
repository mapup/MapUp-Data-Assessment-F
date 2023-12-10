import pandas as pd
import numpy as np
import time
df = pd.read_csv('datasets/dataset-3.csv')
def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # unique IDs
    unique_ids = np.union1d(df['id_start'].unique(), df['id_end'].unique())

    # empty matrix
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    # Set diagonal values to 0
    np.fill_diagonal(distance_matrix.values, 0)

    for i, row in df.iterrows():
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.at[row['id_end'], row['id_start']] = row['distance']

    # cumulative distances
    for i in unique_ids:
        for j in unique_ids:
            for k in unique_ids:
                if not np.isnan(distance_matrix.at[j, i]) and not np.isnan(distance_matrix.at[i, k]):
                    if np.isnan(distance_matrix.at[j, k]):
                        distance_matrix.at[j, k] = distance_matrix.at[j, i] + distance_matrix.at[i, k]
                    else:
                        distance_matrix.at[j, k] = min(distance_matrix.at[j, k], distance_matrix.at[j, i] + distance_matrix.at[i, k])

    return distance_matrix


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.
    Args:
        df (pandas.DataFrame)
    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # distance matrix to a unroll DataFrame
    unroll_matrix = distance_matrix.unstack().reset_index()
    unroll_matrix.columns = ['id_start', 'id_end', 'distance']

    # where id_start is equal to id_end
    unroll_matrix = unroll_matrix[unroll_matrix['id_start'] != unroll_matrix['id_end']]

    return unroll_matrix



def find_ids_within_ten_percentage_threshold(df, reference_id):
    avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    lower_bound = avg_distance * 0.9
    upper_bound = avg_distance * 1.1
    filtered_ids = df[(df['id_start'] != reference_id) &
                      (df['distance'] >= lower_bound) &
                      (df['distance'] <= upper_bound)]['id_start'].unique()
    return sorted(filtered_ids)


def calculate_toll_rate(input_df):

#Adding initial column for each vehical type
    input_df['moto'] = 0.0
    input_df['car'] = 0.0
    input_df['rv'] = 0.0
    input_df['bus'] = 0.0
    input_df['truck'] = 0.0

#Assigning Toll rates based on Vehical type
    input_df['moto'] = 0.8 * input_df['distance']
    input_df['car'] = 1.2 * input_df['distance']
    input_df['rv'] = 1.5 * input_df['distance']
    input_df['bus'] = 2.2 * input_df['distance']
    input_df['truck'] = 3.6 * input_df['distance']

    return input_df
    


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.
    Args:
        df (pandas.DataFrame)
    Returns:
        pandas.DataFrame
    """
    # time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]


    time_based_toll_df_rows = []


    for _, row in df.iterrows():
        for start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for time_range in weekday_time_ranges if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else weekend_time_ranges:
                # time-based toll DataFrame row
                time_based_toll_df_row = {'id_start': int(row['id_start']), 'id_end': int(row['id_end']), 'distance': row['distance'],
                                       'start_day': start_day, 'end_day': start_day, 'start_time': time_range[0], 'end_time': time_range[1]}

                # Apply discount factors
                if time_range[0] <= time(10, 0, 0) <= time_range[1]:
                    time_based_toll_df_row['moto'] = row['distance'] * 0.8
                    time_based_toll_df_row['car'] = row['distance'] * 1.2
                    time_based_toll_df_row['rv'] = row['distance'] * 1.5
                    time_based_toll_df_row['bus'] = row['distance'] * 2.2
                    time_based_toll_df_row['truck'] = row['distance'] * 3.6
                elif time_range[0] <= time(18, 0, 0) <= time_range[1]:
                    time_based_toll_df_row['moto'] = row['distance'] * 1.2
                    time_based_toll_df_row['car'] = row['distance'] * 1.2
                    time_based_toll_df_row['rv'] = row['distance'] * 1.2
                    time_based_toll_df_row['bus'] = row['distance'] * 1.2
                    time_based_toll_df_row['truck'] = row['distance'] * 1.2
                else:
                    time_based_toll_df_row['moto'] = row['distance'] * 0.8
                    time_based_toll_df_row['car'] = row['distance'] * 0.8
                    time_based_toll_df_row['rv'] = row['distance'] * 0.8
                    time_based_toll_df_row['bus'] = row['distance'] * 0.8
                    time_based_toll_df_row['truck'] = row['distance'] * 0.8


                time_based_toll_df_rows.append(time_based_toll_df_row)

    # Create the time-based toll DataFrame
    time_based_toll_df = pd.DataFrame(time_based_toll_df_rows)

    return time_based_toll_df[['id_start', 'id_end', 'distance', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']]


distance_matrix = calculate_distance_matrix(df)
print(distance_matrix)

unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df)


reference_id = 1001400
result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(result_ids)

toll_matrix = calculate_toll_rate(distance_matrix)
print(toll_matrix)

result_df = pd.DataFrame({'id_start': result_ids})
# Merge the DataFrames 
result_df = pd.merge(unrolled_df, result_df, on='id_start')

final_result_df = calculate_time_based_toll_rates(result_df)
print(final_result_df)