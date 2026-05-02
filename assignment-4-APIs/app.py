#Imports
from flask import Flask, request, jsonify
import db_utils
import config

# Creating the APP
app = Flask(__name__)

# Defining valid input

