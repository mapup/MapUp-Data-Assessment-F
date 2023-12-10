import pandas as pd


def generate_car_matrix(dataframe):
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
        # Pivot the DataFrame to get 'car' values based on 'id_1' and 'id_2'
    car_matrix = dataframe.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    for i in car_matrix.index:
        car_matrix.at[i, i] = 0.0
    # Round values to one decimal point
    car_matrix = car_matrix.round(1)

    return car_matrix

# Example usage
# Assuming df is your DataFrame containing the data
df = pd.read_csv('C:\\Users\\user\\Desktop\\Mapup\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')
result_matrix = generate_car_matrix(df)
print(result_matrix)



def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
          # Add a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'],
                            bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'],
                            right=False)

    # Calculate the count of occurrences for each 'car_type'
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count

# Assuming you have loaded the CSV file into a DataFrame named 'dataset'
dataset = pd.read_csv('C:\\Users\\user\\Desktop\\Mapup\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')


# Call the function and print the result
result_count = get_type_count(dataset)
print(result_count)

    

def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Assuming you have loaded the CSV file into a DataFrame named 'dataset'
dataset = pd.read_csv('C:\\Users\\user\\Desktop\\Mapup\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')

# Call the function and print the result
result_indexes = get_bus_indexes(dataset)
print(result_indexes)

    


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    def filter_routes(df):
    # Group by 'route' and calculate the average of 'truck' column for each group
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Assuming you have loaded the CSV file into a DataFrame named 'dataset'
dataset = pd.read_csv('C:\\Users\\user\\Desktop\\Mapup\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')


# Call the function and print the result
result_routes = filter_routes(dataset)
print(result_routes)
    

def multiply_matrix(input_matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = input_matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Assuming 'result_matrix' is the DataFrame from Question 1
# You can replace it with the actual variable you have
result_matrix = generate_car_matrix(pd.read_csv('C:\\Users\\user\\Desktop\\Mapup\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv'))

# Call the function and print the result
modified_result = multiply_matrix(result_matrix)
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

    return pd.Series()
