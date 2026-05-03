# config.py
# ------------------------------------------------------------
# Loads database and Flask configuration from a .env file
# using python-dotenv. This keeps credentials out of source
# code and out of GitHub.
#
# To set up: copy .env.example → .env and fill in your values.
# Install dependency: pip install python-dotenv
# ------------------------------------------------------------

import mysql.connector as connector
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")  
#Load environment variables from .env file

DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", 3306))
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME     = os.getenv("DB_NAME", "evcs_security")

FLASK_HOST  = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT  = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"