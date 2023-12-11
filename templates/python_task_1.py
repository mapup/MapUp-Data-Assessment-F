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
    data = pd.read_csv('dataset-1.csv')
    df = pd.read_csv(pd.compat.StringIO(data), delimiter='\t')
    result_df = data.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)

    # Setting diagonal values to 0
    result_df.values[[range(len(result_df))]*2] = 0

    return result_df

# Generate the matrix using the provided data
result_matrix = generate_car_matrix(df)

# Display the result
print(result_matrix)




def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Add a new column 'car_type' based on the conditions
    data['car_type'] = pd.cut(data['car'], bins=[float('-inf'), 15, 25, float('inf')],
                              labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each car_type category
    type_count = data['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count

# Assuming the provided data is saved in a CSV file named 'dataset-1.csv'
data = pd.read_csv('dataset-1.csv')

# Get the count of car types
result = get_type_count(data)

# Display the result
print(result)


   


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

# Assuming the provided data is saved in a CSV file named 'dataset-1.csv'
data = pd.read_csv('dataset-1.csv')

# Get the indices where 'bus' values are greater than twice the mean
result = get_bus_indexes(data)

# Display the result
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
    # Calculate the average value of the 'truck' column for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Assuming the provided data is saved in a CSV file named 'dataset-1.csv'
data = pd.read_csv('dataset-1.csv')

# Get the sorted list of routes based on the average 'truck' values
result = filter_routes(data)

# Display the result
print(result)

    


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # Create a copy of the input DataFrame to avoid modifying the original
    modified_matrix = matrix.copy()

    # Apply the specified logic to each value in the DataFrame
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage with the DataFrame obtained from Question 1
# Replace 'result_dataframe' with the actual variable name you used
result_dataframe = ...

# Modify the DataFrame using the function
modified_result = multiply_matrix(result_dataframe)

# Display the modified DataFrame
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
    # Combine 'startDay' and 'startTime' columns to create a 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Combine 'endDay' and 'endTime' columns to create an 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Check if the time range for each (id, id_2) pair covers a full 24-hour period
    full_day_coverage = ((df['end_timestamp'] - df['start_timestamp']).dt.total_seconds() == 24 * 3600)

    # Check if the time range for each (id, id_2) pair spans all 7 days of the week
    seven_days_coverage = (df.groupby(['id', 'id_2'])['startDay'].nunique() == 7)

    # Combine the two conditions to get the final result
    result_series = full_day_coverage & seven_days_coverage

    return result_series

# Example usage with the DataFrame obtained from dataset-2.csv
# Replace 'data' with the actual variable name you used
data = pd.read_csv('dataset-2.csv')

# Check the time completeness using the function
result = time_check(data)

# Display the result
print(result)
    
