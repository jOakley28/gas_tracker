import os
import json
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
            return redirect('/')
        else:
            flash('Error adding gas record.', 'error')
    
    return render_template('add_gas.html', cars=cars)

@server.route('/api/phase/<car_id>')
def get_phase(car_id):
    return jsonify(gas.get_phases_by_car(car_id))

@server.route('/dashboard')
def dashboard():
    cars = gas.get_all_cars()

    gas_table = gas.dashboard_gas_table(3).to_html(index=False, justify='center', classes='table table-striped table-hover table-bordered table-sm justify-content-center')
    print(gas_table)
    # gas_table, cost_per_gal_plot, cost_per_mile_plot, trip_distance_plot, efficacy_plot = gas.dashboard_plots()

    return render_template('dashboard.html', gas_table=gas_table, cars=cars)


if __name__ == '__main__':
    gas = Gas("database.db")  # create an instance of Gas
    if gas.db_size() == 0:
        print("Creating database tables...")
        with open("schema.sql") as f:
            db_connection = sqlite3.connect("database.db")
            db_connection.executescript(f.read())

    server.run(
        debug=True,
        host=os.getenv('IP'),
        port=8080
    )

