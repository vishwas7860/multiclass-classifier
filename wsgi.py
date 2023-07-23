import sys
import logging
from flask import Flask

# Set up logging (optional)
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/path/to/your/app")  # Replace with the path to your Flask app

# Load the Flask app
app = Flask(__name__)

# Import the Flask app from app.py
from app import app as application  # 'app' is the Flask app instance in app.py
