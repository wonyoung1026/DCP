from flask import make_response, jsonify, request, redirect
from webApp import webApp

from webApp.api.middlewares.auth import providerCheck, buyerCheck, userCheck
from webApp.api.controllers import mainController

import os


@webApp.route('/user/vm')
@userCheck
def getVMs():
    res = mainController.getVMs()
    vm_list = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output':vm_list, 'message': message}), status)

@webApp.route('/user/vm/<string:vm_id>')
@userCheck
def getUserVMByID(vm_id):
    res = mainController.getVMByID(vm_id)
    vm = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output':vm, 'message': message}), status)

@webApp.route('/user/vm/<string:vm_id>/full')
@userCheck
def getUserVMFullByID(vm_id):
    res = mainController.getVMFullByID(vm_id)
    spec_html = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output':spec_html, 'message': message}), status)

@webApp.route('/user/vm/<string:vm_id>/monitor')
@userCheck
def launchVMMonitor(vm_id):
    res = mainController.getVMMonitorURL(vm_id)
    
    url = res.get("output")
    message = res.get("message")
    status = res.get("status")
    print("URL IS")
    print(url)
    return make_response(jsonify({'output': url, 'message':message}),status)


@webApp.route('/user/vm/<string:vm_id>/favorite', methods=['DELETE', 'POST'])
@userCheck
def favoriteVM(vm_id):
    if request.method == "DELETE":
        res = mainController.deleteFavoriteVM(vm_id)
    elif request.method == "POST":
        res = mainController.postAddFavoriteVM(vm_id)
    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)

@webApp.route('/user/vm/favorite')
@userCheck
def getFavoriteVMs():
    res = mainController.getFavoriteVMs()
    favorite_vms = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': favorite_vms, 'message':message}),status)
@webApp.route('/user/vm/base-image')
@userCheck
def getBaseImages():
    res = mainController.getBaseImages()
    base_images = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': base_images, 'message':message}),status)


