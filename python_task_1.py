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
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0

    return car_matrix






def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame): Input DataFrame

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Categorize 'car' values into types
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    return type_counts






def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame): Input DataFrame

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    return bus_indexes

 #Example usage:
 dataset = pd.read_csv("dataset-1.csv")
 result = get_bus_indexes(dataset)
 print(result)





def filter_routes(df: pd.DataFrame) -> list:
    
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Calculate the mean value of the 'truck' column for each 'route'
    route_avg_truck = df.groupby('route')['truck'].mean()

    
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    return selected_routes



def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame): Input DataFrame

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Apply the specified logic to each value in the DataFrame
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix







def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Verify completeness of timestamps for each (id, id_2) pair.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns id, id_2, startDay, startTime, endDay, endTime.

    Returns:
        pd.Series: Boolean series indicating if each (id, id_2) pair has incorrect timestamps.
                   Multi-indexed by id and id_2.
    """
    
    start_timestamp = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    
    end_timestamp = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    
    timestamp_df = pd.DataFrame({'start_timestamp': start_timestamp, 'end_timestamp': end_timestamp})

    
    result_series = timestamp_df.groupby(['id', 'id_2']).apply(
        lambda group: (
            (group['end_timestamp'].max() - group['start_timestamp'].min() >= pd.Timedelta(days=7)) and
            (group['start_timestamp'].min().time() == pd.Timestamp('00:00:00').time()) and
            (group['end_timestamp'].max().time() == pd.Timestamp('23:59:59').time())
        )
    )

    return result_series


