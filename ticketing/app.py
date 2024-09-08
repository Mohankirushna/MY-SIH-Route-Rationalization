from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

# Route to handle the ticket booking
@app.route('/book-ticket', methods=['POST'])
def book_ticket():
    data = request.json
    starting_point = data.get('startingPoint')
    destination = data.get('destination')
    ticket_count = data.get('ticketCount')

    # Ensure all necessary data is provided
    if not starting_point or not destination or not ticket_count:
        return jsonify({'success': False, 'error': 'Missing data'}), 400

    # Write the data to book-ticket.csv
    try:
        rows = []
        total_count_index = None

        with open('My SIH\\ticketing\\book-ticket.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                # Save the index of the "total count" row
                if row[0].lower() == 'total count':
                    total_count_index = idx
                rows.append(row)

        # Step 2: Update the counts for starting_point, destination, and total count
        updated = False
        for row in rows:
            if row[0].lower() == starting_point.lower() or row[0].lower() == destination.lower():
                row[1] = str(int(row[1]) + ticket_count)  # Update the count
                updated = True

        if total_count_index is not None:
            rows[total_count_index][1] = str(int(rows[total_count_index][1]) + ticket_count)  # Update the total count

        # Step 3: Write the updated data back to the CSV file
        with open('My SIH\\ticketing\\book-ticket.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if updated:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Locations not found in CSV'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
