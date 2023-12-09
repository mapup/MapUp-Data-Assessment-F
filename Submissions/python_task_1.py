import pandas as pd
import numpy as np

# Question 1: Car Matrix Generation
def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
# Pivot the DataFrame to get the matrix
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

# Set diagonal values to 0
    np.fill_diagonal(df.values, 0)

    return df

# Question 2: Car Type Count Calculation
def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Adding a new column 'car_type' based on conditions
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = np.select(conditions, choices, default='Unknown')

    # Calculating count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sorting the dictionary alphabetically based on keys
    dict = {key: type_counts[key] for key in sorted(type_counts.keys())}

    return dict

# Question 3: Bus Count Index Retrieval
def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values exceed twice the mean
    list = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    list.sort()

    return list

# Question 4: Route Filtering
def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Calculate average 'truck' values for each route
    avg_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where average 'truck' values are greater than 7
    list = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sort the route names in the list
    list.sort()

    return list

# Question 5: Matrix Value Modification
def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Apply custom conditions to multiply values
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the modified values to 1 decimal place
    matrix = matrix.round(1)

    return matrix

# Question 5: Time Check
def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Combine 'startDay' and 'startTime' columns into a single datetime column 'start_datetime'
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'],errors='coerce')

    # Combine 'endDay' and 'endTime' columns into a single datetime column 'end_datetime'
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'],errors='coerce')

    # Calculate the duration of each timestamp
    df['duration'] = df['end_datetime'] - df['start_datetime']

    # Check if the duration covers a full 24-hour period and spans all 7 days of the week
    full_24_hour = df['duration'].dt.total_seconds() >= 86400  # 24 hours in seconds
    all_7_days = df['start_datetime'].dt.dayofweek.nunique() == 7

    # Aggregate results based on ('id', 'id_2') pairs
    df = df.groupby(['id', 'id_2']).apply(lambda x: all(full_24_hour.loc[x.index]) and all_7_days.loc[x.index[0]])

    return df

df = pd.read_csv(r'C:\Users\iftik\Assignment\MapUp-Data-Assessment-F\datasets\dataset-1.csv')
sample_result = generate_car_matrix(df)
print("The output of Question 1:\n",sample_result)

result = get_type_count(df)
print("The output of Question 2:\n",result)

result = get_bus_indexes(df)
print("The output of Question 3:\n",result)

result = filter_routes(df)
print("The output of Question 4:\n",result)

modified_result = multiply_matrix(sample_result)  # Assuming sample_result is the matrix generated earlier
print("The output of Question 5:\n",modified_result)

df1 = pd.read_csv(r'C:\Users\iftik\Assignment\MapUp-Data-Assessment-F\datasets\dataset-2.csv')
boolean_series = time_check(df1)
print("The output of Question 6:\n",boolean_series)
