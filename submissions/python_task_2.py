import pandas as pd
from datetime import time, timedelta


def calculate_distance_matrix(df):
    # Create an empty dictionary to store distances
    distances = {}

    # Iterate through the dataframe and populate the distances dictionary
    for _, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']

        # Add distance from id_start to id_end
        distances[(id_start, id_end)] = distance

        # Add distance from id_end to id_start (symmetric)
        distances[(id_end, id_start)] = distance

    # Get unique IDs and create a square matrix with zeros
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids, dtype=float)

    # Populate the distance matrix with cumulative distances
    for i in unique_ids:
        for j in unique_ids:
            if i != j:
                # Calculate cumulative distance from i to j
                distance_matrix.at[i, j] = distance_matrix.at[i, j] + distances.get((i, j), 0)
                distance_matrix.at[j, i] = distance_matrix.at[j, i] + distances.get((j, i), 0)

    return distance_matrix


# df = pd.read_csv('dataset-3.csv')
# result_df = calculate_distance_matrix(df)
# print(result_df)


def unroll_distance_matrix(df):
    # Create an empty list to store unrolled data
    unrolled_data = []

    # Iterate through the distance matrix and populate the unrolled_data list
    for i in df.index:
        for j in df.columns:
            if i != j:
                # Append data to the unrolled_data list
                unrolled_data.append({'id_start': i, 'id_end': j, 'distance': df.at[i, j]})

    # Create a DataFrame from the unrolled_data list
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df


# df = pd.read_csv('dataset-3.csv')
# result_df = calculate_distance_matrix(df)
# unrolled_result_df = unroll_distance_matrix(result_df)
# print(unrolled_result_df)


def find_ids_within_ten_percentage_threshold(df, reference_id):
    # Filter DataFrame to include only rows with the specified reference_id
    reference_rows = df[df['id_start'] == reference_id]

    # Check if the reference_id exists in the DataFrame
    if reference_rows.empty:
        raise ValueError(f"Reference ID {reference_id} not found in the DataFrame.")

    # Calculate the average distance for the reference_id
    reference_average_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper bounds for the threshold (10%)
    threshold_percentage = 0.10
    lower_bound = reference_average_distance * (1 - threshold_percentage)
    upper_bound = reference_average_distance * (1 + threshold_percentage)

    # Filter DataFrame to include only rows within the specified percentage threshold
    filtered_df = df[(df['id_start'] == reference_id) & (df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    return filtered_df

# reference_id = 1001400
# df = pd.read_csv('dataset-3.csv')
# result_df = calculate_distance_matrix(df)
# unrolled_result_df = unroll_distance_matrix(result_df)
# result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_result_df, reference_id)
# print(result_within_threshold)


def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate through rows and calculate toll rates for each vehicle type
    for index, row in df.iterrows():
        for vehicle_type, rate_coefficient in rate_coefficients.items():
            # Multiply the distance column by the rate coefficient for the current vehicle type
            df.at[index, vehicle_type] = row['distance'] * rate_coefficient

    return df


# df = pd.read_csv('dataset-3.csv')
# result_df = calculate_distance_matrix(df)
# unrolled_result_df = unroll_distance_matrix(result_df)
# result_with_toll_rate = calculate_toll_rate(unrolled_result_df)
# print(unrolled_result_df)
# print(result_with_toll_rate)


def calculate_time_based_toll_rates(df):
    # Define time intervals and discount factors
    weekday_time_intervals = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]

    weekend_discount_factor = 0.7

    # Function to calculate discounted toll rates
    def calculate_discounted_toll(row):
        for start_time, end_time, discount_factor in weekday_time_intervals:
            if start_time <= row['start_time'] <= end_time and start_time <= row['end_time'] <= end_time:
                return row['distance'] * discount_factor

        return row['distance'] * weekend_discount_factor

    # Apply the function to calculate discounted toll rates
    df['discounted_toll'] = df.apply(calculate_discounted_toll, axis=1)

    return df


# df = pd.read_csv('dataset-3.csv')
# result_df = calculate_distance_matrix(df)
# unrolled_result_df = unroll_distance_matrix(result_df)
# result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_result_df, 1001400)
# result_with_time_based_toll = calculate_time_based_toll_rates(result_within_threshold)
# print(result_with_time_based_toll)
