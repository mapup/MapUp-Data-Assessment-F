#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv("dataset-3.csv")


# In[2]:


df.head(10)


# # Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# ## The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A)

# In[6]:


import pandas as pd

def calculate_distance_matrix(file_path):
    # Read the dataset into a DataFrame
    df = pd.read_csv(file_path)

    # Create a dictionary to store cumulative distances
    distance_dict = {}

    # Iterate through rows in the DataFrame
    for index, row in df.iterrows():
        start_id = row['id_start']
        end_id = row['id_end']
        distance = row['distance']

        # Add the distance from start to end
        if start_id not in distance_dict:
            distance_dict[start_id] = {}
        distance_dict[start_id][end_id] = distance

        # Add the distance from end to start (symmetric)
        if end_id not in distance_dict:
            distance_dict[end_id] = {}
        distance_dict[end_id][start_id] = distance

    # Create a DataFrame from the dictionary
    distance_matrix_df = pd.DataFrame.from_dict(distance_dict, orient='index')

    # Fill missing values with 0 (for diagonal elements)
    distance_matrix_df = distance_matrix_df.fillna(0)

    # Cumulate distances along known routes
    distance_matrix_df = distance_matrix_df.cumsum(axis=1)

    return distance_matrix_df

# Example usage:
file_path = 'dataset-3.csv'
result_df = calculate_distance_matrix(file_path)
print(result_df)


# In[7]:


result_df.head()


# # Question 2: Unroll Distance Matrix
# ## Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# * All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[8]:


import pandas as pd

def unroll_distance_matrix(distance_matrix_df):
    # Initialize an empty list to store unrolled data
    unrolled_data = []

    # Iterate through rows in the distance matrix DataFrame
    for id_start, row in distance_matrix_df.iterrows():
        for id_end, distance in row.items():
            # Skip entries where id_start is equal to id_end
            if id_start != id_end:
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Example usage:
# Assuming result_df is the DataFrame from Question 1
result_df = calculate_distance_matrix('dataset-3.csv')
unrolled_result_df = unroll_distance_matrix(result_df)
print(unrolled_result_df)


# # Question 3: Finding IDs within Percentage Threshold
# ## Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# * Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[9]:


import pandas as pd

def find_ids_within_ten_percentage_threshold(unrolled_df, reference_value):
    # Filter rows where id_start is equal to the reference value
    reference_rows = unrolled_df[unrolled_df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_avg_distance = reference_rows['distance'].mean()

    # Calculate the threshold values (10% above and below the average)
    threshold_upper = reference_avg_distance * 1.1
    threshold_lower = reference_avg_distance * 0.9

    # Filter rows within the 10% threshold
    within_threshold_rows = unrolled_df[
        (unrolled_df['distance'] >= threshold_lower) & (unrolled_df['distance'] <= threshold_upper)
    ]

    # Get unique values from the id_start column and sort them
    result_ids = sorted(within_threshold_rows['id_start'].unique())

    return result_ids

# Example usage:
# Assuming unrolled_result_df is the DataFrame from Question 2
reference_value = 1001400  # Replace with the desired reference value
result_ids = find_ids_within_ten_percentage_threshold(unrolled_result_df, reference_value)
print(result_ids)


# # Question 4: Calculate Toll Rate
# ## Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# * The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for moto
# 
# 1.2 for car
# 
# 1.5 for rv
# 
# 2.2 for bus
# 
# 3.6 for truck

# In[10]:


import pandas as pd

def calculate_toll_rate(unrolled_df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate through rate coefficients and calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'
        unrolled_df[column_name] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df

# Example usage:
# Assuming unrolled_result_df is the DataFrame from Question 2
result_with_toll_df = calculate_toll_rate(unrolled_result_df)
print(result_with_toll_df)


# In[11]:


result_with_toll_df.head()


# # Question 5: Calculate Time-Based Toll Rates
# ## Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# * The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[19]:


import pandas as pd
from datetime import time

def calculate_time_based_toll_rates(unrolled_df):
    # Define time ranges and corresponding discount factors
    time_ranges_weekday = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    time_ranges_weekend = [(time(0, 0, 0), time(23, 59, 59))]

    discount_factors_weekday = [0.8, 1.2, 0.8]
    discount_factor_weekend = 0.7

    # Create new columns for start_day, start_time, end_day, and end_time
    unrolled_df['start_day'] = 'Monday'
    unrolled_df['end_day'] = 'Sunday'
    unrolled_df['start_time'] = time(0, 0, 0)
    unrolled_df['end_time'] = time(23, 59, 59)

    # Apply discount factors based on time ranges
    for i, (start_time, end_time) in enumerate(time_ranges_weekday):
        weekday_condition = (unrolled_df['start_time'] >= start_time) & (unrolled_df['end_time'] <= end_time)
        unrolled_df.loc[weekday_condition, ['start_time', 'end_time']] = [start_time, end_time]

        # Make sure the columns exist before multiplying
        vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
        if set(vehicle_columns).issubset(unrolled_df.columns):
            unrolled_df.loc[weekday_condition, vehicle_columns] *= discount_factors_weekday[i]

    for start_time, end_time in time_ranges_weekend:
        weekend_condition = (unrolled_df['start_time'] >= start_time) & (unrolled_df['end_time'] <= end_time)
        unrolled_df.loc[weekend_condition, ['start_time', 'end_time']] = [start_time, end_time]

        # Make sure the columns exist before multiplying
        if set(vehicle_columns).issubset(unrolled_df.columns):
            unrolled_df.loc[weekend_condition, vehicle_columns] *= discount_factor_weekend

    return unrolled_df

# Example usage:
# Assuming unrolled_result_df is the DataFrame from Question 3
result_with_time_based_toll_df = calculate_time_based_toll_rates(unrolled_result_df)
print(result_with_time_based_toll_df)


# In[20]:


result_with_time_based_toll_df.head()

