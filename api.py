from flask import Flask, redirect, render_template, request, Blueprint, jsonify
import requests

flight_ap = Blueprint('api', __name__)

#Aviation Stack API
SOURCE_URL = 'http://api.aviationstack.com/v1/'
KEY = 'dcb9a120af503f155746458d12d3fd3d'

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
    
