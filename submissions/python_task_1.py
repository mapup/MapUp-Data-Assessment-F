import pandas as pd
from datetime import datetime, time

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
    temp = df
    df = temp.pivot(index='id_1', columns='id_2', values='car')

    for id in df.index:
        if id in df.columns:
            df.at[id, id] = 0

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
     # Categorizing the 'car' values into 'car_type'
    conditions = [
        df['car'] <= 15,
        (df['car'] > 15) & (df['car'] <= 25),
        df['car'] > 25
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, float('inf')], labels=choices, right=False)

    # Calculating the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    return dict(sorted(type_count.items()))


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # Calculating twice the mean value of the 'bus' column
    mean_bus = df['bus'].mean()
    threshold = 2 * mean_bus

    # Identifying indices where 'bus' values are greater than twice the mean
    indices = df.index[df['bus'] > threshold].tolist()

    # Sorting the indices in ascending order
    indices.sort()
    
    return indices


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    
    # Grouping by 'route' and calculating the average of the 'truck' column
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filtering routes where the average of 'truck' values is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sorting the list of routes
    filtered_routes.sort()

    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    
    # Applying the specified logic to each value in the DataFrame using applymap and rounding decimal to 1 digit
    return matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    
    # Helper function to parse time and day of the week
    def parse_time_day(time_str, day_str):
        return datetime.strptime(day_str + ' ' + time_str, '%A %H:%M:%S')

    # Parsing 'startDay', 'startTime', 'endDay', 'endTime' columns
    df['startTimestamp'] = df.apply(lambda x: parse_time_day(x['startTime'], x['startDay']), axis=1)
    df['endTimestamp'] = df.apply(lambda x: parse_time_day(x['endTime'], x['endDay']), axis=1)

    # Creating a multi-index based on 'id' and 'id_2'
    df.set_index(['id', 'id_2'], inplace=True)

    # Function to check if the time range covers 24 hours for each group
    def covers_full_day(group):
        times = set()
        for _, row in group.iterrows():
            current_day = row['startTimestamp']
            while current_day <= row['endTimestamp']:
                times.add(current_day.time())
                current_day += pd.Timedelta(hours=1)
        return len(times) == 24 * 7

    # Function to check if the time range covers all days of the week for each group
    def covers_full_week(group):
        days = set(group['startTimestamp'].dt.dayofweek) | set(group['endTimestamp'].dt.dayofweek)
        return len(days) == 7

    # Applying the checks and combining results
    return df.groupby(level=[0, 1]).apply(covers_full_day)
