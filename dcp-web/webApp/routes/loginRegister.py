from webApp import webApp
from flask import render_template
from webApp.api.controllers import authController



@webApp.route('/')
def getLoginPage():
    return render_template('login.html')

@webApp.route('/user/forgot-password')
def getForgotPasswordPage():
    return render_template('forgot-password.html')

@webApp.route('/user/register')
def getRegisterPage():
    return render_template('register.html')

@webApp.route('/session-login', methods=['POST'])
def postSessionLogin():
    return authController.sessionLogin()

@webApp.route('/session-logout', methods=['POST'])
def postSessionLogout():   
    return authController.sessionLogout()

@webApp.route('/pre-register', methods=['POST'])
def postPreRegister():
    return authController.preregisterCheck()

@webApp.route('/user', methods=['POST'])
def postUser():
    return authController.createUser()
