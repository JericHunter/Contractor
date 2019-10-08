from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import reduce
import os

app = Flask(__name__)


@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html')
