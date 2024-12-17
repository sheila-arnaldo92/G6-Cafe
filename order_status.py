from flask import Flask, request, render_template_string, jsonify
import mysql.connector
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# MySQL database connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Ararawts2024***",
    "database": "order_status"
}


# Function to connect to the MySQL database and retrieve order data
def get_order_from_db(order_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch order details
    cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()

    # Fetch live location for the order
    cursor.execute("SELECT latitude, longitude, updated_at FROM locations WHERE order_id = %s", (order_id,))
    location = cursor.fetchone()

    cursor.close()
    conn.close()

    return order, location


# Function to update live location in the database
def update_location_in_db(order_id, latitude, longitude):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert or update location for the order
    cursor.execute(
        """
        INSERT INTO locations (order_id, latitude, longitude, updated_at)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE latitude = %s, longitude = %s, updated_at = %s
        """,
        (order_id, latitude, longitude, datetime.now(), latitude, longitude, datetime.now())
    )

    conn.commit()
    cursor.close()
    conn.close()


# HTML template for the webpage
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Status and Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #000000;
            color: #FFFFFF;
        }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background: #222222;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #FFFFFF;
        }
        form {
            text-align: center;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #218838;
        }
        .result, .tracker {
            margin-top: 20px;
            font-size: 18px;
        }
        .error {
            color: red;
            font-weight: bold;
        }
        #map {
            height: 300px;
            width: 100%;
            margin-top: 20px;
            border: 2px solid #fff;
            border-radius: 5px;
        }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBexeMBMyn22oC-7C7uWrRN4yYdE5qTT24"></script>
    <script>
        function initMap(latitude, longitude) {
            const location = { lat: latitude, lng: longitude };
            const map = new google.maps.Map(document.getElementById("map"), {
                zoom: 14,
                center: location
            });
            new google.maps.Marker({ position: location, map: map });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Order Status and Live Tracker</h1>
        <form method="GET" action="/">
            <label for="order_id">Enter Order ID:</label><br>
            <input type="text" id="order_id" name="order_id" placeholder="e.g., 1001" required><br>
            <button type="submit">Check Status</button>
        </form>

        {% if order %}
        <div class="result">
            <p><strong>Order ID:</strong> {{ order_id }}</p>
            <p><strong>Status:</strong> {{ order['status'] }}</p>
            <p><strong>Details:</strong> {{ order['details'] }}</p>
        </div>
        {% if location %}
        <div class="tracker">
            <h3>Live Location</h3>
            <p>Last Updated: {{ location['updated_at'] }}</p>
            <div id="map"></div>
            <script>
                initMap({{ location['latitude'] }}, {{ location['longitude'] }});
            </script>
        </div>
        {% endif %}
        {% elif order_id %}
        <div class="error">
            <p>No order found with ID <strong>{{ order_id }}</strong>.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def check_status():
    """Route to handle order status and location display."""
    order_id = request.args.get("order_id")
    if order_id:
        order, location = get_order_from_db(order_id)
    else:
        order, location = None, None
    return render_template_string(html_template, order=order, location=location, order_id=order_id)


@app.route("/update_location", methods=["POST"])
def update_location():
    """API to update live location."""
    data = request.json
    order_id = data.get("order_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not all([order_id, latitude, longitude]):
        return jsonify({"error": "Missing data"}), 400

    update_location_in_db(order_id, latitude, longitude)
    return jsonify({"success": "Location updated successfully"})


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
