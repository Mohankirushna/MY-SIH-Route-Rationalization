import pandas as pd
from datetime import datetime, timedelta

# Load CSV data
bus_schedule = pd.read_csv('My SIH\\bus_schedule.csv')
passenger_data = pd.read_csv('My SIH\\book-ticket.csv')

bus_schedule['departure_time'] = bus_schedule['departure_time'].str.replace(r':00$', '', regex=True)
bus_schedule['arrival_time'] = bus_schedule['arrival_time'].str.replace(r':00$', '', regex=True)

# Convert time columns to datetime
bus_schedule['departure_time'] = pd.to_datetime(bus_schedule['departure_time'], format='%H:%M').dt.time
bus_schedule['arrival_time'] = pd.to_datetime(bus_schedule['arrival_time'], format='%H:%M').dt.time

invalid_times = bus_schedule[bus_schedule['departure_time'].isna() | bus_schedule['arrival_time'].isna()]
if not invalid_times.empty:
    print("Warning: Some time data could not be converted:")
    print(invalid_times)


### 3. Predict Bus Delay and Adjust Schedule

def predict_bus_delay(bus_id):
    return 0

def adjust_schedule(bus_schedule, delay):
    adjusted_schedule = bus_schedule.copy()
    for idx, row in adjusted_schedule.iterrows():
        departure_time = datetime.combine(datetime.today(), row['departure_time']) + timedelta(minutes=delay)
        adjusted_schedule.at[idx, 'departure_time'] = departure_time.time()
        arrival_time = datetime.combine(datetime.today(), row['arrival_time']) + timedelta(minutes=delay)
        adjusted_schedule.at[idx, 'arrival_time'] = arrival_time.time()
    return adjusted_schedule

delay = predict_bus_delay(1) # Example for bus_id = 1
bus_schedule = adjust_schedule(bus_schedule, delay)

### 4. Manage Bus Capacity and Schedule Changes

def check_and_adjust_capacity(passenger_data, bus_schedule, bus_capacity=50):
    # Ensure 'total count' is present in the passenger_data
    if 'total count' not in passenger_data['location'].str.lower().values:
        raise ValueError("'total count' not found in passenger_data")

    # Extract total count and ensure it's an integer
    total_count_value = passenger_data.loc[passenger_data['location'].str.lower() == 'total count', 'count'].values[0]
    total_count_value = int(total_count_value)

    buses_needed = (total_count_value + bus_capacity - 1) // bus_capacity
    current_time = datetime.now().time()

    # Determine buses currently in motion
    buses_in_motion = bus_schedule[
        (bus_schedule['departure_time'] <= current_time) & (bus_schedule['arrival_time'] >= current_time)
    ]
    current_buses_in_motion = len(buses_in_motion)

    # If more buses are needed, adjust the next departing bus time
    if buses_needed > current_buses_in_motion:
        # Get the next bus that will depart after the current time
        next_bus = bus_schedule[bus_schedule['departure_time'] > current_time].iloc[0]
        next_bus_idx = bus_schedule[bus_schedule['departure_time'] > current_time].index[0]

        # Adjust departure time (e.g., 5 minutes earlier)
        new_departure_time = (datetime.combine(datetime.today(), next_bus['departure_time']) - timedelta(minutes=5)).time()
        bus_schedule.at[next_bus_idx, 'departure_time'] = new_departure_time

    return bus_schedule

bus_schedule = check_and_adjust_capacity(passenger_data, bus_schedule)

def save_bus_schedule(bus_schedule, file_path):
    bus_schedule.to_csv(file_path, index=False)

# Save the updated bus schedule
save_bus_schedule(bus_schedule, 'My SIH\\bus_schedule.csv')

