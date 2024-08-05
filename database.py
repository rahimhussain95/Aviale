import csv
import sqlite3

conn = sqlite3.connect('aviation.db')
cursor = conn.cursor()

with open('static/airlines.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader, None)

    for row in reader:
        cursor.execute("INSERT INTO airlines (id, airline, IATA, ICAO, callsign, country, active) VALUES (?, ?, ?, ?, ?, ?, ?)"
        , row )

conn.commit()
conn.close()

