import pandas as pd
import datetime

### Question 1: Distance Matrix Calculation


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    ids=sorted(set(df['id_start']).union(df['id_end']))
    distance_matrix=pd.DataFrame(0,index=ids,columns=ids)
    for _,row in df.iterrows():
        distance_matrix.at[row['id_start'],row['id_end']]=row['distance']
        distance_matrix.at[row['id_end'],row['id_start']]=row['distance']
        
    for k in ids:
        for i in ids:
            for j in ids:
                if (distance_matrix.at[i, k] + distance_matrix.at[k, j] < distance_matrix.at[i, j]) or (distance_matrix.at[i, j] == 0 and i != j):
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]
                    distance_matrix.at[j, i] = distance_matrix.at[i, j]  
    

    return distance_matrix

### using the function
df=pd.read_csv('dataset-3.csv')
final_result=calculate_distance_matrix(df)
print(final_result)


### Question 2: Unroll Distance Matrix

def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    records = []
    
    # Iterate over the matrix and populate the list with records
    for start_id in df.index:
        for end_id in df.columns:
            if start_id != end_id:  # Exclude same id_start to id_end
                records.append({
                    'id_start': start_id,
                    'id_end': end_id,
                    'distance': df.at[start_id, end_id]
                })
    
    # Create a DataFrame from the list of records
    unrolled_df = pd.DataFrame(records)
    
    return unrolled_df


### using the function
final_result=unroll_distance_matrix(df)
print(final_result)


### Question 3: Finding IDs within Percentage Threshold

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
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    # Calculate the 10% threshold values
    lower_threshold = reference_avg_distance * 0.9
    upper_threshold = reference_avg_distance * 1.1
    # Find all unique id_start values
    unique_ids = df['id_start'].unique()
    # Create a DataFrame to hold the ids and their average distances
    ids_distances = pd.DataFrame(unique_ids, columns=['id_start'])
    ids_distances['average_distance'] = ids_distances.apply(lambda row: df[df['id_start'] == row['id_start']]['distance'].mean(), axis=1)
    # Filter ids by threshold
    ids_within_threshold_df = ids_distances[(ids_distances['average_distance'] >= lower_threshold) &
                                            (ids_distances['average_distance'] <= upper_threshold)]
    # Drop the average_distance column as it's not required in the final output
    ids_within_threshold_df = ids_within_threshold_df.drop(columns=['average_distance'])
    # Sort the DataFrame by id_start
    ids_within_threshold_df = ids_within_threshold_df.sort_values(by='id_start').reset_index(drop=True)
    
    return ids_within_threshold_df

### using the function
final_result=find_ids_within_ten_percentage_threshold(df,1001400)
print(final_result)


### Question 4: Calculate Toll Rate

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients={
        'moto':0.8,
        'car':1.2,
        'rv':1.5,
        'bus':2.2,
        'truck':3.6
    }
    for vehicle,coefficient in rate_coefficients.items():
        df[vehicle]=df['distance']*coefficient

    return df

### using the function
final_result=calculate_toll_rate(df)
print(final_result)


### Question 5: Calculate Time-Based Toll Rates

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    time_discounts_weekday=[
        (datetime.time(0,0),datetime.time(10,0),0.8),
        (datetime.time(10,0),datetime.time(18,0),1.2),
        (datetime.time(18,0),datetime.time(23,59,59),0.8)
    ]
    discount_weekend=0.7
    ### output dataframe
    time_based_tolls=pd.DataFrame()
    for unique_pair in df[['id_start', 'id_end']].drop_duplicates().to_numpy():
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start_time, end_time, discount_factor in time_discounts_weekday:
                new_row = df[(df['id_start'] == unique_pair[0]) & (df['id_end'] == unique_pair[1])].copy()
                new_row['start_day'] = day
                new_row['end_day'] = day
                new_row['start_time'] = start_time
                new_row['end_time'] = end_time
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    new_row[vehicle] *= discount_factor
                time_based_tolls = pd.concat([time_based_tolls, new_row])

        for day in ['Saturday', 'Sunday']:
            new_row = df[(df['id_start'] == unique_pair[0]) & (df['id_end'] == unique_pair[1])].copy()
            new_row['start_day'] = day
            new_row['end_day'] = day
            new_row['start_time'] = datetime.time(0, 0)
            new_row['end_time'] = datetime.time(23, 59, 59)
            for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                new_row[vehicle] *= discount_weekend
            time_based_tolls = pd.concat([time_based_tolls, new_row])
    
        # Reorder the columns according to the prompt
    column_order = ['id_start', 'id_end', 'distance', 'start_day', 'start_time', 'end_day', 'end_time','moto', 'car', 'rv', 'bus', 'truck', ]
    time_based_tolls = time_based_tolls[column_order].reset_index(drop=True)
        
    return time_based_tolls


#### using the function

final_result=calculate_time_based_toll_rates(df)
print(final_result)
    