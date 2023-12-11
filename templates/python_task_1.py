import pandas as pd
import numpy as np

"Import files from local"

from google.colab import drive 
drive.mount('/content/googledrive/', force_remount=True)

df=pd.read_csv('/content/dataset-1.csv')


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    #pivot the DataFrame 
    pivto = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

     # Fill diagonal values with 0
    for idx in pivto.index:
        if idx in pivto.columns:
            pivto.loc[idx, idx] = 0


    return pivto

df = pd.read_csv('dataset-1.csv')

result_matrix = generate_car_matrix(df)
print(result_matrix)


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = 'low'
    df.loc[df['car'] > 15,'car_type'] ='medium'
    df.loc[df['car'] > 25,'car_type'] ='high'

    type_count = df['car_type'].value_counts



    return type_count()

result = get_type_count(df)
print(result)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    #Find mean value
    mean_value = df['bus'].mean()
    #index of value
    bus_indexes = df[df['bus'] > 2 * mean_value].index.tolist()
    bus_indexes.sort()
    
    return bus_indexes

result = get_bus_indexes(df)
print(result)


def filter_routes(df):
    """
    Returns a sorted list of values in the 'route' column
    where the average of 'truck' column values is greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame containing 'route' and 'truck' columns.

    Returns:
        list: Sorted list of values in 'route' column meeting the specified condition.
    """
    
    avg_truck_values = df.groupby('route')['truck'].mean()
    
    # filtering average of 'truck' column values is greater than 7
    filtered_routes = avg_truck_values[avg_truck_values > 7].index.tolist()
    filtered_routes.sort()
    
    return filtered_routes

result = filter_routes(df)
print(result)



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df = df.copy()
    modified = df[col].apply(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified = modified.round(1)
    return modified


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_timestamp']=pd.to_datetime(df['startDay']+'  '+ df['startTime'])
    df['endtime_timestamp']=pd.to_datetime(df['endDay']+'  '+ df['endTime'])
    df['duration']=df['start_timestamp'] - df['endtime_timestamp'] 
    df_group= df.groupby(['id','id2'])

    min_duration_per_group = df_grouped['duration'].min()
    max_duration_per_group = df_grouped['duration'].max()
    return time_check
    
