import pandas as pd

def get_bus_indexes():
    # Load the dataset from CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

result_indexes = get_bus_indexes()
print(result_indexes)
