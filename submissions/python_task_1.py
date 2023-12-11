import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_car_matrix(df) -> pd.DataFrame:
    # Pivot the DataFrame to get 'car' values in the desired format
    matrix_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Replace NaN values with 0 and set diagonal values to 0
    matrix_df = matrix_df.fillna(0).astype(float)
    matrix_df.values[[range(len(matrix_df))] * 2] = 0.0

    return matrix_df


# df = pd.read_csv('dataset-1.csv')
# result_df = generate_car_matrix(df)
# print(result_df)


def get_type_count(df) -> dict:
    # Create a new column 'car_type' based on the conditions
    df['car_type'] = np.select(
        [
            df['car'] <= 15,
            (df['car'] > 15) & (df['car'] <= 25),
            df['car'] > 25
        ],
        [
            'low',
            'medium',
            'high'
        ],
        default='unknown'  # You can set a default value if none of the conditions match
    )

    # Count occurrences for each car_type
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts


# df = pd.read_csv('dataset-1.csv')
# result = get_type_count(df)
# print(result)


def get_bus_indexes(df):
    # Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()

    # Filter the DataFrame to get rows where 'bus' values are greater than twice the mean
    filtered_df = df[df['bus'] > 2 * bus_mean]

    # Get the indices of the filtered rows
    bus_indexes = filtered_df.index.tolist()

    return bus_indexes


# df = pd.read_csv('dataset-1.csv')
# result = get_bus_indexes(df)
# print(result)


def filter_routes(df):
    # Group by 'route' and calculate the average of 'truck' values for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7]

    # Return the sorted list of route names
    return sorted(filtered_routes.index.tolist())


# df = pd.read_csv('dataset-1.csv')
# filtered_routes_list = filter_routes(df)
# print(filtered_routes_list)



def multiply_matrix(matrix):
    # Create a copy of the matrix to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Apply the specified conditions
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


# df = pd.read_csv('dataset-1.csv')
# result_df = generate_car_matrix(df)
# modified_result_df = multiply_matrix(result_df)
# print(modified_result_df)



def convert_to_datetime(row, time_str, weekdays):
    day_str = weekdays[int(row['startDay'])]  # Convert back to string
    return datetime.strptime(day_str + ' ' + row[time_str], '%A %H:%M:%S')

def time_check(df):
    # Convert days to numerical representation
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['startDay'] = df['startDay'].apply(lambda x: weekdays.index(x))
    df['endDay'] = df['endDay'].apply(lambda x: weekdays.index(x))

    # Convert start and end timestamps to datetime
    df['startTimestamp'] = df.apply(lambda row: convert_to_datetime(row, 'startTime', weekdays), axis=1)
    df['endTimestamp'] = df.apply(lambda row: convert_to_datetime(row, 'endTime', weekdays), axis=1)

    # Check if time range covers a full 24-hour period
    df['full_day_coverage'] = (df['endTimestamp'] - df['startTimestamp']) >= timedelta(hours=24)

    # Check if time range spans all 7 days of the week
    df['days_coverage'] = (df['endDay'] - df['startDay'] + 1) % 7 == 0

    # Group by id and id_2, check if any group has incorrect timestamps
    result = df.groupby(['id', 'id_2'])[['full_day_coverage', 'days_coverage']].all()

    return result


# df = pd.read_csv('dataset-2.csv')
# result_series = time_check(df)
# print(result_series)

