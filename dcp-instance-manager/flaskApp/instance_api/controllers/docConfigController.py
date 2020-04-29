import subprocess
from subprocess import Popen, PIPE
from flask import jsonify, make_response, request
from . import helper
import os
import json


# ====================================================================
# Create and start container on buyer purchase
# ====================================================================
def getCreateContainer(container_id):
    base_image_id = request.get_json().get("baseImageID")
    ip_address = request.get_json().get("ipAddress")
    gpu_ids = request.get_json().get("gpuIDs")

    # TODO: docker image only available in lower cases. Need fix 
    base_image_id = base_image_id.lower()
    base_image_repo_name = "{}/{}".format(os.getenv("DCP_DOCKER_REPO_BASE"), base_image_id)

    # Run container on provider host
    # TODO: remove sudo in prod. Need to check if reboot command via SSH actually reboots EC2 used during test
    ssh_user = os.getenv("MASTER_USERNAME")
    ssh_auth_key= os.getenv("MASTER_PUBLIC_KEY")
    

    port_low = 45000
    port_high = 65535
    try:
        command_list = [
            # GET random free port between low and high
            "PORT=comm -23 <(seq {low} {high} | sort) <(ss -Htan | awk \'{{print $4}}' | cut -d\':\' -f2 | sort -u) | shuf | head -n 1 && \
             sudo docker run -dit --restart always --name {cname} -p $PORT:22 --env \"SSH_USER={sshuser}\" --env \"SSH_SUDO=ALL=(ALL) NOPASSWD:ALL\" --env \"SSH_AUTHORIZED_KEYS={sshauth}\" {baseimage} && \
             sudo docker port {cname} 22/tcp".format(
                low=port_low, high=port_high, cname=str(container_id), 
                sshuser=str(ssh_user), sshauth=str(ssh_auth_key), baseimage=str(base_image_repo_name)
            )
        ]
        ssh_process = helper.createSshProcess(ip_address, command_list)
        ssh_output, ssh_errors = ssh_process.communicate()
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while creating container on provider host machine"}),500)

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while creating container on provider host machine",
                        "output": ssh_output,
                        "error": ssh_errors}), 400)

    # Get assigned port
    # destination_port = int(ssh_output.splitlines()[-1].split(":")[-1])
    destination_port = ssh_output.splitlines()[-1].split(":")[-1]
    ssh_tunnel_image = os.getenv("DCP_SSH_TUNNEL_IMAGE")
    destination_user = os.getenv("MASTER_USERNAME")

    try:
        # Create and start ssh tunnel container
        subproc_result = subprocess.run(["docker", "run", "-dit", 
                    "--restart", "always", 
                    "--name", str(container_id),
                    "--env", "DESTINATION_CONTAINER_NAME={}".format(str(container_id)), 
                    "--env", "DESTINATION_IP={}".format(str(ip_address)), 
                    "--env", "DESTINATION_PORT={}".format(str(destination_port)), 
                    "--env", "DESTINATION_USER={}".format(str(destination_user)),
                    str(ssh_tunnel_image)])

    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while creating tunnel container"}),500)

    

    return make_response(jsonify({"message":"Docker container create success"}),200)


# ====================================================================
# Start container
# ====================================================================
def getStartContainer(container_id):
    ip_address = request.get_json().get("ipAddress")
    gpu_ids = request.get_json().get("gpuIDs")
    
    # Start container on provider side
    try:
        command_list = [
            "sudo docker start --restart always {cname} && \
            sudo docker port {cname} 22/tcp ".format(cname=str(container_id))
        ]
        ssh_process = helper.createSshProcess(ip_address, command_list)
        ssh_output, ssh_errors = ssh_process.communicate()
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while starting container on provider host machine"}),500)

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while starting tunnel container",
                        "output": ssh_output,
                        "error": ssh_errors}), 400)

    # Start tunnel container
    # Need string conversion to avoid string type problem
    try:
        cmd = ["docker", "start", "--restart", "always", str(container_id)]
        subprocess.run(cmd)
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while starting tunnel container"}),500)
    

    return make_response(jsonify({"output": container_id, "message":"Container start success"}),200)

# ====================================================================
# Stop container
# ====================================================================
def getStopContainer(container_id):
    ip_address = request.get_json().get("ipAddress")

    # Stop container (+ detach GPU) on provider side
    try:
        command_list = [
            "sudo docker stop {}".format(str(container_id))
        ]
        ssh_process = helper.createSshProcess(ip_address, command_list)
        ssh_output, ssh_errors = ssh_process.communicate()
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while stopping container on provider host machine"}),500)

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while stopping tunnel container",
                        "output": ssh_output,
                        "error": ssh_errors}), 400)


    # Stop tunnel container
    try:
        subprocess.run(["docker", "stop", str(container_id)])
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while stopping tunnel container"}), 500)
    

    return make_response(jsonify({"output": container_id, "message":"Container stop success"}),200)

# ====================================================================
# Terminate container WITHOUT save
# ====================================================================
def getTerminateContainerWithoutSave(container_id):
    ip_address = request.get_json().get("ipAddress")

    # Terminate contanier on provider side
    try:
        command_list = [
            "sudo docker stop {} && sudo docker rm {}".format(str(container_id), str(container_id))
        ]
        ssh_process = helper.createSshProcess(ip_address, command_list)
        ssh_output, ssh_errors = ssh_process.communicate()
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while terminating container on provider host machine"}),500)

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while terminating tunnel container",
                        "output": ssh_output,
                        "error": ssh_errors}), 400)

    # Terminate tunnel container
    try:
        subprocess.run(["docker", "stop", str(container_id)])
        subprocess.run(["docker", "rm", str(container_id)])
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while terminating tunnel container"}),500)
    

    return make_response(jsonify({"output": container_id, "message":"Docker container create success"}),200)

# ====================================================================
# Terminate container WITH save
# ====================================================================
def getTerminateContainerWithSave(container_id):
    ip_address = request.get_json().get("ipAddress")

    # TODO: Commit container, Push to registry, and Terminate contanier on provider side 

    # Terminate tunnel container
    try:
        subprocess.run(["docker", "stop", str(container_id)])
        subprocess.run(["docker", "rm", str(container_id)])
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while terminating tunnel container"}),500)
    

    return make_response(jsonify({"output": container_id, "message":"Docker container create success"}),200)


# ====================================================================
# Terminate vm monitor container
# ====================================================================
def getTerminateVMMonitorContainer(vm_id):
    ip_address = request.get_json().get("ipAddress")


    # Terminate monitor container
    try:
        subprocess.run(["docker", "stop", str(vm_id)])
        subprocess.run(["docker", "rm", str(vm_id)])
    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while terminating tunnel container"}),500)
    

    return make_response(jsonify({"output": vm_id, "message":"Docker container create success"}),200)