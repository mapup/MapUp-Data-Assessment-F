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
    
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    car_matrix.fillna(0)
    for index in car_matrix.index:
        car_matrix.at[index, index] = 0

    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_dict= dict(sorted(type_counts.items()))

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
    bus_indices = df[df['bus'] > 2 * df['bus'].mean()].index.tolist()
    sorted_bus_ind = sorted(bus_indices)

    return sorted_bus_ind


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
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    sorted_filt= sorted(filtered_routes)

    return sorted_filt


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    matrix = modified_matrix.round(1)

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
    def parse_timestamp(date_str, time_str):
        try:
            return pd.to_datetime(f"{date_str} {time_str}", errors='raise')
        except Exception as e:
            print(f"Error parsing timestamp: {e}")
            return pd.NaT
    df['start_timestamp'] = df.apply(lambda row: parse_timestamp(row['startDay'], row['startTime']), axis=1)
    df['end_timestamp'] = df.apply(lambda row: parse_timestamp(row['endDay'], row['endTime']), axis=1)
    span_all_days = (df.groupby(['id', 'id_2'])['start_timestamp'].apply(lambda x: x.dt.dayofweek.nunique()) == 7)
    result_series = full_24_hours & span_all_days

    return result_series
