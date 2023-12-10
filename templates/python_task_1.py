# -*- coding: utf-8 -*-
"""Python_Task1.ipynb

Question 1: Car Matrix Generation
Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:

values from id_2 as columns
values from id_1 as index
dataframe should have values from car column
diagonal values should be 0.
"""

import pandas as pd
import numpy as np

def generate_car_matrix(dataset_path):
    # Load the dataset into a DataFrame
    df = pd.read_csv(dataset_path)

    # Create a pivot table using id_1 as index, id_2 as columns, and car as values
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix

# Example usage
dataset_path = 'dataset-1.csv'
result_matrix = generate_car_matrix(dataset_path)
print(result_matrix)

"""Question 2: Car Type Count Calculation
Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:

low for values less than or equal to 15,
medium for values greater than 15 and less than or equal to 25,
high for values greater than 25.
Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.
"""

import pandas as pd
import numpy as np

def get_type_count(df):
    # Add a new categorical column 'car_type' based on values of the 'car' column
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default=np.nan), dtype="category")

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

    return type_counts

# Example usage
dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = get_type_count(df)
print(result)

"""Question 3: Bus Count Index Retrieval
Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.
"""

import pandas as pd

def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Example usage
dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = get_bus_indexes(df)
print(result)

"""Question 4: Route Filtering
Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.
"""

import pandas as pd

def filter_routes(df):
    # Group by 'route' and calculate the average of the 'truck' column
    avg_truck_per_route = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Example usage
dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = filter_routes(df)
print(result)

"""Question 5: Matrix Value Modification
Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:

If a value in the DataFrame is greater than 20, multiply those values by 0.75,
If a value is 20 or less, multiply those values by 1.25.
The function should return the modified DataFrame which has values rounded to 1 decimal place.
"""

import pandas as pd
import numpy as np

def generate_car_matrix(dataset_path):
    # Load the dataset into a DataFrame
    df = pd.read_csv(dataset_path)

    # Create a pivot table using id_1 as index, id_2 as columns, and car as values
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix

# Example usage
dataset_path = 'dataset-1.csv'
result_matrix = generate_car_matrix(dataset_path)
print(result_matrix)

"""Question 6: Time Check
You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).
"""

import pandas as pd
import numpy as np

def check_time_completeness(df):
    # Combine 'startDay' and 'startTime' columns to create a new 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')

    # Combine 'endDay' and 'endTime' columns to create a new 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    # Drop rows with invalid or out-of-bounds timestamps
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])

    # Group by (id, id_2) and check for each pair if timestamps are within the expected range
    completeness_check = (
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.time != pd.Timestamp('00:00:00').time()) |
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.time != pd.Timestamp('23:59:59').time()) |
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.dayofweek != 0) |  # Check if Monday
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.dayofweek != 6)  # Check if Sunday
    )

    return completeness_check

# Example usage
dataset_path = 'dataset-2.csv'
df = pd.read_csv(dataset_path)
result = check_time_completeness(df)
print(result)
