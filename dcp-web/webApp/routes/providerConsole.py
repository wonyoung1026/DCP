from webApp import webApp, status_is_error, status_is_success
from flask import render_template, redirect, request, Blueprint, abort, jsonify
import json
from webApp.api.controllers import authController, providerController, mainController
from webApp.api.middlewares.auth import providerCheck
from webApp.api.models.userModel import User
bp = Blueprint("provider", __name__)


# @webApp.route('/console/buyer/<string: user_email>/sold')
# def buyer_sold_vm():
#     return render_template('buyerHome.html')

@bp.route('/')
@providerCheck
def home():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('provider/home.html', user=user)

@bp.route('/dashboard')
@providerCheck
def dashboard():
    user = authController.getUserWithSessionCookie().toJson()
    res = providerController.getMyDashboard()
    dashboard_data = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)
    

    return render_template('provider/dashboard.html', user=user, dashboard_data =dashboard_data)

@bp.route('/vm')
@providerCheck
def vmSold():
    user = authController.getUserWithSessionCookie().toJson()
    res = providerController.getMyVMs()
    vm_list = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)

    return render_template('provider/myVMPage.html', user=user, vm_list=vm_list)

@bp.route('/vm/gpu')
@providerCheck
def vm_on_sale():
    user = authController.getUserWithSessionCookie().toJson()
    res = providerController.getMyGPUs()
    gpu_list = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)
    return render_template('provider/myGPUPage.html', user=user, gpu_list=gpu_list)

@bp.route('/vm/marketplace')
@providerCheck
def vmMarketplace():
    user = authController.getUserWithSessionCookie().toJson()
    res = mainController.getVMs()
    vm_list = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)

    return render_template('provider/vmMarketplaceSearchPage.html', user=user, vm_list=vm_list)

@bp.route('/vm/marketplace/sell')
@providerCheck
def vmMarketplaceSell():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('provider/vmMarketplaceSellPage.html', user=user)

@bp.route('/vm/marketplace/sell2')
@providerCheck
def vmMarketplaceSell2():
    user = authController.getUserWithSessionCookie().toJson()
    res = providerController.getPreregisterVM()
    vm = res.get("output")
    message = res.get("message")
    status = res.get("status")
    
    if status_is_error(status):
        abort(status, message)

    return render_template('provider/vmMarketplaceSellPage2.html', user=user, vm= vm), status

    
@bp.route('/vm/marketplace/favorites')
@providerCheck
def myVMList():
    user = authController.getUserWithSessionCookie().toJson()
    res = mainController.getFavoriteVMs()
    favorite_vms = res.get("output")
    message = res.get("message")
    status = res.get("status")

    if status_is_error(status):
        abort(status, message)

    return render_template('provider/myFavoriteVMListPage.html', user=user,vm_list=favorite_vms)

@bp.route('/billing')
@providerCheck
def billing():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('provider/billing.html', user=user)

@bp.route('/support/contact-us')
@providerCheck
def contactUs():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('provider/contactUs.html', user=user)

@bp.route('/support/faq')
@providerCheck
def faq():
    user = authController.getUserWithSessionCookie().toJson()
    return render_template('provider/FAQ.html', user=user)


webApp.register_blueprint(bp, url_prefix='/console/provider')