import subprocess
from subprocess import Popen, PIPE
from flask import jsonify, make_response, request
from . import helper
import os
import json

# ====================================================================
# Initial set up for provider PC
# ====================================================================
def getProviderInitSetup():
    provider_endpoint = str(request.get_json().get("providerEndpoint"))
    vm_id = str(request.get_json().get("vmID"))

    # SCP init set up package
    init_setup_dir_path=os.getenv("LOCAL_DCP_FILES_DIR") #files/DCP
    init_setup_file_name = "setup.sh"
    remote_dir_path = os.getenv("REMOTE_DCP_FILES_DIR")

    scp_process = helper.createScpProcess(init_setup_dir_path, provider_endpoint, "~")
    scp_output, scp_errors = scp_process.communicate()
    

    if scp_process.returncode:
        return make_response(jsonify({"message": "Something went wrong during SCP", 
                        "error": scp_errors,
                        "output": scp_output}), 400)

    # SSH and run init set up script
    scripts_dir_path = "{}/scripts".format(remote_dir_path)
    command_list = [
        "sudo chmod 744 -R {}\n".format(scripts_dir_path),
        "{}/{}\n".format(scripts_dir_path, init_setup_file_name)
    ]
    ssh_process = helper.createSshProcess(provider_endpoint, command_list)
    ssh_output, ssh_errors = ssh_process.communicate()
    

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while running init setup script",
                        "output": ssh_output,
                        "error": ssh_errors}), 400)

    # TODO: uncomment when not on AWS. Reboot on AWS doesn't work automatically. 
    # command_list = [
    #     "sudo reboot"
    # ]
    # ssh_process = helper.createSshProcess(provider_endpoint, command_list)

    # if ssh_process.returncode:
    #     return make_response(jsonify({"message": "Something went wrong while running rebooting",
    #                     "output": ssh_output,
    #                     "error": ssh_errors}), 400)


    # ------------------------------------------------
    # Create VM monitor container
    # ------------------------------------------------
    vm_monitor_image = os.getenv("DCP_VM_MONITOR_IMAGE")
    destination_user = os.getenv("MASTER_USERNAME")

    try:
        subproc_result = subprocess.run(["docker", "run", "-dit", 
                        "--restart", "always", 
                        "--name", str(vm_id),
                        "--env", "DESTINATION_IP={}".format(str(provider_endpoint)), 
                        "--env", "DESTINATION_USER={}".format(str(destination_user)),
                        str(vm_monitor_image)])

    except subprocess.CalledProcessError as error:
        return make_response(jsonify({"error": error, "message":"Error while creating tunnel container"}),500)


    return make_response(jsonify({"message":"Init setup successful", "output": ssh_output}),200)


# ====================================================================
# Get html of system spec check
# ====================================================================
def getHTMLSystemSpecCheck():
    provider_endpoint = request.get_json().get("providerEndpoint")
    
    command_list = [
        "sudo lshw -html\n"
    ]
    ssh_process = helper.createSshProcess(provider_endpoint, command_list)
    ssh_output, ssh_errors = ssh_process.communicate()
    
    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while running full system check",
                        "error": ssh_errors}), 400)
    
    return make_response(jsonify({"message":"Full system spec check successful", 
                            "output":ssh_output}), 200)

# ====================================================================
# Get parsed system spec check
# ====================================================================
def getSystemSpecCheck():
    provider_endpoint = request.get_json().get("providerEndpoint")

    command_list = [
        "sudo lshw -short -class processor -class memory -class disk\n"

        # TODO: add nvidia commands to fetch gpu info
    ]
    ssh_process = helper.createSshProcess(provider_endpoint, command_list)
    ssh_output, ssh_errors = ssh_process.communicate()
    
    response = {"memory": [], "processor": [], "disk": [], "gpu":[]}

    # Parse stdout to filter out desired description values
    # TODO: only minimal working version. Would be good if hardware can be listed in json
    for line in ssh_output.split("\n")[2:-1]:
        split_line = line.split()
        description = ' '.join(split_line[2:])
        if split_line[1] == "processor":
            response["processor"].append(description)
        elif split_line[1] == "disk":
            response["disk"].append(description)
        elif split_line[1] == "memory" and "System Memory" in description:
            response["memory"].append(description)
    

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while running system check",
                        "error": ssh_errors}), 400)
    


    return make_response(jsonify({"message":"System check successful", "output": response}),200)


