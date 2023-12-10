import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
  """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Create a pivot table to represent distances between toll locations
    distance_matrix = df.pivot(index='from', columns='to', values='distance')

    # Ensure the matrix is symmetric by filling missing values
    distance_matrix = distance_matrix.fillna(0) + distance_matrix.fillna(0).T

    # Set diagonal values to 0
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    # Calculate cumulative distances along known routes
    for col in distance_matrix.columns:
        for row in distance_matrix.index:
            if distance_matrix.at[row, col] == 0:
                # Calculate cumulative distance only if the direct distance is not known
                intermediate_stops = distance_matrix.index.difference([row, col])
                cumulative_distance = distance_matrix.at[row, intermediate_stops].sum() + distance_matrix.at[intermediate_stops, col].sum()
                distance_matrix.at[row, col] = cumulative_distance

    return distance_matrix



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
   # Reset index to convert row labels (IDs) to columns
    distance_matrix = distance_matrix.reset_index()

    # Unroll the distance matrix to a DataFrame
    unrolled_df = pd.melt(distance_matrix, id_vars='index', var_name='id_end', value_name='distance')

    # Rename columns
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Exclude rows where id_start is equal to id_end
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    # Reset index
    unrolled_df = unrolled_df.reset_index(drop=True)

    return unrolled_df

# Example usage
# Assuming result_df is the DataFrame from Question 1
result_unrolled_df = unroll_distance_matrix(result_df)
print(result_unrolled_df)

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
    # Calculate the average distance for the reference value
    reference_average_distance = df[df['id_start'] == reference_value]['distance'].mean()

    # Calculate the lower and upper thresholds
    lower_threshold = reference_average_distance - 0.1 * reference_average_distance
    upper_threshold = reference_average_distance + 0.1 * reference_average_distance

    # Find values within the 10% threshold
    within_threshold_values = df[(df['id_start'] != reference_value) & 
                                 (df['distance'] >= lower_threshold) & 
                                 (df['distance'] <= upper_threshold)]['id_start'].unique()

    # Sort the list of values
    within_threshold_values = sorted(within_threshold_values)

    return within_threshold_values

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
     # Ensure that the input DataFrame has a 'distance' column
    if 'distance' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'distance' column.")

    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

  


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Ensure that the input DataFrame has 'start_time' and 'end_time' columns
    if 'start_time' not in df.columns or 'end_time' not in df.columns:
        raise ValueError("Input DataFrame must contain 'start_time' and 'end_time' columns.")

    # Define time ranges and discount factors for weekdays and weekends
    weekday_time_ranges = [(datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('10:00:00', '%H:%M:%S').time()),
                           (datetime.strptime('10:00:00', '%H:%M:%S').time(), datetime.strptime('18:00:00', '%H:%M:%S').time()),
                           (datetime.strptime('18:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time())]

    weekend_time_ranges = [(datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time())]

    # Create new columns for start_day, start_time, end_day, and end_time
    df['start_day'] = df['start_time'].apply(lambda x: x.strftime('%A'))
    df['end_day'] = df['end_time'].apply(lambda x: (x + timedelta(days=1)).strftime('%A'))

    # Initialize discount factors for weekdays and weekends
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    # Modify values of vehicle columns based on time ranges and discount factors
    for i, (start_range, end_range) in enumerate(weekday_time_ranges):
        mask = ((df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])) &
                (df['start_time'] >= start_range) & (df['end_time'] <= end_range))
        df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekday_discount_factors[i]

    for start_range, end_range in weekend_time_ranges:
        mask = ((df['start_day'].isin(['Saturday', 'Sunday'])) &
                (df['start_time'] >= start_range) & (df['end_time'] <= end_range))
        df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor

    return df
