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
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    # Initialize the matrix with 0s on the diagonal
    distance_matrix = distance_matrix.fillna(0)

    # Populate the matrix with cumulative distances
    for index, row in df.iterrows():
        start_id, end_id, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[start_id, end_id] += distance
        distance_matrix.at[end_id, start_id] += distance

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
    # Initialize an empty DataFrame to store unrolled distances
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through the upper triangular part of the distance matrix
    for i in range(len(distance_matrix.index)):
        for j in range(i+1, len(distance_matrix.columns)):
            id_start = distance_matrix.index[i]
            id_end = distance_matrix.columns[j]
            distance = distance_matrix.at[id_start, id_end]

            # Append the data to the unrolled DataFrame
            unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

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
    # Filter the DataFrame based on the reference_id
    reference_df = df[df['id_start'] == reference_id]

    # Check if the reference_df is not empty
    if reference_df.empty:
        print(f"No data found for reference value {reference_id}")
        return []

    # Print the reference_df to inspect its content
    print("Reference DataFrame:")
    print(reference_df)

    # Check if there are non-zero distances in the reference_df
    if (reference_df['distance'] == 0).all():
        print("All distances are zero in the reference_df.")
        return []

    # Calculate the average distance for the reference value
    average_distance = reference_df['distance'].mean()

    # Print the average_distance for debugging
    print(f"Average Distance for {reference_id}: {average_distance}")

    # Define the threshold range
    threshold_lower = 0.9 * average_distance
    threshold_upper = 1.1 * average_distance

    # Filter the DataFrame based on the threshold range
    filtered_df = df[(df['id_start'] != reference_id) & (df['distance'] >= threshold_lower) & (df['distance'] <= threshold_upper)]

    # Print the filtered_df for debugging
    print("Filtered DataFrame:")
    print(filtered_df)

    # Get the unique values from the id_start column and sort them
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
     # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create columns for each vehicle type with default values of 0.0
    for vehicle_type in rate_coefficients.keys():
        df[vehicle_type] = 0.0

    # Calculate toll rates for each vehicle type
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

    # Define discount factor for weekends
    weekend_discount_factor = 0.7

    # Create columns for start_day, start_time, end_day, and end_time
    df['start_day'] = ''
    df['start_time'] = pd.to_datetime('1900-01-01')
    df['end_day'] = ''
    df['end_time'] = pd.to_datetime('1900-01-01')

    # Calculate toll rates based on time intervals
    for index, row in df.iterrows():
        start_time = pd.to_datetime(row['start_time'])
        end_time = pd.to_datetime(row['end_time'])

        # Assign values for start_day, end_day, start_time, and end_time
        df.at[index, 'start_day'] = start_time.strftime('%A')
        df.at[index, 'end_day'] = end_time.strftime('%A')
        df.at[index, 'start_time'] = start_time.time()
        df.at[index, 'end_time'] = end_time.time()

        # Calculate toll rates based on time intervals and weekdays/weekends
        for interval_start, interval_end, discount_factor in time_intervals:
            if interval_start <= start_time.time() <= interval_end:
                df.at[index, 'distance'] *= discount_factor
                break

        if start_time.weekday() >= 5 or end_time.weekday() >= 5:  # Check if it's a weekend
            df.at[index, 'distance'] *= weekend_discount_factor

    return df