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

    df = pd.read_csv(r"C:\Users\Ritesh Mishra\Desktop\Assesments\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    # Pivot the DataFrame to create the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
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
    
    df = pd.read_csv(r'C:\Users\Ritesh Mishra\Desktop\Assesments\MapUp-Data-Assessment-F\datasets\dataset-1.csv')

    # Define a function to categorize 'car' values
    def categorize_car(value):
        if value <= 15:
             return 'low'
        elif 15 < value <= 25:
            return 'medium'
        else:
            return 'high'

    # Apply the function to the 'car' column to create the 'car_type' column
    df['car_type'] = df['car'].apply(categorize_car)

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))

    return type_count


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df = pd.read_csv(r"C:\Users\Ritesh Mishra\Desktop\Assesments\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

     # Calculate twice the mean value of the 'bus' column
    mean_bus = 2 * df['bus'].mean()

    # Get the indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > mean_bus].index.tolist()

    # Sort the list in ascending order
    bus_indexes.sort()

    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df = pd.read_csv(r"C:\Users\Ritesh Mishra\Desktop\Assesments\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    # Group by 'route' and calculate the average of the 'truck' column
    avg_truck = df.groupby('route')['truck'].mean()

    # Get the 'route' values where the average 'truck' value is greater than 7
    routes = avg_truck[avg_truck > 7].index.tolist()

    # Sort the list in ascending order
    routes.sort()

    return routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    df = df.round(1)

    return df


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df2 = pd.read_csv(r'C:\Users\Ritesh Mishra\Desktop\MapUp-Data-Assessment-F-main\datasets\dataset-2.csv')

    # Convert the 'startDay', 'startTime', 'endDay', and 'endTime' columns into datetime format
    df2['start'] = pd.to_datetime(df2['startDay'] + ' ' + df2['startTime'])
    df2['end'] = pd.to_datetime(df2['endDay'] + ' ' + df2['endTime'])

    # Check if each unique (id, id_2) pair covers a full 24-hour period and spans all 7 days of the week
    df2['incorrect'] = ((df2['end'] - df2['start']).dt.total_seconds() != 24*60*60) | (df2[['start', 'end']].apply(lambda x: set(pd.date_range(x['start'], x['end'], freq='D').dayofweek), axis=1) != set(range(7)))

    # Return a boolean series that indicates if each (id, id_2) pair has incorrect timestamps
    return df2.set_index(['id', 'id_2'])['incorrect']

    return pd.Series()
