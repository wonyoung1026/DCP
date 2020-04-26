from flaskApp import instanceApp
from flaskApp.instance_api.controllers import contConfigController
from flask import request

# "/html-system-spec-check?provider-endpoint=ec2-100-27-21-76.compute-1.amazonaws.com"
# provider_endpoint="ec2-100-27-21-76.compute-1.amazonaws.com"

# @instanceApp.route('/create-container')
# def create_container():
#     provider_endpoint = request.args.get("provider-endpoint")
#     return contConfigController.createBaseContainer(provider_endpoint)
    
# @instanceApp.route('/run-container')
# def run_container():
#     buyer_endpoint = request.args.get("buyer-endpoint")
#     provider_endpoint = request.args.get("provider-endpoint")
#     buyer_id = request.args.get("buyer-id")
#     password = request.args.get("password")
#     public_key = request.args.get("public-key")
#     port_num = request.args.get("port-num")
#     return contConfigController.runContainer(buyer_endpoint, provider_endpoint, buyer_id, password, public_key, port_num)

# @instanceApp.route('/terminate-container')
# def terminate_container():
#     provider_endpoint = request.args.get("provider-endpoint")
#     buyer_id = request.args.get("buyer-id")
#     return contConfigController.terminateContainer(provider_endpoint, buyer_id)

"""
@instanceApp.route('/check-port')
def check_port():
    provider_endpoint = request.args.get("provider-endpoint")
    port_num = request.args.get("port-num")
    return contConfigController.checkPort(provider_endpoint, port_num)
"""