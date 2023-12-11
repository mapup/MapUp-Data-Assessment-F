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
    # Pivot the DataFrame to get values from 'car' with 'id_1' as index and 'id_2' as columns
    df = dataset.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0 (assuming NaN means no car for that combination)
    df = result_df.fillna(0)

    for col in df.columns:
        df.at[col, col] = 0

    

    return df


def get_type_count(data)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
     data['car_type'] = pd.cut(data['car'], bins=[-float('inf'), 15, 25, float('inf')],
                                labels=['low', 'medium', 'high'], right=False)

    dict = data['car_type'].value_counts().to_dict()

    dict = dict(sorted(dict.items()))

    return dict()


def get_bus_indexes(data)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    mean_bus_value = data['bus'].mean()

    List = dataset[data['bus'] > 2 * mean_bus_value].index.tolist()

    List.sort()

    return List()

    


def filter_routes(data)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
def filter_routes(data):
    
    route_avg_truck = data.groupby('route')['truck'].mean()
    List = route_avg_truck[route_avg_truck > 7].index.tolist()

  

    return List()

    


def multiply_matrix(dataset)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    matrix = dataset.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    matrix = matrix.round(1)
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
data_2['start_datetime'] = pd.to_datetime(data_2['start_day'] + ' ' + data_2['start_time'])
    data_2['end_datetime'] = pd.to_datetime(data_2['end_day'] + ' ' + data_2['end_time'])

    data_2['duration'] = data_2['end_datetime'] - data_2['start_datetime']
    completeness_check = data_2.groupby(['id', 'id_2']).apply(lambda group: check_time_completeness(group)).droplevel(level=[0, 1])

    return completeness_check

    return pd.Series()
