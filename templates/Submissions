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
    df = pd.read_csv("dataset-1.csv")
    
    car_pivot = df.pivot(index='id_1', columns='id_2', values='car')
    diagonal_indices = np.diag_indices_from(car_pivot)
    car_pivot.values[diagonal_indices] = 0
    
    return car_pivot
new_df = generate_car_matrix(df)
print(new_df)


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df.loc[df['car'] <= 15, 'car_type'] = 'low'
    df.loc[(df['car'] > 15) & (df['car'] <= 25), 'car_type'] = 'medium'
    df.loc[df['car'] > 25, 'car_type'] = 'high'
    
    count_dict = df['car_type'].value_counts().to_dict()
    
    sorted_count_dict = dict(sorted(count_dict.items()))
    
    return sorted_count_dict

data = pd.read_csv("dataset-1.csv")

result = get_type_count(data)
print(result)

def get_bus_indexes(df) -> list:
    """
    Identifies and returns indices where 'bus' values are greater than twice the mean value of the 'bus' column.

    Args:
        df (pandas.DataFrame): Input DataFrame.

    Returns:
        list: A list of indices sorted in ascending order.
    """
    bus_mean = df['bus'].mean()
    
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    bus_indexes.sort()
    
    return bus_indexes

data = pd.read_csv("dataset-1.csv")

result = get_bus_indexes(data)
print(result)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    truck_avg = df.groupby('route')['truck'].mean()
    filter_routes = truck_avg[truck_avg > 7].index.tolist()
    filter_routes.sort()
    
    return filter_routes

data = pd.read_csv("dataset-1.csv")

result = filter_routes(data)
print(result)

def multiply_matrix(input_df)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """

    modified_df = input_df.copy()
    
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    modified_df = modified_df.round(1)
    
    return modified_df

resulting_df = new_df

modified_result = multiply_matrix(resulting_df)
print(modified_result)

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['startDay'] = pd.to_datetime(df['startDay'], errors='coerce')
    df['endDay'] = pd.to_datetime(df['endDay'], errors='coerce')
    df['startTime'] = pd.to_datetime(df['startTime'], errors='coerce').dt.time
    df['endTime'] = pd.to_datetime(df['endTime'], errors='coerce').dt.time

    def check_timestamps(group):
        hours_covered = set(group['startTime'].apply(lambda x: x.hour)) | set(group['endTime'].apply(lambda x: x.hour))
        all_hours_covered = len(hours_covered) == 24

        days_covered = set(group['startDay'].dt.dayofweek) | set(group['endDay'].dt.dayofweek)
        all_days_covered = len(days_covered) == 7

        return not (all_hours_covered and all_days_covered)

    incomplete_timestamps = df.groupby(['id', 'id_2']).apply(check_timestamps)

    return incomplete_timestamps

data = pd.read_csv("dataset-2.csv")

result = time_check(data)
print(result)

