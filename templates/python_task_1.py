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

    # Create a matrix using pivot_table
    df = df.pivot_table(values='car', index='id_1', columns='id_2', aggfunc='sum', fill_value=0)

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
    
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=choices)
    car_type_counts = df['car_type'].value_counts().to_dict()
    car_type_counts = dict(sorted(car_type_counts.items()))

    return car_type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus_value = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean value
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    # Filter routes where the average of 'truck' values is greater than 7
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sort the list of routes in ascending order
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
    df = generate_car_matrix(matrix)
    modified_matrix = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    
    weekday_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

    # Map 'startDay' and 'endDay' to numeric values
    df['start_day_numeric'] = df['startDay'].map(weekday_mapping)
    df['end_day_numeric'] = df['endDay'].map(weekday_mapping)
    df['start_timestamp'] = pd.to_datetime(df['start_day_numeric'].astype(str) + ' ' + df['startTime'], errors='coerce')

    # Combine 'end_day_numeric' and 'endTime' to create 'end_timestamp'
    df['end_timestamp'] = pd.to_datetime(df['end_day_numeric'].astype(str) + ' ' + df['endTime'], errors='coerce')

    # Extract day of the week and time from start and end timestamps
    df['start_day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['end_day_of_week'] = df['end_timestamp'].dt.dayofweek
    df['start_time'] = df['start_timestamp'].dt.time
    df['end_time'] = df['end_timestamp'].dt.time

    # Check if each (id, id_2) pair covers a full 24-hour period and spans all 7 days
    completeness_check = (
            df.groupby(['id', 'id_2'])
            .apply(lambda group: (group['start_time'].min() == pd.Timestamp('00:00:00')) and
                                (group['end_time'].max() == pd.Timestamp('23:59:59')) and
                                (set(group['start_day_of_week']).union(set(group['end_day_of_week'])) == set(range(7))))
        )
    return completeness_check


# df1=pd.read_csv("datasets\dataset-1.csv")
# matrix=generate_car_matrix(df1)

# print(get_type_count(df1))
# print(get_bus_indexes(df1))
# print(filter_routes(df1))
# modified_matrix=multiply_matrix(df1)
# df2=pd.read_csv('datasets\dataset-2.csv')
# print(time_check(df2))


