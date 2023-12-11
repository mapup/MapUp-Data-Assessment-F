import pandas as pd

dataset1 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')

def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    print(car_matrix)

    return df

result_df = generate_car_matrix(dataset1)

import pandas as pd

def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))

    return dict(sorted_type_counts)

dataset1 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')
result_dict = get_type_count(dataset1)
print(result_dict)

import pandas as pd

def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_indices = df[df['bus'] > 2 * df['bus'].mean()].index.tolist()
    bus_indices.sort()

    return list(bus_indices)

dataset1 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')
result_list = get_bus_indexes(dataset1)
print(result_list)

import pandas as pd

def filter_routes(df: pd.DataFrame) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    filtered_routes.sort()

    return list(filtered_routes)

dataset1 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')
result_list = filter_routes(dataset1)
print(result_list)



def multiply_matrix(df) -> pd.DataFrame:
    """
    Generates a matrix and multiplies its values with custom conditions.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    matrix = matrix.apply(pd.to_numeric, errors='coerce')
    matrix = matrix.applymap(lambda x: x * 0.75 if pd.notna(x) and x > 20 else x * 1.25)
    matrix = matrix.round(1)

    return matrix

dataset1 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')
result_matrix_multiplied = multiply_matrix(dataset1)
print(result_matrix_multiplied)


def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period.

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: Boolean series indicating if each (`id`, `id_2`) pair has incorrect timestamps.
    """
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce', format='%A %H:%M:%S')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce', format='%A %H:%M:%S')
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    incomplete_time_check = (
        (df['duration'] < pd.Timedelta(days=1)) |  # Check if duration is less than 24 hours
        (df.groupby(['id', 'id_2'])['start_timestamp'].transform('min').dt.day_name() != 'Monday') |
        (df.groupby(['id', 'id_2'])['end_timestamp'].transform('max').dt.day_name() != 'Sunday')
    )
    result_series = incomplete_time_check.groupby([df['id'], df['id_2']]).any()

    return pd.Series(result_series)

dataset2 = pd.read_csv('D:/MapUp-Data-Assessment-F-main/datasets/dataset-2.csv')
result = time_check(dataset2)
print(result)

