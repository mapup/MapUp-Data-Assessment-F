import pandas as pd

def get_type_count():
    # for loading the dataset from .csv file to dataframe
    df=pd.read_csv('dataset-1.csv')

    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

       #  Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts



result_dict = get_type_count()
print(result_dict)