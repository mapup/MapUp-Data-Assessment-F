import pandas as pd

def check_timestamp_completeness():

     # for loading the dataset form .csv file into dataframe
    df = pd.read_csv('dataset-2.csv')

     # Combine 'startDay' and 'startTime' into a single datetime column
    start_datetime = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')

    # Combine 'endDay' and 'endTime' into a single datetime column
    end_datetime = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')

    # Create a DataFrame with (id, id_2) pairs and corresponding start and end timestamps
    timestamps_df = pd.DataFrame({
        'start_datetime': start_datetime,
        'end_datetime': end_datetime
    })

    # Calculate the duration of each timestamp pair
    duration = timestamps_df['end_datetime'] - timestamps_df['start_datetime']
  #  duration.to_csv('duration.csv')

    # Check if each duration covers a full 24-hour period and spans all 7 days
    completeness_check = (duration >= pd.Timedelta(days=1) - pd.Timedelta(seconds=1)) & \
                         (timestamps_df['start_datetime'].dt.dayofweek == 0) & \
                         (timestamps_df['end_datetime'].dt.dayofweek == 6)

    # Create a multi-index boolean series with (id, id_2) as indices
    result_series = completeness_check.groupby([df['id'], df['id_2']]).all()

     # Convert the result series to a DataFrame
    completeness_result = pd.DataFrame(result_series, columns=['is_complete'])

    # Save the result DataFrame to a CSV file
    completeness_result.to_csv('completeness_result.csv')

    return completeness_result


 
completeness_result = check_timestamp_completeness()

print(completeness_result)
