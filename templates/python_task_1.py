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
    np.fill_diagonal(car_matrix.values, 0)
    

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
     car_categories = {
        "low": (0, 15],
        "medium": (15, 25],
        "high": (25, None],
    }

    # Create a new column 'car_type' with categorized values
    df["car_type"] = df["car"].apply(
        lambda car: next(
            category for category, range in car_categories.items() if car in range
        )
    )

    # Count occurrences of each car type
    type_counts = df["car_type"].value_counts().sort_index()

    return type_counts.to_dict()

    //return dict()


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
    mean_bus_value = df['bus'].mean()

    # Identify indices where bus values are greater than twice the mean
    bus_indices = df.loc[df['bus'] > 2 * mean_bus_value].index

    # Sort the bus indices in ascending order and convert to a list
    bus_indices_list = bus_indices.sort_values().tolist()

    return bus_indices_list


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

     # Calculate average 'truck' values for each route
    average_truck_per_route = df.groupby('route')['truck'].mean()

    # Filter routes with average 'truck' values greater than 7
    filtered_routes = average_truck_per_route[average_truck_per_route > 7]

    # Sort filtered route names in ascending order
    sorted_routes = filtered_routes.sort_values(ascending=True).index.to_list()

    return sorted_routes

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    # Define threshold values
    threshold_high = 20

    # Modify values based on thresholds
    matrix.loc[matrix > threshold_high] *= 0.75
    matrix.loc[matrix <= threshold_high] *= 1.25

    # Round values to one decimal place
    return matrix.round(1)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    # Check if there are at least 24 timestamps per day
    daily_timestamps = df.groupby(['id', 'id_2'])['timestamp'].apply(
        pd.Series.dt.hour.nunique
    ) >= 24

    # Check if there are timestamps for at least 7 days
    days_covered = df.groupby(['id', 'id_2'])['timestamp'].dt.date.nunique() >= 7

    # Combine both checks and return the result as a Series
    return daily_timestamps & days_covered
