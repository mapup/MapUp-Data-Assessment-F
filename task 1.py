import pandas as pd

def generate_car_matrix(df):
    # Pivot the DataFrame to create the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    for index in car_matrix.index:
        car_matrix.at[index, index] = 0

    return car_matrix


df = pd.read_csv('C:/Users/shiva/OneDrive/Desktop/Mapup/MapUp-Data-Assessment-F/datasets/dataset-1.csv',encoding="UTF-8")
result_matrix = generate_car_matrix(df)

# Print or further use the resulting matrix
print(result_matrix)



def get_type_count(df):
    # Add a new categorical column 'car_type' based on values of the column 'car'
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=choices)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts


df = pd.read_csv('C:/Users/shiva/OneDrive/Desktop/Mapup/MapUp-Data-Assessment-F/datasets/dataset-1.csv',encoding="UTF-8")
result = get_type_count(df)


print(result)




def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    sorted_bus_indexes = sorted(bus_indexes)

    return sorted_bus_indexes


df = pd.read_csv('C:/Users/shiva/OneDrive/Desktop/Mapup/MapUp-Data-Assessment-F/datasets/dataset-1.csv',encoding="UTF-8")
result = get_bus_indexes(df)


print(result)




import pandas as pd

def filter_routes(df):
    # Group by 'route' and calculate the average of the 'truck' column
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes in ascending order
    sorted_routes = sorted(selected_routes)

    return sorted_routes


df = pd.read_csv('C:/Users/shiva/OneDrive/Desktop/Mapup/MapUp-Data-Assessment-F/datasets/dataset-1.csv',encoding="UTF-8")
result = filter_routes(df)


print(result)


    # Filter routes where the average of 'truck' column is greater than 7




def multiply_matrix(input_matrix):
    # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = input_matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage with the DataFrame obtained from generate_car_matrix
# Assuming 'result_matrix' is the DataFrame from generate_car_matrix function
result_matrix = generate_car_matrix(df)
modified_result = multiply_matrix(result_matrix)

# Print or further use the modified DataFrame
print(modified_result)
