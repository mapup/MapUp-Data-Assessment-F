import pandas as pd
import numpy as np
'''To upload from local drive'''
from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['dataset-1.csv']))

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
      ans = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
      np.fill_diagonal(ans.values, 0)

      return ans
updated_df = generate_car_matrix(df)
print(updated_df)



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
     df.loc[df['car'] > 15, 'car_type'] = 'medium'
     df.loc[df['car'] > 25, 'car_type'] = 'high'
     type_count = df['car_type'].value_counts().sort_index().to_dict()
     return type_count
updated_df = get_type_count(df)
print(updated_df)

  


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
    indices = df[df['bus'] > 2 * mean].index.tolist()
    indices.sort()
    return indices
ans = get_bus_indexes(df)
print(ans)
   



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
      
    mean_truck = dataframe.groupby('route')['truck'].mean()
    routes = mean_truck[mean_truck> 7].index.tolist()
    routes.sort()
    return routes
ans = filter_routes(df)
print(ans)



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    
    updated_df = result_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    updated_df = updated_df.round(1)
    return updated_df

'''To upload dataset-2 from local drive'''
from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['dataset-2.csv']))
def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']
    grp = df.groupby(['id', 'id_2'])
    check = grp.apply(lambda x: (
        (x['duration'].min() >= pd.Timedelta(days=1)) and
        (x['duration'].max() <= pd.Timedelta(days=1, seconds=1)) and
        (x['start_timestamp'].dt.dayofweek.nunique() == 7)
    ))
    return check
