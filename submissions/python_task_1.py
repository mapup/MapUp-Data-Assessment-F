import pandas as pd

df = pd.read_csv(r"../datasets/dataaset-1.csv")
df_2 = pd.read_csv(r"../datasets/dataset-2.csv")



def generate_car_matrix(df):
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    # Create a cross-tabulation matrix
    car_matrix = pd.crosstab(index=df['id_1'], columns=df['id_2'], values=df['car'], aggfunc='sum')
    
    # Set diagonal values to 0
    for i in range(min(car_matrix.shape[0], car_matrix.shape[1])):
        car_matrix.iloc[i, i] = 0
    
    return car_matrix
    #return df


def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    # Add a new column 'car_type' based on 'car' values
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    
    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()
    
    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))
    
    return type_count
    #return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here


    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()
    
    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    # Sort the indices in ascending order
    bus_indexes.sort()
    
    return bus_indexes
    #return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    
    
    # Group by 'route' and calculate the average of 'truck' values for each group
    route_avg_truck = df.groupby('route')['truck'].mean()
    
    # Filter routes where the average of 'truck' values is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    # Sort the list of routes in ascending order
    filtered_routes.sort()
    
    return filtered_routes

    #return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    
   
    # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Apply the modification logic
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


    #return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Combine 'startDay' and 'startTime' columns to create a 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce', format='%A %H:%M:%S')
    
    # Combine 'endDay' and 'endTime' columns to create an 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce', format='%A %H:%M:%S')
    
    # Drop rows with invalid timestamp values
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])
    
    # Define a reference date (year 2000)
    reference_date = pd.to_datetime('2000-01-01')
    
    # Group by 'id' and 'id_2' and check completeness
    time_check = (
        df.groupby(['id', 'id_2'])
        .apply(lambda group: (
            (group['start_timestamp'].min() == reference_date) and
            (group['end_timestamp'].max() == reference_date + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)) and
            set(group['start_timestamp'].dt.day_name()) == set(pd.date_range('Monday', 'Sunday').day_name)
        ))
    )    

    return time_check
   
    

  
result_matrix = generate_car_matrix(df)
print(result_matrix)


result_type_count = get_type_count(df)
print(result_type_count)

result_bus_indexes = get_bus_indexes(df)
print(result_bus_indexes)

result_filtered_routes = filter_routes(df)
print(result_filtered_routes)

result_modified_matrix = multiply_matrix(result_matrix)
print(result_modified_matrix)

result = time_check(df_2)
print(result)