import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
origin = "Ballygunge, Kolkata, West Bengal"
destination = "Netaji Subhash Chandra Bose International Airport, Kolkata, West Bengal"
distance_meters = 19955
duration_seconds = 2288

# Date range for the new data
start_date = datetime(2024, 11, 3, 17, 22)
end_date = datetime(2024, 11, 8, 16, 22)
current_date = start_date

# List to hold the new rows
data = []

# Generate new rows
while current_date <= end_date:
    # Generate random traffic duration between 1888 and 2688 seconds
    duration_in_traffic_seconds = np.random.randint(1888, 2689)
    
    # Calculate delay
    delay = duration_in_traffic_seconds - duration_seconds
    
    # Append the data to the list
    data.append([origin, destination, distance_meters, duration_seconds, duration_in_traffic_seconds, current_date.strftime('%Y-%m-%d %H:%M:%S'),delay])
    
    # Move to the next hour
    current_date += timedelta(hours=1)

# Create DataFrame
columns = ['origin', 'destination', 'distance_meters', 'duration_seconds', 'duration_in_traffic_seconds', 'departure_time','delay']
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('fake_data.csv', index=False)

print("Fake data generated and saved to 'fake_data.csv'")
