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
    distance_matrix = df.pivot_table(index='toll_booth_A', columns='toll_booth_B', values='distance', aggfunc='sum', fill_value=0)
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)

    return distance_matrix

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    columns = distance_matrix.columns
    index = distance_matrix.index
    combinations = [(start, end) for start in index for end in columns]
    id_start_list = []
    id_end_list = []
    distance_list = []
    for start, end in combinations:
        if start != end:
             id_start_list.append(start)
             id_end_list.append(end)
             distance_list.append(distance_matrix.loc[start, end])
    unrolled_df = pd.DataFrame({'id_start': id_start_list, 'id_end': id_end_list, 'distance': distance_list})

    return unrolled_df

    return df


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
    reference_avg_distance = unrolled_df.loc[unrolled_df['id_start'] == reference_value, 'distance'].mean()
    threshold_range = 0.1 * reference_avg_distance
    within_threshold_ids = unrolled_df[
        (unrolled_df['id_start'] != reference_value) &
        (unrolled_df['distance'] >= (reference_avg_distance - threshold_range)) &
        (unrolled_df['distance'] <= (reference_avg_distance + threshold_range))
    ]['id_start'].unique()

    # Sort and return the list of IDs within the threshold
    sorted_within_threshold_ids = sorted(within_threshold_ids)

    return sorted_within_threshold_ids

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        unrolled_df[vehicle_type] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df

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
    time_ranges_weekdays = [(pd.to_datetime('00:00:00').time(), pd.to_datetime('10:00:00').time()),
                            (pd.to_datetime('10:00:00').time(), pd.to_datetime('18:00:00').time()),
                            (pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time())]

    time_ranges_weekends = [(pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time())]

    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7
    unrolled_df[['start_day', 'start_time']] = unrolled_df['id_start'].str.split('_', expand=True)
    unrolled_df[['end_day', 'end_time']] = unrolled_df['id_end'].str.split('_', expand=True)

    # Convert start_time and end_time columns to datetime.time type
    unrolled_df['start_time'] = pd.to_datetime(unrolled_df['start_time']).dt.time
    unrolled_df['end_time'] = pd.to_datetime(unrolled_df['end_time']).dt.time

    # Calculate time-based toll rates
    for idx, row in unrolled_df.iterrows():
        time_range = (row['start_time'], row['end_time'])

        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            discount_factor = discount_factors_weekdays[time_ranges_weekdays.index(time_range)]
        else:
            discount_factor = discount_factor_weekends

        # Update vehicle columns based on the time range and discount factor
        for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
            unrolled_df.at[idx, vehicle_type] *= discount_factor

    return unrolled_df

    return df
