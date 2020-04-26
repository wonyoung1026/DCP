from flask import make_response, jsonify, abort, request
from webApp import webApp, status_is_error, status_is_success

from webApp.api.middlewares.auth import providerCheck
from webApp.api.controllers import providerController

@webApp.route("/provider/vm/pre-register-spec")
@providerCheck
def getProviderVMPreregisterSpec():
    res = providerController.getPreregisterVM()
    vm = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': vm, 'message':message}),status)


@webApp.route("/provider/vm/<string:vm_id>/hide")
@providerCheck
def getProviderVMHide(vm_id):
    res = providerController.hideMyVM(vm_id)
    vm_id = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': vm_id, 'message':message}),status)
@webApp.route("/provider/vm/<string:vm_id>/show")
@providerCheck
def getProviderVMShow(vm_id):
    res = providerController.showMyVM(vm_id)
    vm_id = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': vm_id, 'message':message}),status)



@webApp.route("/provider/vm/<string:vm_id>", methods=['UPDATE','DELETE', 'GET'])
@providerCheck
def provider_vm(vm_id):
    if request.method == 'UPDATE':
        res = providerController.updateMyVM(vm_id)
    elif request.method == "DELETE":
        res = providerController.terminateMyVM(vm_id)
    elif request.method == "GET":
        res = providerController.getMyVM(vm_id)

    vm_id = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': vm_id, 'message':message}),status)


@webApp.route('/provider/vm', methods=['POST'])
@providerCheck
def postProviderVM():
    res = providerController.postRegisterVM()
    vm = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': vm, 'message':message}),status)

@webApp.route("/provider/vm/gpu/<string:gpu_id>", methods=['UPDATE', 'GET'])
@providerCheck
def providerGPU(gpu_id):
    if request.method == 'UPDATE':
        res = providerController.updateMyGPU(gpu_id)
    elif request.method == 'GET':
        res = providerController.getMyGPU(gpu_id)
    gpu = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': gpu, 'message':message}),status)


@webApp.route('/provider/vm/gpu/<string:gpu_id>/monitoring')
@providerCheck
def getProviderGPUMonitoring(gpu_id):
    res = providerController.getGPUMonitoring(gpu_id)
    gpu_metrics = res.get("output")
    message = res.get("message")
    status = res.get("status")

    return make_response(jsonify({'output': gpu_metrics , 'message':message}),status)