import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Creating a empty DataFrame to store the distance matrix
    unique_ids = sorted(set(df['id_start']) | set(df['id_end']))
    distance_matrix = pd.DataFrame(0, columns=unique_ids, index=unique_ids)
    # Filling  the distance matrix with cumulative distances along known routes
    for index, row in df.iterrows():
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.at[row['id_end'], row['id_start']] = row['distance']

    
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, k] + distance_matrix.at[k, j] < distance_matrix.at[i, j]:
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    # Seting diagonal values to 0
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0
    
    return distance_matrix

result = calculate_distance_matrix(df)
print(result)


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # extract unique IDs from the index 
    unique_ids = distance_matrix.index
    id_start = []
    id_end = []
    distance = []

    for i in unique_ids:
        for j in unique_ids:
            # Skip rows where id_start equals id_end
            if i != j:
                id_start.append(i)
                id_end.append(j)
                distance.append(distance_matrix.at[i, j])

    unrolled_df = pd.DataFrame({
        'id_start': id_start,
        'id_end': id_end,
        'distance': distance
    })

    return unrolled_df

result_unrolled = unroll_distance_matrix(result)
print(result_unrolled)



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    refer_df = df[df['id_start'] == reference_id]
    ave_distance = refer_df['distance'].mean()
    
    lower_threshold = ave_distance - (ave_distance * 0.1)
    upper_threshold = ave_distance + (ave_distance * 0.1)
    
    filter_ids = df.groupby('id_start')['distance'].mean().reset_index()
    filter_ids = filter_ids[(filter_ids['distance'] >= lower_threshold) & (filter_ids['distance'] <= upper_threshold)]
    
    return filter_ids

    


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    coefficients = {'moto': 0.8,'car': 1.2,'rv': 1.5,'bus': 2.2,'truck': 3.6}
    
    for vehicle, coefficient in coefficients.items():
        df[vehicle] = df['distance'] * coefficient
    
    return df

result_with_toll_rates = calculate_toll_rate(df)
print(result_with_toll_rates)

    


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
