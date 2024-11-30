import pandas as pd

# Load data from CSV
file_path = 'diabetes_data.csv'
data = pd.read_csv(file_path)

# Preview the data
print(data.head())