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
    df = pd.read_csv("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    car_matrix = car_matrix.fillna(0)

    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0

    return df

dataset_path = "D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv"
result_df = generate_car_matrix(dataset_path)
print(result_df)

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df = pd.read_csv("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], include_lowest=True)
    
    type_counts = df['car_type'].value_counts()

    return dict(type_counts)

dataset_path = "D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv"
result_counts = get_type_count(dataset_path)
print(result_counts)

def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df = pd.read_csv("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    bus_mean = df['bus'].mean()
    
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    bus_indexes.sort()

    return list(bus_indexes)

dataset_path = "D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv"
result_indexes = get_bus_indexes(dataset_path)
print(result_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df = pd.read_csv("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    route_avg_truck = df.groupby('route')['truck'].mean()

    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()


    return list(selected_routes)

dataset_path = "D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv"
selected_routes = filter_routes(dataset_path)
print(selected_routes)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    if not isinstance(multiply_matrix, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    multiply_matrix = matrix.copy()

    multiply_matrix[multiply_matrix > 20] *= 0.75
    multiply_matrix[multiply_matrix <= 20] *= 1.25

    multiply_matrix = multiply_matrix.round(1)

    return multiply_matrix

result_df = generate_car_matrix("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-1.csv")
multiply_result_df = multiply_matrix(result_df)
print(multiply_result_df)
    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df = pd.read_csv("D:\learning\MapUp-Data-Assessment-F\datasets\dataset-2.csv")

    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    full_day_check = (df['end_datetime'] - df['start_datetime']) == pd.Timedelta(days=1)
    
    days_check = df.groupby(['id', 'id_2'])['start_datetime'].agg(lambda x: x.dt.dayofweek.nunique() == 7)

    result_series = full_day_check & days_check

    return result_series

dataset_path = "D:\learning\MapUp-Data-Assessment-F\datasets\dataset-2.csv"
result_series = time_check(dataset_path)
print(result_series)