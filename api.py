from flask import Flask, redirect, render_template, request, Blueprint, jsonify
import requests
from dotenv import load_dotenv
import os

flight_ap = Blueprint('api', __name__)

#Aviation Stack API
SOURCE_URL = os.getenv('SOURCE')
KEY = os.getenv('AERO_API_KEY')

def query(flight_info):
    endpoint = f"{SOURCE_URL}flights"

    params = {
        'access_key': KEY,
        'flight_iata': flight_info
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {'error': 'Failed to fetch flight information'}
    
