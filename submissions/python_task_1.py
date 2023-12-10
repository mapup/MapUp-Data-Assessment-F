import pandas as pd


def generate_car_matrix(df):
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Checking if the columns are present in the given dataframe.
    if 'id_1' not in df.columns or 'id_2' not in df.columns or 'car' not in df.columns:
        raise ValueError("Dataframe must have columns 'id_1', 'id_2', 'car'")

    new_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Filling the diagonal entries with zero
    for i in range(len(new_df)):
        new_df.iloc[i, i] = 0

    return new_df


def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Checking if the columns are present in the given dataframe.
    if 'car' not in df.columns:
        raise ValueError("Data frame must have the column 'car'")

    # Replacing the values with the category
    for i in range(len(df)):
        if df.loc[i, 'car'] <= 15:
            df.loc[i, 'car_type'] = 'low'
        elif 15 < df.loc[i, 'car'] <= 25:
            df.loc[i,'car_type'] = 'medium'
        else:
            df.loc[i, 'car_type'] = 'high' 

    # Grouping and counting each category.
    count_dict = dict(df.groupby('car_type')['car_type'].count())
    sorted_dict = dict(sorted(count_dict.items()))
    return sorted_dict


def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # If bus column not present raise ValueError
    if 'bus' not in df.columns:
        raise ValueError("Data frame must have the column 'bus'")
    # The list containing the values
    bus_list = list(df[df['bus']>2*df['bus'].mean()].index)
    return bus_list


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # If route or truck columns not present raise ValueError
    if 'route' not in df.columns or 'truck' not in df.columns:
        raise ValueError("Data frame must have the column 'route' and 'truck'")

    # Dataframe grouped by routes and values as mean of truck values
    route_truck_mean = df.groupby('route')['truck'].mean()

    # Sorted list of the routes with truck mean greater than 7
    route_list = sorted(list(route_truck_mean[route_truck_mean > 7].index))
    
    return route_list


def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Applying the generate_car_matrix function to dataframe.
    data_matrix = generate_car_matrix(matrix)

    # Applying the given conditions to the obtained matrix
    modified_matrix = data_matrix.applymap(lambda s: round(s*0.75, 1) if s > 20 else round(s*1.25, 1))

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Ensure the required columns exist in the DataFrame
    if 'id' not in df.columns or 'id_2' not in df.columns or 'startDay' not in df.columns or 'startTime' not in df.columns or 'endDay' not in df.columns or 'endTime' not in df.columns:
        raise ValueError("DataFrame must have 'id', 'id_2', 'startDay', 'startTime', 'endDay', and 'endTime' columns.")

    # Adding a extra boolean column for the conditions checked
    df['time_stamp_bool'] = ((df['startTime'] != '00:00:00') | 
                                (df['endTime'] != '23:59:59') | 
                                (df['startDay'] != 'Monday') | 
                                (df['endDay'] != 'Sunday'))

    # Grouping on the basis of the ids such that any condition is satisfied.
    result = df.groupby(['id', 'id_2'])['time_stamp_bool'].any()

    return result

    