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
from ingestdata import format_estimated_time
from classes.prototypelab import PrototypeLab
from classes.prototypelabplots import PrototypeLabPlots
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file, flash, send_from_directory
from datetime import datetime
from datetime import timedelta

dotenv.load_dotenv()

config = {
    "SECRET_KEY": os.getenv('SECRET_KEY'),
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

server = Flask(__name__)
bcrypt = Bcrypt(server)
server.config.from_mapping(config)

lab = PrototypeLab("database.db")

"""
    Views
"""

# add a route for 404 errors
@server.errorhandler(404)
def page_not_found(e):
    referer = request.headers.get("Referer")
    if referer is None:
        referer = url_for("index")

    return render_template('404.html', referer=referer), 404

@server.route('/')
def index():
    logout()
    return render_template("index.html")

