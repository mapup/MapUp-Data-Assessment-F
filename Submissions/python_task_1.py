import pandas as pd


def generate_car_matrix():
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

     # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-1.csv')
     # for pivoting the dataframe
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
   # car_matrix = car_matrix.fillna(0)

    # for assign the diagonal values to 0
    for i in range(min(car_matrix.shape[0], car_matrix.shape[1])):
        car_matrix.iloc[i, i] = 0


    return car_matrix




def get_type_count():
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
     # for loading the dataset from .csv file to dataframe
    df=pd.read_csv('dataset-1.csv')

    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

       #  Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

   


def get_bus_indexes():
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
     # Load the dataset from CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

    


def filter_routes():
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
      # Load the dataset from CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Group by 'route' and calculate the average of 'truck' for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes



def multiply_matrix():
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
      # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-1.csv')

    # for pivoting the dataframe
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
    car_matrix = car_matrix.fillna(0)

    # for assign the diagonal values to 0
    for i in range(min(car_matrix.shape[0], car_matrix.shape[1])):
        car_matrix.iloc[i, i] = 0


     # Apply the specified logic to each value in the DataFrame
    modified_df = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

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

     # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-2.csv')

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

    