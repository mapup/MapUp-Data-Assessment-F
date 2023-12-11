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
    df=pd.read_csv('dataset-1.csv')
    df=df.pivot(index='id_1',columns='id_2',values='car').fillna(0)
    for i in range(min(df.shape)):
        df.iloc[i,i]=0

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
    df=pd.read_csv('dataset-1.csv')
    bin=[-np.inf,15,25,np.inf]
    labels=['low','medium','high']
    df['car_type']=pd.cut(df['car'],bins=bin,labels=labels,right=False)
    tcount=df['car_type'].value_counts().to_dict()
    tcount=dict(sorted(tcount.items()))

    return tcount


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df=pd.read_csv('dataset-1.csv')
    mean=df['bus'].mean()
    result=df[df['bus']>2*mean].index.tolist()
    result.sort()

    return result


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df=pd.read_csv('dataset-1.csv')
    routem=df.groupby('route')['truck'].mean()
    result=routem[routem > 7].index.tolist()
    result.sort()

    return result


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df=pd.read_csv('dataset-1.csv')
    result=result_df.applymap(lambda x : x * 0.75 if x > 20 else x * 1.25)
    reslt=result.round(1)

    return reslt


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
