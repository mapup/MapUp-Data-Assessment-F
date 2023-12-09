import pandas as pd


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
    df = pd.pivot(df, index= 'id_1', columns='id_2', values='car')
    df.fillna(0, inplace=True)    

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

    df['car_type'] = df['car'].apply(lambda x: 'low' if x<= 15 else ('high' if x>25 else 'medium' ))
    car_type_counts = df['car_type'].value_counts().to_dict()
    sorted_dict = dict(sorted(car_type_counts.items()))

    return sorted_dict


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    mean = df['bus'].mean()
    list_index = df[df['bus'] > 2*mean].index.tolist()

    return list_index


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    average_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()
    sorted_routes = sorted(filtered_routes)

    return sorted_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    condition = matrix > 20
    matrix[condition] *= 0.75
    matrix[~condition] *= 1.25
    

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    return pd.Series()
