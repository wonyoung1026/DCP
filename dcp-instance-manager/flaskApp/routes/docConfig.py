from flaskApp import instanceApp
from flaskApp.instance_api.controllers import docConfigController
from flask import request

@instanceApp.route('/')
def normal():
    return "<h1>'Instance Manager App'</h1>"

@instanceApp.route('/container/<string:container_id>/create')
def createContainer(container_id):
    return docConfigController.getCreateContainer(container_id)

@instanceApp.route('/container/<string:container_id>/start')
def startContainer(container_id):
    return docConfigController.getStartContainer(container_id)

@instanceApp.route('/container/<string:container_id>/stop',)
def stopContainer(container_id):
    return docConfigController.getStopContainer(container_id)

@instanceApp.route('/container/<string:container_id>/terminate')
def terminateContainerWithoutSave(container_id):
    return docConfigController.getTerminateContainerWithoutSave(container_id)
@instanceApp.route('/container/<string:container_id>/terminate/s')
def terminateContainerWithSave(container_id):
    return docConfigController.getTerminateContainerWithSave(container_id)

@instanceApp.route('/vm/container/<string:vm_id>/terminate')
def terminateVMMonitorContainer(vm_id):
    return docConfigController.getTerminateVMMonitorContainer(vm_id)

