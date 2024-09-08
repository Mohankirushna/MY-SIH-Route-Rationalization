from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the stops and their order
stops = [
    "thambaram",
    "Irumbuliyur",
    "Peerkankaranai",
    "Perungalathur",
    "Police Check Post",
    "Vandalur Railway Station Gate",
    "vandalur"
]

# Load passenger data CSV file
def load_passenger_data():
    return pd.read_csv('My SIH\\ticketing\\book-ticket.csv')

# Save updated passenger data back to the CSV
def save_passenger_data(df):
    df.to_csv('My SIH\\ticketing\\book-ticket.csv', index=False)

# Function to update passenger data based on ticket request
def update_passenger_data(start, destination, ticket_count):
    df = load_passenger_data()

    # Find indices of start and destination
    start_index = stops.index(start)
    dest_index = stops.index(destination)

    # Determine if the route is from Thambaram to Vandalur or Vandalur to Thambaram
    if start_index < dest_index:
        # Thambaram to Vandalur route
        df.loc[start_index, 'count_tbm'] += ticket_count
        df.loc[dest_index, 'count_tbm'] += ticket_count
        df.loc[df['tbm'] == 'total count_tbm', 'count_tbm'] += ticket_count
    else:
        # Vandalur to Thambaram route
        df.loc[start_index, 'count_van'] += ticket_count
        df.loc[dest_index, 'count_van'] += ticket_count
        df.loc[df['van'] == 'total count_van', 'count_van'] += ticket_count

    # Save updated data back to CSV
    save_passenger_data(df)

# Route to handle ticket booking requests
@app.route('/book-ticket', methods=['POST'])
def book_tickets():
    # Get the input data from the request
    data = request.get_json()
    start = data['startingPoint']
    destination = data['destination']
    ticket_count = data['ticketCount']

    # Update the passenger data CSV file
    update_passenger_data(start, destination, ticket_count)

    return jsonify({"message": "Ticket booking data updated successfully."})

if __name__ == '__main__':
    app.run(debug=True)
