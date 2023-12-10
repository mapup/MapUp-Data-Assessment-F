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
    result_df = df.pivot(index='id_1', columns= 'id_2', value='car')

    result_df = result_df.fillna(0)
    result_df.values[[range(len(result_df))]*2] = 0.0

    return result_df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'),15, 25, float('inf')], labels=['low','medium','high'])
    type_counts = df['car_type'].values_counts().to_dict()
    return type_counts


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
    get_bus_indexes = df[df['bus']>2*bus_mean].index.tolist()

    return get_bus_indexes()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()

    selected_routes = route_avg_truck[route_avg_truck>7].index.tolist

    return selected_routes()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix[matrix>20] *= 0.75
    matrix[matrix<=20] *=1.25

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
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    completeness_series = df.groupby(['id', 'id_2']).apply(check_completeness)
    return completeness_series()

def check_completeness(group):
    # Extract unique dates, weekdays, and hours from the group
    unique_dates = group['start_datetime'].dt.date.unique()
    unique_weekdays = group['start_datetime'].dt.dayofweek.unique()
    unique_hours = group['start_datetime'].dt.hour.unique()
    is_complete = (len(unique_dates) == 7) and (len(unique_weekdays) == 7) and (len(unique_hours) == 24) and check_continuous_intervals(group)
    return pd.Series({'is_complete': is_complete})

def check_continuous_intervals(group):
    # Check if there are no gaps in the time intervals
    return (group['end_datetime'].diff().fillna(pd.Timedelta(seconds=0)) == pd.Timedelta(seconds=1)).all()

    return pd.Series()
