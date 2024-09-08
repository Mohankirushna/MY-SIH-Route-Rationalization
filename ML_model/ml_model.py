import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


# Update the path to the CSV file
df = pd.read_csv('My SIH\\model\\traffic_data_two_weeks.csv')
df.head()

# Convert 'departure_time' to datetime and extract hour and day of the week
df['departure_time'] = pd.to_datetime(df['departure_time'])
df['hour'] = df['departure_time'].dt.hour
df['day_of_week'] = df['departure_time'].dt.dayofweek

# Check for missing values
df.isnull().sum()

# Drop rows with missing values, if any
df.dropna(inplace=True)

# Select the relevant features for training
X = df[['distance_meters','duration_seconds', 'hour', 'day_of_week']]
y = df['delay']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Calculate Percentage Error
percentage_errors = np.abs((y_test - y_pred) / y_test) * 100
mean_percentage_error = np.mean(percentage_errors)
print(f"Mean Percentage Error: {mean_percentage_error}%")

r2 = r2_score(y_test, y_pred)

results_df = pd.DataFrame({'Expected': y_test, 'Predicted': y_pred})

print("R² Score:", r2)
print(results_df.head())

plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Prediction')
plt.xlabel('Expected Delay')
plt.ylabel('Predicted Delay')
plt.title('Actual vs Predicted Delay')
plt.legend()
plt.show()


joblib.dump(model, 'delay_predictor_model_1.joblib')
