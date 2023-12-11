import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df = pd.read_csv(r'C:\Users\Ritesh Mishra\Desktop\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv')

    # Create an empty DataFrame for the distance matrix
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)
    distance_matrix = distance_matrix.fillna(0)

    # Fill in the distances in the matrix
    for index, row in df.iterrows():
        start, end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance  # Ensure symmetry

    # Update the matrix with cumulative distances along known routes
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                    # If distances between toll locations A to B and B to C are known,
                    # then the distance from A to C should be the sum of these distances.
                    if distance_matrix.at[i, j] == 0 or distance_matrix.at[i, j] > distance_matrix.at[i, k] + distance_matrix.at[k, j]:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

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
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through the input matrix to extract distances and create rows
    for i in input_matrix.index:
        for j in input_matrix.columns:
            if i != j and input_matrix.at[i, j] != 0:
                unrolled_df = unrolled_df.append({'id_start': i, 'id_end': j, 'distance': input_matrix.at[i, j]}, ignore_index=True)

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
    df3=pd.read_csv(r'C:\Users\Ritesh Mishra\Desktop\MapUp-Data-Assessment-F-main\datasets\dataset-3.csv')
    ref_avg = df3[df3['id_start'] == ref_value]['distance'].mean()

    # Calculate the 10% threshold
    threshold = 0.1 * ref_avg

    # Find 'id_start' values within the threshold
    ids_within_threshold = df3[(df3['distance'] >= ref_avg - threshold) & (df3['distance'] <= ref_avg + threshold)]['id_start'].unique()

    # Sort the list
    ids_within_threshold.sort()

    return df3


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
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
        }

    # Create new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df3[vehicle_type] = df3['distance'] * rate_coefficient


    return df3


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
        {"start": time(0, 0, 0), "end": time(10, 0, 0), "factor": 0.8},
        {"start": time(10, 0, 0), "end": time(18, 0, 0), "factor": 1.2},
        {"start": time(18, 0, 0), "end": time(23, 59, 59), "factor": 0.8}
    ]
    
    weekend_factor = 0.7
    
    # Create a copy of the input DataFrame to avoid modifying the original data
    result_df = input_df.copy()

    # Iterate over unique (id_start, id_end) pairs
    for _, row in result_df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        
        # Iterate over days of the week
        for day in range(7):
            # Determine the day name (Monday to Sunday) for start_day and end_day
            start_day = (datetime.strptime(row['date'], '%Y-%m-%d') + timedelta(days=day)).strftime('%A')
            end_day = (datetime.strptime(row['date'], '%Y-%m-%d') + timedelta(days=day + 1)).strftime('%A')

            # Iterate over time intervals
            for interval in time_intervals:
                start_time = datetime.combine(datetime.min, interval["start"])
                end_time = datetime.combine(datetime.min, interval["end"])

                # Apply discount factor based on the time interval and day
                if day < 5:  # Weekdays (Monday - Friday)
                    discount_factor = interval["factor"]
                else:  # Weekends (Saturday and Sunday)
                    discount_factor = weekend_factor

                # Update toll rates for the specific time interval and day
                mask = (result_df['id_start'] == id_start) & (result_df['id_end'] == id_end) & \
                       (result_df['date'] == row['date']) & \
                       (result_df['timestamp'] >= start_time) & (result_df['timestamp'] <= end_time)

                result_df.loc[mask, ['vehicle_1', 'vehicle_2', 'vehicle_3']] *= discount_factor

    # Add start_day, start_time, end_day, and end_time columns
    result_df['start_day'] = result_df['timestamp'].dt.strftime('%A')
    result_df['start_time'] = result_df['timestamp'].dt.time
    result_df['end_day'] = (result_df['timestamp'] + timedelta(seconds=1)).dt.strftime('%A')
    result_df['end_time'] = (result_df['timestamp'] + timedelta(days=1) - timedelta(seconds=1)).dt.time


    return df
