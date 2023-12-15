import pandas as pd

file_path1 = "https://raw.githubusercontent.com/mapup/MapUp-Data-Assessment-F/main/datasets/dataset-1.csv"
df1 = pd.read_csv(file_path1)

file_path2 = "https://raw.githubusercontent.com/mapup/MapUp-Data-Assessment-F/main/datasets/dataset-2.csv"
df2 = pd.read_csv(file_path2)

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
    car_mat = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    for index in car_mat.index:
        if index in car_mat.columns:
            car_mat.loc[index, index] = 0
    return car_mat

print("ANSWER FOR Q1 : ")
result_1 = generate_car_matrix(df1)
print(result_1)

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()

    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts

print("")
print("ANSWER FOR Q2 : ")
result_2 = get_type_count(df1)
print(result_2)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    # Sort the indices in ascending order
    bus_indexes.sort()
    return bus_indexes

print("")
print("ANSWER FOR Q3 : ")
result_3 = get_bus_indexes(df1)
print(result_3)

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    selected_routes.sort()
    return selected_routes


print("")
print("ANSWER FOR Q4 : ")
result_4 = filter_routes(df1)
print(result_4)

def multiply_matrix(df)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_df = df.copy()

    modified_df[df > 20] *= 0.75
    modified_df[df <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_df = modified_df.round(1)
    return modified_df

print("")
print("ANSWER FOR Q5 : ")
result_df = generate_car_matrix(df1)
result_5 = multiply_matrix(result_df)
print(result_5)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here


     # for loading the dataset form .csv file into dataframe
    df = pd.read_csv(file_path2)

     # Combine 'startDay' and 'startTime' into a single datetime column
    start_datetime = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')

    # Combine 'endDay' and 'endTime' into a single datetime column
    end_datetime = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')

    # Create a DataFrame with (id, id_2) pairs and corresponding start and end timestamps
    timestamps_df = pd.DataFrame({
        'start_datetime': start_datetime,
        'end_datetime': end_datetime
    })

    # Calculate the duration of each timestamp pair
    duration = timestamps_df['end_datetime'] - timestamps_df['start_datetime']
     #  duration.to_csv('duration.csv')

    # Check if each duration covers a full 24-hour period and spans all 7 days
    completeness_check = (duration >= pd.Timedelta(days=1) - pd.Timedelta(seconds=1)) & \
                         (timestamps_df['start_datetime'].dt.dayofweek == 0) & \
                         (timestamps_df['end_datetime'].dt.dayofweek == 6)

    # Create a multi-index boolean series with (id, id_2) as indices
    result_series = completeness_check.groupby([df['id'], df['id_2']]).all()

     # Convert the result series to a DataFrame
    completeness_result = pd.DataFrame(result_series, columns=['is_complete'])

    # Save the result DataFrame to a CSV file
    completeness_result.to_csv('completeness_result.csv')

    return result_series

print("Answer for Q6")
result_6 = time_check(df2)
print(result_6)


