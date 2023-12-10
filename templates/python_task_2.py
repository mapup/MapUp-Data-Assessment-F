from datetime import time


def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): Input dataframe with columns 'id_start', 'id_end', 'distance'.

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Create a pivot table to calculate cumulative distances along known routes
    distance_matrix = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='sum', fill_value=0)

    # Make the matrix symmetric
    distance_matrix = distance_matrix + distance_matrix.T - np.diag(distance_matrix.values.diagonal())

    return distance_matrix


def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Input distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Reset index to convert the matrix to a long format
    unrolled_df = df.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Remove rows where id_start is equal to id_end
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): Input unrolled distance matrix.
        reference_id (int): Reference ID for calculating the average distance.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Calculate the average distance for the reference ID
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    # Find IDs within 10% threshold
    threshold_min = 0.9 * reference_avg_distance
    threshold_max = 1.1 * reference_avg_distance

    result_df = df[(df['distance'] >= threshold_min) & (df['distance'] <= threshold_max)].copy()

    return result_df


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame): Input unrolled distance matrix.

    Returns:
        pandas.DataFrame: Updated DataFrame with added columns 'moto', 'car', 'rv', 'bus', 'truck'.
    """
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df


def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): Input dataframe with columns 'id_start', 'id_end', 'distance', 'start_time', 'end_time', 'start_day', 'end_day'.

    Returns:
        pandas.DataFrame: Updated DataFrame with added columns 'start_day', 'start_time', 'end_day', 'end_time'.
    """
    # Define time ranges and discount factors
    time_ranges = [
        {'start': time(0, 0, 0), 'end': time(10, 0, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start': time(10, 0, 0), 'end': time(18, 0, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start': time(18, 0, 0), 'end': time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    # Apply discount factors based on time ranges and weekdays/weekends
    for time_range in time_ranges:
        mask = (df['start_time'] >= time_range['start']) & (df['end_time'] <= time_range['end'])
        df.loc[mask & ~df['start_day'].isin(['Saturday', 'Sunday']), 'distance'] *= time_range['weekday_factor']
        df.loc[mask & df['start_day'].isin(['Saturday', 'Sunday']), 'distance'] *= time_range['weekend_factor']

    return df
