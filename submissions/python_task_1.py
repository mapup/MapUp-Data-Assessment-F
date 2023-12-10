#QUESTION-1=Car Matrix Generation:

import os
import pandas as pd

def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.
    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_1', 'id_2', and 'car'.
    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot_table(values='car', index='id_1', columns='id_2', fill_value=0)

    for i in car_matrix.index:
        car_matrix.at[i, i] = 0

    return car_matrix

#QUESTION-2=Car Type Count Calculation:

import pandas as pd

def get_type_count(df: pd.DataFrame) -> dict:
    """
        Categorizes 'car' values into types and returns a dictionary of counts.

        Args:
            df (pandas.DataFrame)

        Returns:
            dict: A dictionary with car types as keys and their counts as values.
        """
    conditions = [(df['car'] <= 15), (df['car'] > 15) & (df['car'] <= 25), (df['car'] > 25)]
    car_types = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=car_types, right=False)
    type_count = df['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    return type_count


#QUESTION-3=Bus Count Index Retrieval:

import pandas as pd

def get_bus_indexes(df: pd.DataFrame) -> list:
    """
        Returns the indexes where the 'bus' values are greater than twice the mean.

        Args:
            df (pandas.DataFrame)

        Returns:
            list: List of indexes where 'bus' values exceed twice the mean.
        """
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()
    return bus_indexes



#QUESTION:4=Route Filtering:

import pandas as pd
"""
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """

def filter_routes(df: pd.DataFrame) -> list:
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes



#QUESTION:5=Matrix Value Modification:

import pandas as pd
"""
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """

def multiply_matrix(car_matrix: pd.DataFrame) -> pd.DataFrame:
    new_matrix = car_matrix.copy()  # Create a copy to avoid modifying the original DataFrame
    for column in new_matrix.columns:
        new_matrix[column] = new[column].apply(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    return new_matrix

#QUESTION:6=Time Check:

def time_check(df):
    """
     Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

     Args:
         df (pandas.DataFrame)

     Returns:
         pd.Series: return a boolean series
     """
    # Combining startDay and startTime into a single datetime column
    df['start_datetime'] = df['startDay'] + ' ' + df['startTime']

    # Combining endDay and endTime into a single datetime column
    df['end_datetime'] = df['endDay'] + ' ' + df['endTime']

    # Converting to datetime format
    df['start_datetime'] = pd.to_datetime(df['start_datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['end_datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # Checking if each (id, id_2) pair has incorrect timestamps
    result = df.groupby(['id', 'id_2']).apply(check_timestamps)

    return result
