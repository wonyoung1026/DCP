from flask import Flask
from flask_cors import CORS
import firebase_admin 
import os

# -------------------------------------------------
# Create Flask app 
# -------------------------------------------------
instanceApp = Flask(__name__)

CORS(instanceApp)

# -------------------------------------------------
# Create firebase app
# -------------------------------------------------
cred = firebase_admin.credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_app = firebase_admin.initialize_app(cred)

# -------------------------------------------------
# Import routes
# -------------------------------------------------

from .routes import docConfig
from .routes import remote
from .routes import contConfig
from .routes import monitConfig





