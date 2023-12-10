import pandas as pd


def calculate_distance_matrix(file_path):
    df = pd.read_csv(r'C:\Users\LENOVO\Documents\Assessment\MapUp-Data-Assessment-F\datasets\dataset-3.csv')
    unique_ids = df['id_A'].unique()
    num_ids = len(unique_ids)
    distance_matrix = [[0] * num_ids for _ in range(num_ids)]
    for _, row in df.iterrows():
        d_A, id_B, distance = row['id_A'], row['id_B'], row['distance']
        index_A = list(unique_ids).index(id_A)
        index_B = list(unique_ids).index(id_B)

        distance_matrix[index_A][index_B] += distance
        distance_matrix[index_B][index_A] += distance

    distance_df = pd.DataFrame(distance_matrix, index=unique_ids, columns=unique_ids)
    return distance_df



def unroll_distance_matrix(distance_matrix):
    distance_df = distance_matrix.copy()
    for col in distance_df.columns:
        distance_df.loc[col, col] = 0
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for col in distance_df.columns:
        for idx in distance_df.index:
            if idx != col:
                unrolled_df = unrolled_df.append({'id_start': idx, 'id_end': col, 'distance': distance_df.loc[idx, col]},
                                                 ignore_index=True)
    return unrolled_df


'''
def find_ids_within_ten_percentage_threshold(df, reference_id):
    
return 
'''

def calculate_toll_rate(input_df):

#Adding initial column for each vehical type
    input_df['moto'] = 0.0
    input_df['car'] = 0.0
    input_df['rv'] = 0.0
    input_df['bus'] = 0.0
    input_df['truck'] = 0.0

#Assigning Toll rates based on Vehical type
    input_df['moto'] = 0.8 * input_df['distance']
    input_df['car'] = 1.2 * input_df['distance']
    input_df['rv'] = 1.5 * input_df['distance']
    input_df['bus'] = 2.2 * input_df['distance']
    input_df['truck'] = 3.6 * input_df['distance']

    return input_df
    


def calculate_time_based_toll_rates(df):




        return df