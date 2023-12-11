import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:

    # Write your logic here
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set the diagonal values to 0
    for index in car_matrix.index:
        df.at[index, index] = 0

    return df


def get_type_count(df)->dict:
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))

    return type_count


def get_bus_indexes(df)->list:
    bus_mean = df['bus'].mean()

    # Identify and return the indexes where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the list of indexes in ascending order
    bus_indexes.sort()

    return bus_indexes



def filter_routes(df)->list:
        route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of routes
    filtered_routes.sort()

    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    # Apply custom conditions to multiply matrix values
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix





def time_check(df)->pd.Series:
    # Convert timestamp columns to datetime format
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculate the duration of each timestamp pair
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    # Group by (`id`, `id_2`) and check if the timestamps cover a full 24-hour and 7 days period
    result_series = df.groupby(['id', 'id_2']).apply(
        lambda group: (group['duration'].sum() >= pd.Timedelta(days=7) and
                       (group['start_timestamp'].min().time() == pd.Timestamp('00:00:00').time()) and
                       (group['end_timestamp'].max().time() == pd.Timestamp('23:59:59').time()))
    )

    return result_series



dataset1 = pd.read_csv("..\datasets\dataset-1.csv")  # Replace 'path_to_your_dataset1.csv' with the actual path
dataset2 = pd.read_csv("..\datasets\dataset-2.csv")  # Replace 'path_to_your_dataset1.csv' with the actual path

# Call each function with the dataset1 as an argument
# Call each function with the dataset1 as an argument
car_matrix = generate_car_matrix(dataset1)
print("Car Matrix:")
print(car_matrix)

type_count = get_type_count(dataset1)
print("\nType Count:")
print(type_count)

bus_indexes = get_bus_indexes(dataset1)
print("\nBus Indexes:")
print(bus_indexes)

filtered_routes = filter_routes(dataset1)
print("\nFiltered Routes:")
print(filtered_routes)

modified_matrix = multiply_matrix(car_matrix)
print("\nModified Matrix:")
print(modified_matrix)


time_result_series = time_check(dataset2)
print("\nTime Result Series:")
print(time_result_series)
