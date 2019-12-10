import flask
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, safe_join, abort
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/buscarInfo', methods=['GET', 'POST'])
def buscarData():
    