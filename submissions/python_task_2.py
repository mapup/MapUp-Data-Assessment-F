import pandas as pd
from datetime import time


df = pd.read_csv(r"C:\assignment\MapUp-Data-Assessment-F\datasets\dataset-3.csv")

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Get unique IDs from both id_start and id_end columns
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))

    # Create a DataFrame with ID_start values as both row and column indices
    distance_matrix = pd.DataFrame(float('inf'), index=unique_ids, columns=unique_ids)

    # Set diagonal values to 0
    distance_matrix.values[[range(len(unique_ids))]*2] = 0

    # Update the matrix with distances from the dataset
    for index, row in df.iterrows():
        start_id = row['id_start']
        end_id = row['id_end']
        distance = row['distance']

        # Assign the distance value to the corresponding cell in the matrix
        distance_matrix.at[start_id, end_id] = distance
        distance_matrix.at[end_id, start_id] = distance  # Assign values symmetrically

    # Update the matrix with cumulative distances
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                # Use minimum cumulative distance formula
                distance_matrix.at[i, j] = min(
                    distance_matrix.at[i, j],
                    distance_matrix.at[i, k] + distance_matrix.at[k, j]
                )

    return distance_matrix




def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Convert the distance matrix to a flat DataFrame
    flat_matrix = distance_matrix.unstack().reset_index()
    flat_matrix.columns = ['id_start', 'id_end', 'distance']

    # Filter out rows where id_start is equal to id_end
    flat_matrix = flat_matrix[flat_matrix['id_start'] != flat_matrix['id_end']]

    return flat_matrix






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
    # Filter the DataFrame for the specified reference_id
    reference_df = distance_matrix.loc[[reference_id], :].append(distance_matrix.loc[:, [reference_id]])

    # Calculate the average distance for the reference_id
    average_distance = reference_df.sum().sum() / (len(reference_df) - 1)  # Exclude the reference_id itself

    # Calculate the threshold values
    lower_threshold = average_distance - 0.1 * average_distance
    upper_threshold = average_distance + 0.1 * average_distance

    # Filter the DataFrame for distances within the 10% threshold
    result_df = distance_matrix[
        (distance_matrix.index == reference_id) |
        (distance_matrix[reference_id] >= lower_threshold) &
        (distance_matrix[reference_id] <= upper_threshold)
    ]

    # Extract unique values from the index and columns and sort the list
    result_ids = sorted(set(result_df.index.unique()) | set(result_df.columns.unique()))
    
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
    # Define toll rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create an empty list to store rows for the toll DataFrame
    toll_rows = []

    # Iterate over the rows and columns of the distance matrix
    for start_id, row in distance_matrix.iterrows():
        for end_id, distance in row.items():
            # Skip entries where id_start and id_end are the same
            if start_id != end_id:
                # Create a row for the toll DataFrame
                toll_row = {'id_start': start_id, 'id_end': end_id}

                # Calculate toll rates for each vehicle type
                for vehicle_type, rate_coefficient in rate_coefficients.items():
                    toll_row[vehicle_type] = distance * rate_coefficient

                # Append the row to the list
                toll_rows.append(toll_row)

    # Create the toll DataFrame
    toll_df = pd.DataFrame(toll_rows)

    return toll_df
    


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]

    # Create an empty list to store rows for the time-based toll DataFrame
    time_based_toll_rows = []

    # Iterate over each unique ('id_start', 'id_end') pair
    for _, row in df.iterrows():
        for start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for time_range in weekday_time_ranges if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else weekend_time_ranges:
                # Create a row for the time-based toll DataFrame
                time_based_toll_row = {'id_start': int(row['id_start']), 'id_end': int(row['id_end']), 'distance': row['distance'],
                                       'start_day': start_day, 'end_day': start_day, 'start_time': time_range[0], 'end_time': time_range[1]}

                # Apply discount factors based on time ranges
                if time_range[0] <= time(10, 0, 0) <= time_range[1]:
                    time_based_toll_row['moto'] = row['distance'] * 0.8
                    time_based_toll_row['car'] = row['distance'] * 1.2
                    time_based_toll_row['rv'] = row['distance'] * 1.5
                    time_based_toll_row['bus'] = row['distance'] * 2.2
                    time_based_toll_row['truck'] = row['distance'] * 3.6
                elif time_range[0] <= time(18, 0, 0) <= time_range[1]:
                    time_based_toll_row['moto'] = row['distance'] * 1.2
                    time_based_toll_row['car'] = row['distance'] * 1.2
                    time_based_toll_row['rv'] = row['distance'] * 1.2
                    time_based_toll_row['bus'] = row['distance'] * 1.2
                    time_based_toll_row['truck'] = row['distance'] * 1.2
                else:
                    time_based_toll_row['moto'] = row['distance'] * 0.8
                    time_based_toll_row['car'] = row['distance'] * 0.8
                    time_based_toll_row['rv'] = row['distance'] * 0.8
                    time_based_toll_row['bus'] = row['distance'] * 0.8
                    time_based_toll_row['truck'] = row['distance'] * 0.8

                # Append the row to the list
                time_based_toll_rows.append(time_based_toll_row)

    # Create the time-based toll DataFrame
    time_based_toll_df = pd.DataFrame(time_based_toll_rows)

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
# Merge the DataFrames based on 'id_start'
result_df = pd.merge(unrolled_df, result_df, on='id_start')

final_result_df = calculate_time_based_toll_rates(result_df)
print(final_result_df)
