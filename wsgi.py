import sys
from flask import Flask


sys.path.insert(0, "/app")  # Replace with the path to your Flask app

# Load the Flask app
app = Flask(__name__)

# Import the Flask app from app.py
from app import app as application  # 'app' is the Flask app instance in app.py
