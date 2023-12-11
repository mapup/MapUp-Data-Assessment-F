import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():


    # Pivot the DataFrame to create a matrix with 'Source' as index, 'Destination' as columns, and 'Distance' as values
    distance_matrix = df.pivot(index='Source', columns='Destination', values='Distance').fillna(0)

    # Make the matrix symmetric by adding its transpose to itself
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)

    # Set diagonal values to 0
    distance_matrix.values[[range(len(distance_matrix))] * 2] = 0

    # Calculate cumulative distances along known routes
    distance_matrix = distance_matrix.cumsum(axis=1)

    return distance_matrix



def unroll_distance_matrix(df)->pd.DataFrame():


    source_locations = df.index
    destination_locations = df.columns

    # Initialize lists to store the unrolled data
    id_start_list = []
    id_end_list = []
    distance_list = []

    # Iterate over each combination of source and destination
    for source in source_locations:
        for destination in destination_locations:
            # Check if source and destination are not the same
            if source != destination:
                # Append data to lists
                id_start_list.append(source)
                id_end_list.append(destination)
                distance_list.append(df.loc[source, destination])

    # Create the unrolled DataFrame
    unrolled_df = pd.DataFrame({'id_start': id_start_list, 'id_end': id_end_list, 'distance': distance_list})

    return unrolled_df




def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():


    # Filter rows where id_start is the reference_id
    reference_df = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_df['distance'].mean()

    # Calculate the lower and upper bounds for the 10% threshold
    lower_bound = reference_avg_distance - 0.1 * reference_avg_distance
    upper_bound = reference_avg_distance + 0.1 * reference_avg_distance

    # Filter rows where average distance is within the 10% threshold
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= lower_bound) & (result_df['distance'] <= upper_bound)]

    # Sort the result DataFrame by id_start
    result_df = result_df.sort_values(by='id_start')

    return result_df



def calculate_toll_rate(df)->pd.DataFrame():


    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'
        df[column_name] = df['distance'] * rate_coefficient

    return df



def calculate_time_based_toll_rates(df)->pd.DataFrame():

    time_ranges_weekdays = [
        {'start': time(0, 0, 0), 'end': time(10, 0, 0), 'discount_factor': 0.8},
        {'start': time(10, 0, 0), 'end': time(18, 0, 0), 'discount_factor': 1.2},
        {'start': time(18, 0, 0), 'end': time(23, 59, 59), 'discount_factor': 0.8}
    ]

    time_ranges_weekends = [
        {'start': time(0, 0, 0), 'end': time(23, 59, 59), 'discount_factor': 0.7}
    ]

    # Create new columns for start_day, start_time, end_day, end_time
    df['start_day'] = df['end_day'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['start_time'] = time(0, 0, 0)
    df['end_time'] = time(23, 59, 59)

    # Apply discount factors based on time ranges
    for time_range in time_ranges_weekdays:
        mask = (df['start_time'] >= time_range['start']) & (df['end_time'] <= time_range['end'])
        for column in ['moto_toll', 'car_toll', 'rv_toll', 'bus_toll', 'truck_toll']:
            df.loc[mask, column] *= time_range['discount_factor']

    for time_range in time_ranges_weekends:
        mask = (df['start_time'] >= time_range['start']) & (df['end_time'] <= time_range['end'])
        for column in ['moto_toll', 'car_toll', 'rv_toll', 'bus_toll', 'truck_toll']:
            df.loc[mask, column] *= time_range['discount_factor']

    return df


dataset_path = pd.read_csv("..\datasets\dataset-3.csv")

# Load the dataset
dataset = pd.read_csv(dataset_path)

# Step 1: Calculate distance matrix
distance_matrix = calculate_distance_matrix(dataset)
print("Distance Matrix:")
print(distance_matrix)
print()

# Step 2: Unroll distance matrix
unrolled_df = unroll_distance_matrix(distance_matrix)
print("Unrolled DataFrame:")
print(unrolled_df)
print()

# Step 3: Find IDs within a ten percentage threshold
reference_id = 1  # Replace with the desired reference ID
within_threshold_df = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print("IDs within 10% threshold of reference ID:")
print(within_threshold_df)
print()

# Step 4: Calculate toll rates
toll_rate_df = calculate_toll_rate(within_threshold_df)
print("Toll Rates DataFrame:")
print(toll_rate_df)
print()

# Step 5: Calculate time-based toll rates
time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rate_df)
print("Time-based Toll Rates DataFrame:")
print(time_based_toll_rates_df)