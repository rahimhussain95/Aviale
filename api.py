from flask import Flask, redirect, render_template, request, Blueprint, jsonify
import requests
from dotenv import load_dotenv
import os

flight_ap = Blueprint('api', __name__)

#Aviation Stack API
SOURCE_URL = os.getenv('SOURCE')
KEY = os.getenv('AERO_API_KEY')

HEADERS = {'x-apikey': KEY}

def query_flight(ident, ident_type='designator'):
    endpoint = f"{SOURCE_URL}flights/{ident}"

    params = {
        'ident_type': ident_type,
        'max_pages': 1
    }

    response = requests.get(endpoint, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print{f"Error: {response.status_code}, {response.text}"}
        return {'error': 'Failed to fetch flight information'}
    
