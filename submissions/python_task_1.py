import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:

    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """

    # Write your logic here

    id_1 = df['id_1'].unique()
    id_2 = df['id_2'].unique()
    matrix = [[0 for _ in range(len(id_2))] for _ in range(len(id_1))]

    for index, row in df.iterrows():
        row_index = list(id_1).index(row['id_1'])
        col_index = list(id_2).index(row['id_2'])
        matrix[row_index][col_index] = row['car']

    df = pd.DataFrame(matrix, index=id_1, columns=id_2)
    np.fill_diagonal(df.values, 0)
    return df

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """

    # Write your logic here

    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, float('Inf')], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts()
    type_dict = dict(sorted(type_count.items()))

    return type_dict



def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    bus_mean = df['bus'].mean()
    bus_filter = df[df['bus'] > 2 * bus_mean]
    bus_index = list(bus_filter.index)
    bus_index.sort()
    return bus_index


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    groupby_route = df.groupby('route')['truck'].mean()
    filter_truck = groupby_route[groupby_route > 7]
    filter_route = list(filter_truck.index)
    filter_route.sort()
    return filter_route


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    df = matrix.copy()

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i,j] > 20:
                df.iloc[i,j] = df.iloc[i,j] * 0.75
            else:
                df.iloc[i,j] = df.iloc[i,j] * 1.25

    return df



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    df['startDay'] = pd.to_datetime(df['startDay'], format='%A')
    df['endDay'] = pd.to_datetime(df['endDay'],format='%A')
    df = df.set_index(['id', 'id_2'])
    results = []
    for pair in df.index.unique():
        subset = df.loc[pair]
        full_day = (subset['startTime'].min() == '00:00:00') and (subset['endTime'].max() == '23:59:59')
        full_week = (subset['startDay'].nunique() == 7) and (subset['endDay'].nunique() == 7)
        results.append(not (full_day and full_week))
    boolean_series = pd.Series(results, index=df.index.unique())

    return boolean_series

