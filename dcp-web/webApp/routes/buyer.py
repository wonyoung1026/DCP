from webApp import webApp
from flask import make_response, jsonify, request, redirect

from webApp.api.middlewares.auth import buyerCheck
from webApp.api.controllers import buyerController
import os 

@webApp.route('/buyer/vm/purchase', methods=['POST'])
@buyerCheck
def buyerVMPurchase():
    res = buyerController.postPurchaseVM()
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'message':message}),status)

@webApp.route('/buyer/container/<string:container_id>/terminate/s', methods=["POST"])
@buyerCheck
def terminateContainerWithSave(container_id):
    res = buyerController.postTerminateMyContainerWithSave(container_id)
    
    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)

@webApp.route('/buyer/container/<string:container_id>/terminate', methods=["POST"])
@buyerCheck
def terminateContainerWithoutSave(container_id):
    res = buyerController.postTerminateMyContainerWithoutSave(container_id)
    
    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)

@webApp.route('/buyer/container/<string:container_id>/start', methods=["POST"])
@buyerCheck
def startMyContainer(container_id):
    res = buyerController.postStartMyContainer(container_id)
    
    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)

@webApp.route('/buyer/container/<string:container_id>/stop', methods=["POST"])
@buyerCheck
def stopMyContainer(container_id):
    res = buyerController.postStopMyContainer(container_id)
    
    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)



@webApp.route('/buyer/container/<string:container_id>', methods=['GET', 'UPDATE'])
@buyerCheck
def buyerContainer(container_id):
    if request.method == 'GET':
        res = buyerController.getMyContainer(container_id)
    elif request.method == 'UPDATE':
        res = buyerController.updateMyContainer(container_id)

    output = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': output,'message':message}),status)


@webApp.route('/buyer/vm/<string:vm_id>/gpu')
@buyerCheck
def getVMGPUs(vm_id):
    res = buyerController.getVMGPUs(vm_id)
    gpus = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': gpus, 'message':message}),status)

@webApp.route('/buyer/billing/<string:amount>/recharge',methods=['GET'])
@buyerCheck
def rechargeCredit(amount):
    res = buyerController.rechargeUserCredit(amount)
    message = res.get("message")
    status = res.get("status")
    
    return make_response(jsonify({'message': message}), status)

# TODO: change to redirect when CORS issue fixed
# Returns URL for now
@webApp.route('/buyer/container/<string:container_id>/shell')
@buyerCheck
def launchShell(container_id):
    res = buyerController.getShellURL(container_id)
    
    url = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': url, 'message':message}),status)


@webApp.route('/buyer/container/<string:container_id>/monitor')
@buyerCheck
def launchMonitor(container_id):
    res = buyerController.getContainerMonitorURL(container_id)
    
    url = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': url, 'message':message}),status)