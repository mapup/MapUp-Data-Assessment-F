import pandas as pd
import numpy as np

def generate_car_matrix(df_path: str) -> pd.DataFrame:
    """
    Generate a matrix based on the 'car' values in the input DataFrame.

    Args:
    - df_path (str): Path to the input CSV file.

    Returns:
    - pd.DataFrame: Matrix where rows and columns correspond to 'id_1' and 'id_2', values are 'car' values.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(df_path)
    
    # Pivot the DataFrame to create a matrix with 'id_1' as index, 'id_2' as columns, and 'car' as values
    df_matrix = df.pivot(index="id_1", columns="id_2", values="car")
    
    # Fill diagonal elements with 0
    np.fill_diagonal(df_matrix.values, 0)

    return df_matrix


def get_type_count(df: pd.DataFrame) -> dict:
    """
    Count the occurrences of car types ('low', 'medium', 'high') based on 'car' values.

    Args:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    - dict: Dictionary containing the count of each car type.
    """
    # Create a new column 'car_type' based on 'car' values
    df['car_type'] = df['car'].apply(lambda x: 'low' if x <= 15 else 'medium' if x <= 25 else 'high')
    
    # Group by 'car_type' and count occurrences, then sort the dictionary
    type_count = df.groupby('car_type')['car_type'].count()
    type_count = dict(type_count)
    type_count = dict(sorted(type_count.items()))

    return type_count


def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Get the sorted list of indexes where 'bus' values are greater than twice the mean value.

    Args:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    - list: Sorted list of indexes.
    """
    # Calculate the mean value of 'bus' column
    mean_value = df['bus'].mean()
    
    # Get the indexes where 'bus' values are greater than 2 times the mean value
    index_list = df[df['bus'] > 2 * mean_value].index.tolist()
    
    # Sort the index list
    sorted_index_list = sorted(index_list)

    return sorted_index_list


def filter_routes(df: pd.DataFrame) -> list:
    """
    Filter and get the sorted list of routes where the mean 'truck' value is greater than 7.

    Args:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    - list: Sorted list of routes.
    """
    # Group by 'route' and calculate the mean 'truck' value for each route
    grouped_df = df.groupby('route')['truck'].mean()
    
    # Filter routes where the mean 'truck' value is greater than 7
    filtered_routes = grouped_df[grouped_df > 7]
    
    # Get the sorted list of routes
    return sorted(filtered_routes.index.tolist())


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiply matrix values by 0.75 if they are greater than 20, otherwise multiply by 1.25.

    Args:
    - matrix (pd.DataFrame): Input matrix.

    Returns:
    - pd.DataFrame: Transformed matrix.
    """
    # Apply a function to each element of the matrix
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    return matrix


def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Check if time conditions are met for each group in the DataFrame.

    Args:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    - pd.Series: Series of boolean values indicating whether time conditions are met for each group.
    """
    # Convert 'startTime' and 'endTime' columns to time format
    df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M:%S').dt.time
    df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M:%S').dt.time
    
    # Group by 'id' and 'id_2'
    grouped = df.groupby(['id', 'id_2'])

    # Initialize an empty Series to store boolean results
    results = pd.Series(dtype=bool)

    # Iterate through groups and check time conditions
    for name, group in grouped:
        if (group['startTime'].min() <= pd.to_datetime('00:00:00', format='%H:%M:%S').time() and
            group['endTime'].max() >= pd.to_datetime('23:59:59', format='%H:%M:%S').time() and
            set(group['startDay']).union(set(group['endDay'])) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])):
            results[name] = False
        else:
            results[name] = True

    return results
