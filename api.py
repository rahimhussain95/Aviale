from flask import Flask, redirect, render_template, request, Blueprint, jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

flight_ap = Blueprint('api', __name__)

#Aviation Stack API
SOURCE_URL = os.getenv('AERO_API_SOURCE')
KEY = os.getenv('AERO_API_KEY')

HEADERS = {'x-apikey': KEY}

def get_flight_data(ident, ident_type='designator'):
    endpoint = f"{SOURCE_URL}/flights/{ident}"

    params = {
        'ident_type': ident_type,
        'max_pages': 1
    }

    response = requests.get(endpoint, headers=HEADERS, params=params)

    if response.status_code == 200:
        raw_data = response.json().get('flights', [])
        return raw_data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {"Error': 'Failed to fetch flight information"}

def find_user_flight(flights, origin=None, destination=None):
    current_flight = [flight for flight in flights if flight['status'].startswith('En Route')]

    if origin and destination:
        matched_flights = [flight for flight in flights if 
                           flight['origin']['code_iata'] == origin and 
                           flight['destination']['code_iata'] == destination]

        # Sort by priority: En Route > Scheduled > Arrived
        en_route = [flight for flight in matched_flights if flight['status'].startswith('En Route')]
        scheduled = sorted([flight for flight in matched_flights if flight['status'] == 'Scheduled'], 
                            key=lambda x: x['scheduled_out'])
        arrived = sorted([flight for flight in matched_flights if flight['status'].startswith('Arrived')], 
                          key=lambda x: x['actual_in'], reverse=True)

        # Return the highest priority flight
        return en_route[0] if en_route else (scheduled[0] if scheduled else arrived[0] if arrived else None)
    
    # Default to the current En Route flight if no filters are provided
    return current_flight[0] if current_flight else None

# def filter_data():
