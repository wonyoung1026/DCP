
from flaskApp import instanceApp
from flaskApp.instance_api.controllers import remoteHostController
from flask import request, Blueprint

bp = Blueprint("remote", __name__)

@bp.route('/provider/init')
def providerInitSetup():
    return remoteHostController.getProviderInitSetup()

@bp.route('/provider/spec/html')
def htmlSystemSpecCheck():
    return remoteHostController.getHTMLSystemSpecCheck()

@bp.route('/provider/spec')
def systemSpeccheck():
    return remoteHostController.getSystemSpecCheck()

instanceApp.register_blueprint(bp, url_prefix='/remote')