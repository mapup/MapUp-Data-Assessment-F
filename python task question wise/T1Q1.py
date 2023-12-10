import pandas as pd

def generate_car_matrix():
    # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-1.csv')

    # for pivoting the dataframe
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
   # car_matrix = car_matrix.fillna(0)

    # for assign the diagonal values to 0
    for i in range(min(car_matrix.shape[0], car_matrix.shape[1])):
        car_matrix.iloc[i, i] = 0


    return car_matrix

result_matrix = generate_car_matrix()
print(result_matrix)
