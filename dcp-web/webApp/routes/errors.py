from webApp import webApp
from flask import render_template


@webApp.errorhandler(404)
def pageNotFound(e):
    return render_template('errors/404.html', message=e.description), 404

@webApp.errorhandler(500)
def internalServerError(e):
    return render_template('errors/500.html', message=e.description), 500

@webApp.errorhandler(401)
def unauthorized(e):
    return render_template('errors/401.html', message=e.description), 401
@webApp.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html', message=e.description), 403