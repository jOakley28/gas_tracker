import os
import json
import jsonify
import dotenv
import base64
import plotly
import sqlite3
import pandas as pd
from html import unescape
import plotly.express as px
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file, flash, send_from_directory
from datetime import datetime
from datetime import timedelta
from classes.gas import Gas 

dotenv.load_dotenv()

config = {
    "SECRET_KEY": os.getenv('SECRET_KEY'),
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

server = Flask(__name__)
bcrypt = Bcrypt(server)
server.config.from_mapping(config)

gas = Gas("database.db")

"""
    Views
"""

# add a route for 404 errors
@server.errorhandler(404)
def page_not_found(e):
    referer = request.headers.get("Referer")
    if referer is None:
        referer = url_for("home")
    return render_template('404.html', referer=referer), 404

@server.route('/resources/<path:path>')
def send_resources(path):
    return send_file(f"resources/{path}")

@server.route('/')
def home():
    return render_template('index.html')

@server.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        owner = request.form['owner']
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        tank_size = float(request.form['tank_size'])
        
        if gas.add_car(owner, make, model, year, tank_size):
            return redirect('/')
        else:
            flash('Error adding car.', 'error')
            
    return render_template('add_car.html')

@server.route('/add_gas', methods=['GET', 'POST'])
def add_gas():
    cars = gas.get_all_cars()
    
    if request.method == 'POST':
        # get form data and add gas record to database
        car_id = request.form['car_id']
        cost = request.form['cost']
        amount = request.form['amount']
        distance = request.form['distance']
        phase = request.form['phase']
        
        if gas.add_gas(car_id, cost, amount, distance, phase):
            flash('Gas record added successfully!', 'success')
            return redirect('fill_up_summary')
        else:
            flash('Error adding gas record.', 'error')
    
    return render_template('add_gas.html', cars=cars)

@server.route('/api/phase/<car_id>')
def get_phase(car_id):
    return jsonify(gas.get_phases_by_car(car_id))

@server.route('/fill_up_summary')
def fill_up_summary():
    cars = gas.get_all_cars()
    last_gas = gas.get_last_gas()
    cost_per_gallon = last_gas['cost_per_gallon'].tolist()[0]
    mpg = last_gas['trip_mpg'].tolist()[0]
    cost_per_mile = round(cost_per_gallon/mpg, 2)
    distance_remaining = last_gas['distance_remaining'].tolist()[0]
    phase = last_gas['phase'].tolist()[0]

    return render_template('fill_up_summary.html', 
                           cost_per_gallon=cost_per_gallon, 
                           mpg=mpg,
                           cost_per_mile=cost_per_mile,
                           distance_remaining=distance_remaining,
                           phase=phase, 
                           cars=cars,)

@server.route('/dashboard')
def dashboard():
    cars = gas.get_all_cars()

    gas_table = gas.dashboard_gas_table(3).to_html(index=False, justify='center', classes='table table-striped table-hover table-bordered table-sm justify-content-center')
    print(gas_table)
    # gas_table, cost_per_gal_plot, cost_per_mile_plot, trip_distance_plot, efficacy_plot = gas.dashboard_plots()

    return render_template('dashboard.html', gas_table=gas_table, cars=cars)

@server.route('/trip_calculator', methods=['GET', 'POST'])
def trip_calculator():
    cars = gas.get_all_cars()
    return render_template('trip_calculator.html', cars=cars)

@server.route('/api/trip_cost/<int:trip_length>/<int:car_id>')
def trip_cost(trip_length, car_id):
    return jsonify(gas.trip_cost(car_id, trip_length))

# main loop
if __name__ == '__main__':  
    if gas.db_size() == 0:
        print("Creating database tables...")
        with open("schema.sql") as f:
            db_connection = sqlite3.connect("database.db")
            db_connection.executescript(f.read())

    server.run(
        debug=True,
        host=os.getenv('IP'),
        port=3000
    )

