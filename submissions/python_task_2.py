import numpy as np
import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here

    ids = []
    ids.extend(list(df['id_start']))
    ids.extend(list(df['id_end']))
    ids = set(ids)
    ids = list(ids)
    ids.sort()
    ids1 =ids
    ids = pd.Series(ids)
    matrix = [[0 for _ in range(len(ids))] for _ in range(len(ids))]

    for index, row in df.iterrows():
        row_index = list(ids).index(row['id_start'])
        col_index = list(ids).index(row['id_end'])
        matrix[row_index][col_index] = row['distance']
        matrix[col_index][row_index] = row['distance']


    distance_matrix = pd.DataFrame(matrix, index=ids, columns=ids)

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if distance_matrix.iloc[i, j] == 0:
                non_zero = distance_matrix.iloc[i, :].replace(0, np.nan).dropna()
                if len(non_zero) > 0:
                    distance_matrix.iloc[i, j] = non_zero.values[0] + distance_matrix.iloc[ids1.index(non_zero.index[0]), j]
                    distance_matrix.iloc[j, i] = distance_matrix.iloc[i, j]



    return distance_matrix

data = pd.read_csv("./datasets/dataset-3.csv")
# print(data)
# calculate_distance_matrix(data)
def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    rates = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle, rate in rates.items():
        # Calculate the toll rate by multiplying the distance with the rate coefficient
        df[vehicle] = df['distance'] * rate
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
