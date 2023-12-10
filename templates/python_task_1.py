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
    # Pivot the dataframe to create the matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    # Set diagonal values to 0
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
    # Create a new column 'car_type' based on conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Count occurrences for each car type and sort alphabetically
    type_count = df['car_type'].value_counts().sort_index().to_dict()

    return type_count


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_indexes = df[df['bus'] > 2 * df['bus'].mean()].index.tolist()

    return bus_indexes



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
      # Group by 'route' and filter based on average 'truck' values
    filtered_routes = df.groupby('route')['truck'].mean().loc[lambda x: x > 7].index.tolist()

    return filtered_routes

    return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
     # Apply custom multiplication based on conditions
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)

    return modified_matrix


def time_check(df: pd.DataFrame)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
        # Convert timestamp columns to datetime
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculate duration for each entry
    df['duration'] = df['end_datetime'] - df['start_datetime']

    # Group by ('id', 'id_2') and check time completeness
    time_completeness = df.groupby(['id', 'id_2']).apply(lambda group: group['duration'].sum() == pd.Timedelta(days=7)).droplevel(2)

    return time_completeness

    return pd.Series()
