from datetime import datetime
from api import *
from database import *
from flask import Flask, flash, redirect, render_template, request, jsonify

app = Flask(__name__)

# app.register_blueprint(flight_ap, url_prefix='/api')

@app.route("/")
def index():
    return render_template("index.html");

@app.route('/autocomplete/airports', methods=['GET'])
def airport_complete():
    query = request.args.get('query', '')
    if query:
        results = query_airports(query)
        suggestions = [
            {"IATA": row['IATA'], "display": f"({row['IATA']}) {row['city']}"} for row in results
        ]
        return jsonify(suggestions)
    return jsonify([])

@app.route('/autocomplete/airlines', methods=['GET'])
def airline_complete():
    query = request.args.get('query', '')
    if query:
        results = query_airlines(query)
        suggestions = [
            {"IATA": row['IATA'], "display": f"({row['IATA']}) {row['airline']}"} if row['IATA']
            else {"IATA": None, "display": row['airline']}
            for row in results
        ]
        return jsonify(suggestions)
    return jsonify([])


@app.route("/data")
def test():
    ident = "UAL4"
    flight_data = get_flight_data(ident)
    return jsonify(flight_data)

@app.route("/status", methods =["GET", "POST"])
def status():
    if request.method == "POST":

        airline = request.form.get("airline")
        flightnumber = request.form.get("flightNo")
        departure = request.form.get("Departure")
        arrival = request.form.get("Arrival")
        icao = request.form.get("AirlineICAO")

        flight_param = f"{icao}{flightnumber}"
        flight_data = get_flight_data(flight_param)

        user_flight = find_user_flight(flight_data, departure, arrival)

        fa_flight_id = user_flight.get("fa_flight_id", "N/A") if user_flight else "N/A"

        return render_template("status.html", flight=user_flight, )




        conn = sqlite3.connect('aviation.db')
        db = conn.cursor()

        flightIATA = db.execute("SELECT IATA FROM airlines WHERE airline = ?", (airline,)).fetchone()[0]
       # flight_data = query(flightIATA + flightnumber)
        flight_info = flight_data['data'][0]

        departure_details = {
            "departure_airport": flight_info['departure']['airport'],
            "departure_iata": flight_info['departure']['iata'],
            "departure_terminal": flight_info['departure']['terminal'],
            "departure_gate": flight_info['departure']['gate'],
            "departure_scheduled": datetime.fromisoformat(flight_info['departure']['scheduled']).strftime("%I:%M %p"),
        }

        arrival_details = {
            "arrival_airport": flight_info['arrival']['airport'],
            "arrival_iata": flight_info['arrival']['iata'],
            "arrival_terminal": flight_info['arrival']['terminal'],
            "arrival_gate": flight_info['arrival']['gate'],
            "arrival_scheduled": datetime.fromisoformat(flight_info['arrival']['scheduled']).strftime("%I:%M %p"),
        }

        conn.close()

        return render_template("status.html", **departure_details, **arrival_details)

    return render_template("status.html")

@app.route("/stack")
def stack():
    return render_template("stack.html");

if __name__ == '__main__':
    app.run(debug=True)