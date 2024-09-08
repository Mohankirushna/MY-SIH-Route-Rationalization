import pandas as pd

# Read the CSV file
df = pd.read_csv('updated_schedule.csv')

# Arrange the data in order
df = df.sort_values(by='departure_time')

# Verify the sorted data
print(df.head())  # print the first few rows to verify the sorting

# Save the sorted data to a new CSV file (optional)
df.to_csv('updated_schedule.csv', index=False)