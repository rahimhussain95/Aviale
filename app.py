import datetime
import sqlite3
from api import query

from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/status", methods =["GET", "POST"])
def status():
    if request.method == "POST":

        airline = request.form.get("airline")
        flightnumber = request.form.get("flightNo")

        conn = sqlite3.connect('aviation.db')
        db = conn.cursor()

        flightIATA = db.execute("SELECT IATA FROM airlines WHERE airline = ?", (airline,)).fetchone()[0]
        flight_data = query(flightIATA + flightnumber)

        departure_airport = flight_data['data'][0]['departure']['airport']

        return render_template("status.html", departure=departure_airport);

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)