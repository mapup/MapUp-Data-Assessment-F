import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    
    df = pd.read_csv(df)
    df = df.pivot(index="id_1", columns="id_2", values="car")
    np.fill_diagonal(df.values, 0)

    return df


def get_type_count(df)->dict:
    
    df['car_type'] = df['car'].apply(lambda x: 'low' if x <= 15 else 'medium' if x <= 25 else 'high')
    type_count = df.groupby('car_type')['car_type'].count()
    type_count = dict(type_count)
    type_count = dict(sorted(type_count.items()))
    
    return type_count


def get_bus_indexes(df)->list:

    mean_value = df['bus'].mean()
    index_list = df[df['bus'] > 2 * mean_value].index.tolist()
    sorted_index_list = sorted(index_list)

    return sorted_index_list


def filter_routes(df: pd.DataFrame) -> list:

    grouped_df = df.groupby('route')['truck'].mean()
    filtered_routes = grouped_df[grouped_df > 7]

    return sorted(filtered_routes.index.tolist())


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:

    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    return matrix


def time_check(df):
   
    df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M:%S').dt.time
    df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M:%S').dt.time
    grouped = df.groupby(['id', 'id_2'])

    results = pd.Series(dtype=bool)

    for name, group in grouped:
        if (group['startTime'].min() <= pd.to_datetime('00:00:00', format='%H:%M:%S').time() and
            group['endTime'].max() >= pd.to_datetime('23:59:59', format='%H:%M:%S').time() and
            set(group['startDay']).union(set(group['endDay'])) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])):
            results[name] = False
        else:
            results[name] = True

    return results
