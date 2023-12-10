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
    # Write your logic here

    new_df = pd.DataFrame(index=df['id_1'].unique(), columns=df['id_2'].unique())

    # Fill the DataFrame with values from the car column
    for i in range(len(df)):
        row = df.iloc[i]
        new_df.loc[row['id_1'], row['id_2']] = row['car']

    # Set diagonal values to 0
    new_df.values[::len(new_df) + 1] = 0
    new_df = new_df.fillna('0')
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
    def categorize_car(car_value):
        if car_value <= 15:
            return "low"
        elif car_value <= 25:
            return "medium"
        else:
            return "high"

    # Add the new 'car_type' column
    df["car_type"] = df["car"].apply(categorize_car)

    # Count occurrences of each car type
    type_counts = df["car_type"].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts


def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus = df["bus"].mean()

    # Identify bus values greater than twice the mean
    filtered_df = df[df["bus"] > 2 * mean_bus]

    # Extract and sort the indices
    bus_indexes = sorted(filtered_df.index.to_list())

    return bus_indexes


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck_by_route = df.groupby("route")["truck"].mean()

    # Filter routes with average truck value greater than 7
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sort filtered routes
    sorted_routes = sorted(filtered_routes)

    return sorted_routes


def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """

    # Write your logic here
    def modify_value(value):
        if value > 20:
            return value * 0.75
        else:
            return value * 1.25

    # Apply the logic to each value in the DataFrame
    matrix = matrix.applymap(modify_value)

    # Round values to 1 decimal place
    matrix = matrix.round(1)
    return matrix


def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    def is_valid_timestamp(start_day, start_time, end_day, end_time):
        try:
            # Convert timestamp strings to datetime objects
            start_datetime = pd.to_datetime(f"{start_day} {start_time}")
            end_datetime = pd.to_datetime(f"{end_day} {end_time}")
            # Check for 24 hours and 7 days duration
            duration = end_datetime - start_datetime
            if duration.days != 7 or duration.seconds != 86400:
                return False
            # Check for valid time range (00:00:00 to 23:59:59)
            if (start_datetime.time() != pd.to_datetime("00:00:00").time() or
                    end_datetime.time() != pd.to_datetime("23:59:59").time()):
                return False
            return True
        except:
            # Handle any errors in conversion or datetime operations
            return False

    # Apply the check to each (id, id_2) pair
    df["valid_timestamps"] = df.apply(
        lambda row: is_valid_timestamp(row["startDay"], row["startTime"], row["endDay"], row["endTime"]), axis=1)

    # Group by (id, id_2) and check if all timestamps are valid
    invalid_timestamps = df.groupby(["id", "id_2"])["valid_timestamps"].all().apply(lambda x: not x)

    return invalid_timestamps


if __name__ == '__main__':
    input1 = r'C:\Users\joshi\Downloads\dataset-1.csv'
    input2 = r'C:\Users\joshi\Downloads\dataset-2.csv'
    df = pd.read_csv(input1)
    df2 = pd.read_csv(input2)
    print(generate_car_matrix(df))
    print(get_type_count(df))
    print(get_bus_indexes(df))
    print(filter_routes(df))
    df_new = generate_car_matrix(df)
    # print(multiply_matrix(df_new))
    print(time_check(df2))

