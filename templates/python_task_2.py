#import libraries
import pandas as pd
import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

# Question 1:
def calculate_distance_matrix(df):
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(np.zeros((len(unique_ids), len(unique_ids))), index=unique_ids, columns=unique_ids)

    for _, row in df.iterrows():
        start, end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance
    for k in unique_ids:
        distance_matrix += np.where((distance_matrix == 0) & (distance_matrix.T != 0) & (distance_matrix[k] != 0),
                                    distance_matrix[:, k:k+1] + distance_matrix[k:k+1, :], 0)

    np.fill_diagonal(distance_matrix.values, 0)

    return distance_matrix

# Question 2: 
def unroll_distance_matrix(distance_matrix):
    unique_ids = distance_matrix.index
    unrolled_data = []

    for i, id_start in enumerate(unique_ids):
        for id_end in unique_ids[i+1:]:
            distance = distance_matrix.at[id_start, id_end]
            unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    return pd.DataFrame(unrolled_data)

# Question 3: 
def find_ids_within_ten_percentage_threshold(df, reference_id):
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_min, threshold_max = reference_avg_distance - (reference_avg_distance * 0.1), reference_avg_distance + (reference_avg_distance * 0.1)

    filtered_ids = df.groupby('id_start')['distance'].mean().reset_index()
    filtered_ids = filtered_ids[(filtered_ids['distance'] >= threshold_min) & (filtered_ids['distance'] <= threshold_max)]

    return filtered_ids.sort_values(by='id_start')

# Question 4: 
def calculate_toll_rate(df):
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df.drop(columns='distance')

def calculate_time_based_toll_rates(df):
  """
  Calculates time-based toll rates for different time intervals within a day.

  Args:
    df: A Pandas DataFrame.

  Returns:
    A modified Pandas DataFrame with additional columns and adjusted vehicle values.
  """
  # Define time intervals and discount factors for weekdays
  weekday_intervals = {
    ("00:00:00", "10:00:00"): 0.8,
    ("10:00:00", "18:00:00"): 1.2,
    ("18:00:00", "23:59:59"): 0.8,
  }

  # Define discount factor for weekends
  weekend_discount_factor = 0.7

  # Create start and end day columns
  df["start_day"] = pd.to_datetime(df["timestamp"].str.split(" ").str[0]).dt.strftime("%A")
  df["end_day"] = (df["start_day"] + timedelta(days=1)).dt.strftime("%A")

  # Create start and end time columns
  df["start_time"] = df["timestamp"].str.split(" ").str[1].apply(lambda t: datetime.strptime(t, "%H:%M:%S").time())
  df["end_time"] = (df["start_time"] + timedelta(hours=23)).time()

  # Define function to apply discount based on time and day
  def apply_discount(row, intervals=weekday_intervals, discount_factor=weekend_discount_factor):
    start_day = row["start_day"]
    start_time = row["start_time"]
    for interval, factor in intervals.items():
      start_time_interval, end_time_interval = interval
      if start_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        if start_time >= datetime.strptime(start_time_interval, "%H:%M:%S").time() and start_time < datetime.strptime(end_time_interval, "%H:%M:%S").time():
          return row["vehicle"] * factor
    else:
      return row["vehicle"] * discount_factor

  # Apply discount to vehicle values
  df["vehicle"] = df.apply(apply_discount, axis=1)

  return df

# Read the dataset
data = pd.read_csv(r'C:\Users\joshi\Downloads\dataset-3.csv')

# Calculate distance matrix
resulting_distance_matrix = calculate_distance_matrix(data)
print("Distance Matrix result:\n", resulting_distance_matrix)

# Unroll the distance matrix
unrolled_data = unroll_distance_matrix(resulting_distance_matrix)
print("Unroll Distance Matrix result:\n", unrolled_data)


reference_value = 1001404 
resulting_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_data, reference_value)
print("Finding IDs within Percentage Threshold:\n", resulting_ids_within_threshold)

result_with_toll_rates = calculate_toll_rate(unrolled_data)
print("Calculate Toll Rate:\n", result_with_toll_rates)
