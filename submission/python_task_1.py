import pandas as pd

def generate_car_matrix(dataframe):
    # Pivot the dataframe using id_1 and id_2 columns
    pivoted_df = dataframe.pivot(index='id_1', columns='id_2', values='car')

    
    # Set diagonal values to 0
    for index in pivoted_df.index:
        pivoted_df.at[index, index] = 0

    return pivoted_df

# Assuming df is your DataFrame loaded from 'dataset-1.csv'
df = pd.read_csv('D:\prateek\MapUp-Data-Assessment-F\datasets\dataset-1.csv')
result_matrix = generate_car_matrix(df)

# Print the resulting matrix.
print(result_matrix)



def get_type_count(dataframe):
    # Add a new categorical column 'car_type' based on values of the column 'car'
    dataframe['car_type'] = pd.cut(dataframe['car'], bins=[float('-inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = dataframe['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys.
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

# Assuming df is your DataFrame loaded from 'dataset-1.csv'
df = pd.read_csv('D:/prateek/MapUp-Data-Assessment-F/datasets/dataset-1.csv')

# Call the function and store the result in result_counts
result_counts = get_type_count(df)

# Print the result
print(result_counts)




def get_bus_indexes(dataframe):
    # Calculate the mean value of the 'bus' column
    mean_bus = dataframe['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = dataframe[dataframe['bus'] > 2 * mean_bus].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Example usage:
# Assuming df is your DataFrame loaded from 'dataset-1.csv'
df = pd.read_csv('D:/prateek/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
result_indexes = get_bus_indexes(df)

# Print the result
print(result_indexes)


def filter_routes(dataframe):
    # Group by 'route' and calculate the mean of the 'truck' column for each route
    route_means = dataframe.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    filtered_routes = route_means[route_means > 7].index.tolist()

    return filtered_routes

# Example usage:
# Assuming df is your DataFrame loaded from 'dataset-1.csv'
df = pd.read_csv('D:/prateek/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
result_routes = filter_routes(df)

# Print the result
print(result_routes)



def multiply_matrix(input_matrix):
    # Create a copy of the input matrix to avoid modifying the original
    modified_matrix = input_matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


# Call the function to modify the matrix
modified_result = multiply_matrix(result_matrix)

# Print the modified matrix
print(modified_result)



def verify_time_completeness(dataframe):
    # Combine date and time columns and create datetime objects
    dataframe['start_datetime'] = pd.to_datetime(dataframe['startDay'] + ' ' + dataframe['startTime'], errors='coerce')
    dataframe['end_datetime'] = pd.to_datetime(dataframe['endDay'] + ' ' + dataframe['endTime'], errors='coerce')

    # Calculate the duration for each row
    dataframe['duration'] = dataframe['end_datetime'] - dataframe['start_datetime']

    # Group by unique ('id', 'id_2') pairs
    grouped_data = dataframe.groupby(['id', 'id_2'])

    # Check if timestamps cover a full 24-hour period and span all 7 days
    completeness_check = grouped_data.apply(lambda group: (
        (group['duration'].min() >= pd.Timedelta(hours=0)) and
        (group['duration'].max() <= pd.Timedelta(hours=23, minutes=59, seconds=59)) and
        (set(group['start_datetime'].dt.dayofweek) == set(range(7)))
    ))

    return completeness_check

# Example usage:
# Assuming df is your DataFrame loaded from 'dataset-2.csv'
df = pd.read_csv('D:\prateek\MapUp-Data-Assessment-F\datasets\dataset-2.csv')

# Call the function to verify time completeness
completeness_result = verify_time_completeness(df)

# Print the result
print(completeness_result)




