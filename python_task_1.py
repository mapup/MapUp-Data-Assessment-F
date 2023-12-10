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
   # Create a pivot table using id_1, id_2, and car columns
    pivot_table = df.pivot(index='id_1', columns='id_2', values='car')

    # Replace NaN values with 0
    pivot_table = pivot_table.fillna(0)

    # Set diagonal values to 0
    pivot_table.values[[range(len(pivot_table))]*2] = 0

    return pivot_table

   


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
   # Create a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'],
                            bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'],
                            right=False)

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
    # Calculate the mean value of the 'bus' column
    mean_bus_value = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean value
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

    return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
   # Group by 'route' and calculate the mean of 'truck' for each group
    route_truck_means = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' is greater than 7
    selected_routes = route_truck_means[route_truck_means > 7].index.tolist()

    # Sort the list of selected routes
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
   # Apply the specified logic to modify values in the DataFrame
    modified_df = result_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df

   


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
         )
    )

    return completeness_check

# Example usage
file_path = 'dataset-2.csv'
df = pd.read_csv(file_path)
result_series = verify_timestamps(df)
print(result_series)
