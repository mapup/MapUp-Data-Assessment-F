import pandas as pd

def multiply_matrix():
    # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-1.csv')

    # for pivoting the dataframe
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
    car_matrix = car_matrix.fillna(0)

    # for assign the diagonal values to 0
    for i in range(min(car_matrix.shape[0], car_matrix.shape[1])):
        car_matrix.iloc[i, i] = 0


     # Apply the specified logic to each value in the DataFrame
    modified_df = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df

result_matrix = multiply_matrix()
print(result_matrix)