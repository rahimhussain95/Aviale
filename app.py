from datetime import datetime
import sqlite3
from api import query_flight, flight_ap

from flask import Flask, flash, redirect, render_template, request, jsonify

app = Flask(__name__)

app.register_blueprint(flight_ap, url_prefix='/api')

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/data")
def test():
    ident = "UAL4"
    flight_data = query_flight(ident)
    return jsonify(flight_data)

@app.route("/status", methods =["GET", "POST"])
def status():
    if request.method == "POST":

        airline = request.form.get("airline")
        flightnumber = request.form.get("flightNo")

        conn = sqlite3.connect('aviation.db')
        db = conn.cursor()

        flightIATA = db.execute("SELECT IATA FROM airlines WHERE airline = ?", (airline,)).fetchone()[0]
        flight_data = query(flightIATA + flightnumber)
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

    return redirect("/")

@app.route("/stack")
def stack():
    return render_template("stack.html");
