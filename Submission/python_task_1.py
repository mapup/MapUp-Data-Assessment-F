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
    #Setting the diagonal values to zero
    for i in car_matrix.index:
        car_matrix.at[i, i] = 0

    return car_matrix

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.
    Args:
        df (pandas.DataFrame)
    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    categorize_car = lambda x: 'low' if x <= 15 else ('medium' if x <= 25 else 'high')

    # Lambda function to create the 'car_type' column
    df['car_type'] = df['car'].apply(categorize_car)

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.
    Args:
        df (pandas.DataFrame)
    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_of_bus = df['bus'].mean()
    bus_indexes = df.loc[df['bus'] > 2 * mean_of_bus].index.tolist()
    sorted_bus_indexes = sorted(bus_indexes)
    return sorted_bus_indexes

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.
    Args:
        df (pandas.DataFrame)
    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filtering routes where the average 'truck' values are greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sorting the list of route names in ascending order
    sorted_filtered_routes = sorted(filtered_routes)

    return sorted_filtered_routes

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.
    Args:
        matrix (pandas.DataFrame)
    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Using applymap along with lambda to apply the condition.
    modified_matrix = matrix.applymap(lambda x : x *0.75 if x > 20 else x * 1.25)
    # Rounding off the values to 1
    modified_matrix = modified_matrix.round(1)
    return modified_matrix

def time_check(df):
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

def check_timestamps(group):
    # Checking if the timestamps cover a full 24-hour period
    full_24_hours = (group['end_datetime'].max() - group['start_datetime'].min()) >= pd.Timedelta(days=1)

    # Checking if the timestamps span all 7 days of the week
    days_covered = group['start_datetime'].dt.dayofweek.nunique() == 7

    return pd.Series(full_24_hours and days_covered, index=[(group['id'].iloc[0], group['id_2'].iloc[0])])