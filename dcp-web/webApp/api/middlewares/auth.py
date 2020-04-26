from functools import wraps
from flask import request

from webApp.api.controllers import authController
from webApp.api.models.userModel import User

def userCheck(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = authController.getUserWithSessionCookie()
        if not isinstance(res, User):
            return res
        return f(*args, **kwargs)
    return decorated_function

def providerCheck(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = authController.getUserWithSessionCookie()
        if not isinstance(res, User) or not res.isProvider:
            return res
        return f(*args, **kwargs)
    return decorated_function

def buyerCheck(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = authController.getUserWithSessionCookie()
        if not isinstance(res, User) or not res.isBuyer:
            return res
        return f(*args, **kwargs)
    return decorated_function