import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:
  
    #Read the CSV file into a DataFrame
    df = pd.read_csv('datasets/dataset-1.csv')

    # Pivot the DataFrame
    df = df.pivot(index='id_1', columns='id_2', values='car')

    # Replace diagonal values with 0
    np.fill_diagonal(df.values, 0)

    return df


def get_type_count(df)->dict:
   
    # Write your logic here
    # Create the car_type column
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Calculate occurrences and sort the dictionary
    type_count = df['car_type'].value_counts().to_dict()
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count
    return dict()


def get_bus_indexes(df)->list:
   
    # Write your logic here
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indices = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indices.sort()
    return list()


def filter_routes(df)->list:
  
    # Write your logic here
    # Group by 'route' and calculate the mean of 'truck' values
    avg_truck_values = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    selected_routes = avg_truck_values[avg_truck_values > 25].index.tolist()

    # Sort the list of routes
    selected_routes.sort()

    return selected_routes
    return list()


def multiply_matrix(matrix)->pd.DataFrame:
   
    # Write your logic here
    # Multiply values greater than 20 by 0.75
    matrix[matrix > 20] *= 0.75

    # Multiply values 20 or less by 1.25
    matrix[matrix <= 20] *= 1.25

    # Round values to 1 decimal place
    matrix = matrix.round(1)
    return matrix


def time_check(df)->pd.Series:
   
    # Write your logic here
    # Convert timestamp column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by id and id_2
    grouped = df.groupby(['id', 'id_2'])

    # Check completeness for each group
    completeness_check = grouped.apply(lambda group: (
        group['timestamp'].min().time() == pd.Timestamp('00:00:00').time() and
        group['timestamp'].max().time() == pd.Timestamp('23:59:59').time() and
        set(group['timestamp'].dt.dayofweek) == set(range(7))
    ))
    return pd.Series()
