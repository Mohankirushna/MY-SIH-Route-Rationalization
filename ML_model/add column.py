import pandas as pd

df = pd.read_csv('My SIH\\model\\traffic_data.csv')

#print(df.tail())

df['delay'] = df['duration_in_traffic_seconds'] - df['duration_seconds']

df.to_csv('My SIH\\model\\traffic_data.csv', index=False)

#print(df.tail())

