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
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set the diagonal values to 0
    car_matrix.values[[range(len(car_matrix))]*2] = 0

    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Add a new categorical column 'car_type' based on 'car' values
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes


def filter_routes(df):
    """
    Returns the sorted list of values of the 'route' column for which
    the average of values of the 'truck' column is greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame

    Returns:
        list: Sorted list of 'route' values
    """
    # Group by 'route' and calculate the average of 'truck' values
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes in ascending order
    selected_routes.sort()

    return selected_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_df = matrix.copy()

    # Apply the specified logic to each value in the DataFrame
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df = df[(df['id'] >= 0) & (df['id_2'] >= 0)].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Create datetime columns with error handling
    try:
        df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
        df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    except pd.errors.OutOfBoundsDatetime:
        df.loc[:, 'start_timestamp'] = pd.NaT  # Use loc to set values on the original DataFrame
        df.loc[:, 'end_timestamp'] = pd.NaT
    
    # Define multi-index columns
    multi_index_cols = ['id', 'id_2']
    
    # Check completeness
    completeness_check = (
        (df['end_timestamp'] - df['start_timestamp'] == pd.Timedelta(days=1)) &  # Full 24-hour period
        (df['start_timestamp'].dt.dayofweek == 0) &  # Monday
        (df['end_timestamp'].dt.dayofweek == 6)  # Sunday
    )
    
    # Check completeness for all other columns
    completeness_check = completeness_check & df.notna().all(axis=1)
    
    # Create a boolean series with multi-index ('id', 'id_2')
    result_series = completeness_check.groupby([df['id'], df['id_2']]).all()
    
    return result_series
