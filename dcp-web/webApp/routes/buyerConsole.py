from webApp import webApp, status_is_error, status_is_success
from flask import render_template, redirect, request, Blueprint, abort, jsonify
from webApp.api.controllers import authController, mainController, buyerController
from webApp.api.middlewares.auth import buyerCheck
from webApp.api.models.userModel import User

bp = Blueprint("buyer", __name__)

# TODO: buyer & provider 인지 확인하는 middleware 추가 

@bp.route('/')
@buyerCheck
def home():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/home.html', user=user)


@bp.route('/dashboard')
@buyerCheck
def dashboard():
    user = authController.getUserWithSessionCookie().toJson()
    res = buyerController.getMyDashboard()
    dashboard_data = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)
    

    return render_template('buyer/dashboard.html', user=user, dashboard_data =dashboard_data)
@bp.route('/container')
@buyerCheck
def myContainers():
    user = authController.getUserWithSessionCookie().toJson()
    res = buyerController.getMyContainers()
    container_list = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)
    return render_template('buyer/myContainerPage.html', container_list=container_list, user=user)

@bp.route('/vm/key-pair')
@buyerCheck
def vmKeyPair():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/vmKeyPairsPage.html', user=user)

@bp.route('/vm/marketplace')
@buyerCheck
def vmMarketplace():
    user = authController.getUserWithSessionCookie().toJson()
    res = mainController.getVMs()
    vm_list = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)

    return render_template('buyer/vmMarketplaceSearchPage.html', user=user, vm_list=vm_list)

@bp.route('/vm/marketplace/favorites')
@buyerCheck
def myVMList():
    user = authController.getUserWithSessionCookie().toJson()
    res = mainController.getFavoriteVMs()
    favorite_vms = res.get("output")
    message = res.get("message")
    status = res.get("status")

    if status_is_error(status):
        abort(status, message)
    return render_template('buyer/myFavoriteVMListPage.html', user=user, vm_list=favorite_vms)

@bp.route('/billing')
@buyerCheck
def billing():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/billing.html', user=user)

@bp.route('/billing/recharge')
@buyerCheck
def billingRecharge():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/billingRecharge.html', user=user)

@bp.route('/support/contact-us')
@buyerCheck
def contactUs():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/contactUs.html', user=user)

@bp.route('/support/faq')
@buyerCheck
def faq():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('buyer/FAQ.html', user=user)

webApp.register_blueprint(bp, url_prefix='/console/buyer')