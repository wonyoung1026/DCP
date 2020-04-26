from flaskApp import instanceApp
from flaskApp.instance_api.controllers import vmMonitorController
from flask import request


@instanceApp.route('/update-vmMetric')
def update_metric():
    provider_endpoint = request.args.get("provider-endpoint")
    return vmMonitorController.cpuMonitor(provider_endpoint)