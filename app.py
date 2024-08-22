from flask import Flask, request, jsonify
from datetime import datetime
from dateutil import parser
import uuid
import random
import string

app = Flask(__name__)

# A set to keep track of used tracking numbers for uniqueness (in a real-world application, use a database)
used_tracking_numbers = set()

def generate_tracking_number():
    while True:
        # Generate a random tracking number
        tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        if tracking_number not in used_tracking_numbers:
            used_tracking_numbers.add(tracking_number)
            return tracking_number

@app.route('/next-tracking-number', methods=['GET'])
def next_tracking_number():
    # Extract query parameters
    origin_country_id = request.args.get('origin_country_id')
    destination_country_id = request.args.get('destination_country_id')
    weight = request.args.get('weight')
    created_at = request.args.get('created_at')
    customer_id = request.args.get('customer_id')
    customer_name = request.args.get('customer_name')
    customer_slug = request.args.get('customer_slug')

    # Validate query parameters
    if not origin_country_id or not destination_country_id or not weight or not created_at or not customer_id or not customer_name or not customer_slug:
        return jsonify({"error": "Missing required query parameters"}), 400

    try:
        # Validate weight
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be positive")

        # Validate created_at using dateutil.parser
        parser.parse(created_at)

        # Generate tracking number
        tracking_number = generate_tracking_number()
        response = {
            "tracking_number": tracking_number,
            "created_at": datetime.utcnow().isoformat() + 'Z'  # Return in RFC 3339 format
        }
        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (TypeError, parser.ParserError) as e:
        return jsonify({"error": "Invalid 'created_at' format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
