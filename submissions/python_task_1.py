import pandas as pd

def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    pd.DataFrame(np.fill_diagonal(car_matrix.values, 0), index=car_matrix.index, columns=car_matrix.columns)
    return car_matrix

def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_counts = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_counts.items()))

def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.sort_values().tolist()
    return bus_indexes

def filter_routes(df: pd.DataFrame) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.sort_values().tolist()
    return filtered_routes

def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    return modified_matrix

def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    full_day_coverage = df.groupby(['id', 'id_2'])['start_timestamp', 'end_timestamp'].apply(check_full_day_coverage)
    
    return full_day_coverage

def check_full_day_coverage(group):
    # Check if timestamps cover a full 24-hour period and span all 7 days of the week
    start_date = group['start_timestamp'].dt.date.min()
    end_date = group['end_timestamp'].dt.date.max()
    return pd.Series({'full_day_coverage': pd.date_range(start=start_date, end=end_date, freq='D').isin(group['start_timestamp'].dt.date.unique()).all()})
