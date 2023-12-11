import pandas as pd
import datetime


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Create a pivot table to get distances between toll locations
    distance_pivot = pd.pivot_table(df, values='distance', index=['id_1', 'id_2'], aggfunc='sum').unstack(fill_value=0)

    # Create a symmetric matrix by adding the transposed matrix to the original
    distance_matrix = distance_pivot + distance_pivot.T

    # Set diagonal values to 0
    distance_matrix.values[(range(distance_matrix.shape[0]), range(distance_matrix.shape[0]))] = 0

    return distance_matrix

# Example usage with the DataFrame obtained from dataset-3.csv
# Replace 'data' with the actual variable name you used
data = pd.read_csv('dataset-3.csv')

# Generate the distance matrix using the function
result_matrix = calculate_distance_matrix(data)

# Display the result
print(result_matrix)




def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Reset index to make 'id_1' and 'id_2' regular columns
    distance_matrix_reset = distance_matrix.reset_index()

    # Melt the DataFrame to get 'id_start', 'id_end', and 'distance' columns
    unrolled_distance_matrix = pd.melt(distance_matrix_reset, id_vars='id_1', value_vars=distance_matrix_reset.columns[1:],
                                       var_name='id_end', value_name='distance')

    # Rename columns to match the specified names
    unrolled_distance_matrix.columns = ['id_start', 'id_end', 'distance']

    # Filter out rows where 'id_start' is the same as 'id_end'
    unrolled_distance_matrix = unrolled_distance_matrix[unrolled_distance_matrix['id_start'] != unrolled_distance_matrix['id_end']]

    # Reset index for the final result
    unrolled_distance_matrix.reset_index(drop=True, inplace=True)

    return unrolled_distance_matrix

# Example usage with the DataFrame obtained from Question 1
# Replace 'result_matrix' with the actual variable name you used
result_matrix = calculate_distance_matrix(data)

# Unroll the distance matrix using the function
unrolled_result = unroll_distance_matrix(result_matrix)

# Display the result
print(unrolled_result)




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
     # Filter rows where id_start is equal to the reference value
    reference_rows = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper bounds within 10% threshold
    lower_bound = reference_average_distance - (reference_average_distance * 0.1)
    upper_bound = reference_average_distance + (reference_average_distance * 0.1)

    # Filter rows within the 10% threshold
    within_threshold = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    # Get unique values from id_start column and sort the list
    result_ids = sorted(within_threshold['id_start'].unique().tolist())

    return result_ids

# Example usage with the DataFrame obtained from Question 2
# Replace 'unrolled_result' with the actual variable name you used
result_ids = find_ids_within_ten_percentage_threshold(unrolled_result, reference_value=123)

# Display the result
print(result_ids)



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
     # Create a copy of the input DataFrame to avoid modifying the original
    result_df = df.copy()

    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate in rate_coefficients.items():
        result_df[vehicle_type] = result_df['distance'] * rate

    return result_df

# Example usage with the DataFrame obtained from Question 2
# Replace 'unrolled_result' with the actual variable name you used
result_with_toll_rates = calculate_toll_rate(unrolled_result)

# Display the result
print(result_with_toll_rates)



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Create a copy of the input DataFrame to avoid modifying the original
    result_df = df.copy()

    # Define time ranges and discount factors for weekdays and weekends
    weekday_time_ranges = [(datetime.time(0, 0, 0), datetime.time(10, 0, 0)),
                           (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
                           (datetime.time(18, 0, 0), datetime.time(23, 59, 59))]

    weekend_time_range = (datetime.time(0, 0, 0), datetime.time(23, 59, 59))

    # Create new columns for start_day, start_time, end_day, and end_time
    result_df['start_day'] = result_df['startDay'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').strftime('%A'))
    result_df['end_day'] = result_df['endDay'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').strftime('%A'))
    result_df['start_time'] = result_df['startTime'].apply(lambda x: datetime.datetime.strptime(str(x), '%H%M%S').time())
    result_df['end_time'] = result_df['endTime'].apply(lambda x: datetime.datetime.strptime(str(x), '%H%M%S').time())

    # Apply discount factors based on time ranges
    for time_range in weekday_time_ranges:
        mask = (result_df['start_time'] >= time_range[0]) & (result_df['end_time'] <= time_range[1]) & (result_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        result_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8

    mask = (result_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
    for time_range in weekday_time_ranges:
        mask &= ~((result_df['start_time'] >= time_range[0]) & (result_df['end_time'] <= time_range[1]))
    result_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= 1.2

    mask = (result_df['start_time'] >= weekend_time_range[0]) & (result_df['end_time'] <= weekend_time_range[1]) & (result_df['start_day'].isin(['Saturday', 'Sunday']))
    result_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7

    return result_df[['id_start', 'id_end', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']]

# Example usage with the DataFrame obtained from Question 3
# Replace 'time_based_result' with the actual variable name you used
result_with_time_based_rates = calculate_time_based_toll_rates(time_based_result)

# Display the result
print(result_with_time_based_rates)
    
