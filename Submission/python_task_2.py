import pandas as pd
from datetime import datetime, time, timedelta 
from itertools import combinations
def calculate_distance_matrix(df)->pd.DataFrame():
   
    # Write your logic here
    # Get unique id_1 and id_2 values
    unique_id_1 = df['id_1'].unique()
    unique_id_2 = df['id_2'].unique()

    # Create an empty matrix with rows and columns based on unique id values
    df = pd.DataFrame(index=unique_id_1, columns=unique_id_2)

    # Fill the matrix with 'car' values from the DataFrame
    for _, row in df.iterrows():
      df.at[row['id_1'], row['id_2']] = row['car']

    # Fill diagonal values with 0
    df.values[[range(len(df))]*2] = 0

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
  
    # Write your logic here
    # Create a DataFrame to store the unrolled distance matrix
    input_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through the rows of the car_matrix
    for idx_start, row in car_matrix.iterrows():
        for idx_end, distance in row.items():
            if idx_start != idx_end:  # Exclude same id_start and id_end
                unrolled_df = unrolled_df.append({'id_start': idx_start, 'id_end': idx_end, 'distance': distance}, ignore_index=True)

    return unrolled_df

# Assuming result_matrix is the DataFrame generated from the previous question
result_df = unroll_distance_matrix(result_matrix)



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
  
    # Write your logic here
    # Initialize an empty list to store the unrolled data
    unrolled_data = []

    # Iterate through unique pairs of id_start and id_end
    for start, end in combinations(input_df['id'].unique(), 2):
        # Select the corresponding distances
        distance = input_df.loc[(input_df['id'] == start) & (input_df['id_end'] == end), 'distance'].values

        # Check if the combination exists
        if len(distance) > 0:
            # Append the data to the unrolled list
            unrolled_data.append({'id_start': start, 'id_end': end, 'distance': distance[0]})

    # Create a new DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)
    return df


def calculate_toll_rate(df)->pd.DataFrame():
   
    # Wrie your logic here
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Add columns for toll rates based on vehicle types
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    
    # Write your logic here
    # Define time ranges and discount factors
    time_ranges = [
        {'start_time': time(0, 0, 0), 'end_time': time(10, 0, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start_time': time(10, 0, 0), 'end_time': time(18, 0, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start_time': time(18, 0, 0), 'end_time': time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    # Initialize empty lists to store the calculated start_day, start_time, end_day, and end_time
    start_days, start_times, end_days, end_times = [], [], [], []

    # Iterate through each time range
    for time_range in time_ranges:
        # Extract information from the time range
        start_time, end_time = time_range['start_time'], time_range['end_time']
        weekday_factor, weekend_factor = time_range['weekday_factor'], time_range['weekend_factor']

        # Iterate through each day of the week
        for day in range(7):
            # Calculate start and end datetime for the current day and time range
            start_datetime = datetime.combine(datetime(2023, 1, 1), start_time) + timedelta(days=day)
            end_datetime = datetime.combine(datetime(2023, 1, 1), end_time) + timedelta(days=day)

            # Append values to the lists
            start_days.append(start_datetime.strftime('%A'))
            start_times.append(start_datetime.time())
            end_days.append(end_datetime.strftime('%A'))
            end_times.append(end_datetime.time())

    # Add new columns to the DataFrame
    df['start_day'], df['start_time'], df['end_day'], df['end_time'] = start_days, start_times, end_days, end_times

    # Modify vehicle columns based on time ranges and factors
    for time_range in time_ranges:
        weekday_factor, weekend_factor = time_range['weekday_factor'], time_range['weekend_factor']

        # Apply discounts to vehicle columns based on time ranges and factors
        df.loc[(df['start_time'] >= time_range['start_time']) & (df['end_time'] <= time_range['end_time']) &
               (df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])), ['moto', 'car', 'rv', 'bus', 'truck']] *= weekday_factor

        df.loc[(df['start_time'] >= time_range['start_time']) & (df['end_time'] <= time_range['end_time']) &
               (df['start_day'].isin(['Saturday', 'Sunday'])), ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_factor
    return df
