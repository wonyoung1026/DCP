from flask import Flask
from flask_cors import CORS
import firebase_admin
import os 

# -------------------------------------------------
# Create Flask app 
# -------------------------------------------------
webApp = Flask(__name__, static_url_path='')

CORS(webApp)

# -------------------------------------------------
# Create firebase app
# -------------------------------------------------
cred = firebase_admin.credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_app = firebase_admin.initialize_app(cred)



# -------------------------------------------------
# Helper function to determine if status code is success
# -------------------------------------------------
def status_is_success(status):
    return True if status >= 200 and status <= 299 else False

def status_is_error(status):
    return True if status >= 400 and status <= 599 else False


# -------------------------------------------------
# Import routes
# -------------------------------------------------
from .routes import loginRegister
from .routes import main
from .routes import buyerConsole
from .routes import providerConsole
from .routes import buyer
from .routes import provider
from .routes import errors