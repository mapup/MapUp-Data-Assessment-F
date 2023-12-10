import pandas as pd

#To upload from local drive
from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['dataset-3.csv']))
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
import numpy as np
def calculate_distance_matrix(df):
    id = []
    id.extend(list(df['id_start']))
    id.extend(list(df['id_end']))
    id = set(id)
    id = list(id)
    id.sort()
    id1 =id
    id = pd.Series(id)
    matrix = [[0 for _ in range(len(id))] for _ in range(len(id))]
    for index, row in df.iterrows():
        row_index = list(id).index(row['id_start'])
        col_index = list(id).index(row['id_end'])
        matrix[row_index][col_index] = row['distance']
        matrix[col_index][row_index] = row['distance']
    dis_matrix = pd.DataFrame(matrix, index=id, columns=id)
    for i in range(len(id)):
        for j in range(i + 1, len(id)):
            if dis_matrix.iloc[i, j] == 0:
                non_zero =  dis_matrix.iloc[i, :].replace(0, np.nan).dropna()
                if len(non_zero) > 0:
                     dis_matrix.iloc[i, j] = non_zero.values[0] +  dis_matrix.iloc[id1.index(non_zero.index[0]), j]
                     dis_matrix.iloc[j, i] = dis_matrix.iloc[i, j]

    return dis_matrix
    
    


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    distance = distance_matrix.rename_axis('id_start').reset_index()
    unrolled = distance_df.melt(id_vars='id_start', var_name='id_end', value_name='distance')
    unrolled = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled.reset_index(drop=True)


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
    mean = df[df['id_start'] == reference_value]['distance'].mean()
    Lowerlimit = mean * 0.9
    UpperLimit = mean * 1.1
    Range = df[(df['id_start'] != reference_value) &
                          (df['distance'] >= Lowerlimit) &
                          (df['distance'] <= UpperLimit)]['id_start'].unique()
    return sorted(Range)


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    toll_df = distance_matrix.copy()
    toll_df['moto'] = toll_df.apply(lambda row: row * 0.8 if row.name != row.index else 0, axis=1)
    toll_df['car'] = toll_df.apply(lambda row: row * 1.2 if row.name != row.index else 0, axis=1)
    toll_df['rv'] = toll_df.apply(lambda row: row * 1.5 if row.name != row.index else 0, axis=1)
    toll_df['bus'] = toll_df.apply(lambda row: row * 2.2 if row.name != row.index else 0, axis=1)
    toll_df['truck'] = toll_df.apply(lambda row: row * 3.6 if row.name != row.index else 0, axis=1)
    return toll_df





def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    morning = pd.to_datetime('10:00:00').time()
    evening = pd.to_datetime('18:00:00').time()
    def discount(row):
        if row['start_time'].weekday() < 5: 
            if row['start_time'].time() < morning:
                return row * 0.8
            elif row['start_time'].time() < evening:
                return row * 1.2
            else:
                return row * 0.8
        else:
            return row * 0.7
    vehicles = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle in vehicles:
        df[vehicle] = df[vehicle].apply(discount)
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['start_day'] = df['start_time'].dt.weekday.map(week)
    df['end_day'] = df['end_time'].dt.weekday.map(week)
    df['start_time'] = df['start_time'].dt.time
    df['end_time'] = df['end_time'].dt.time
    return df
   
