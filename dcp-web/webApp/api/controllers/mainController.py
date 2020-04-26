from ..models import virtualMachineModel, keyPairModel, gpuModel, vmMetricModel, favoriteModel, baseImageModel
from flask import request, make_response, jsonify, abort
from . import authController, helper

import subprocess
import datetime
import os
import requests
import json

def getVMs():
    # Only fetch VMs with prices set
    vm_list = virtualMachineModel.VirtualMachine.getByQuery([("price",">",0)])


    new_vm_list = []
    for vm in vm_list:
        if not vm.isHidden:
            # Only show one GPU in table
            gpu_list = []
            if vm.gpuIDs:
                gpu = gpuModel.GPU(id=vm.gpuIDs[0])
                gpu.reload()
                
                if gpu.price >=0:
                    gpu_list.append(gpu.toJson())

            vm['gpu'] = gpu_list
            new_vm_list.append(vm)

        vm.toJson()


    return {'output': new_vm_list, 'message': "Virtual machines found", "status": 200}


def getVMByID(vm_id):
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm or vm.isHidden or not vm.price:
        return {'message': "Virtual machine not found", "status": 404}
    
    user = authController.getUserWithSessionCookie()
    
    # Check if already in favorite list
    favorites = favoriteModel.Favorite().getByQuery([("userID", "==", user.id), ("virtualMachineID", "==", vm_id)])
    vm["isFavorite"] = True if favorites else False

    gpu_list = []
    for gpu_id in vm.gpuIDs:
        gpu = gpuModel.GPU(id=gpu_id)
        gpu.reload()
        
        # Update gpu status : if vacant 0, otherise 1
        gpu.status = 0 if not gpu.containerID else 1
        gpu.pop("'containerID", None)

        if gpu.price >= 0:
            gpu_list.append(gpu.toJson())
    vm['gpu'] = gpu_list
    vm.toJson()


    return {'output':vm, 'message': "Virtual machine found", "status":200}

def getVMFullByID(vm_id):
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    
    if not vm:
        return {'message': "Virtual machine not found", "status": 404}

    # ---------------------------------------------------------------
    # Full system check on provider host
    # ---------------------------------------------------------------
    instance_manager_path = "remote/provider/spec/html"
    instance_manager_data = json.dumps({"providerEndpoint":str(vm.ipAddress)})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}
    
    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}

    spec_html = instance_manager_response_json.get("output")

    return {'output':spec_html, 'message': instance_manager_response_json.get("message"), "status":instance_manager_response_json.get("status")}
# ======================================================
# DEPRECATED
# ======================================================
def getVMMonitoring(vm_id):
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    
    if not vm:
        return {'message': "Virtual machine not found", "status": 404}
    n=-2
    n_hours_ago_dt = helper.getCurrentTime() + datetime.timedelta(hours=n)

    vm_metrics = vmMetricModel.VMMetric.getByQuery([("virtualMachineID", "==", vm_id), ('createdOn', ">=", n_hours_ago_dt)])

    stats = {
        'cpuUtils' : [],
        'memoryUtils' : [],
        'networks' : [],
        'numOfContainers':[],
        'time' : []
    }

    for vm_metric in vm_metrics:
        stats['cpuUtils'].append(vm_metric.cpuUtil)
        stats['memoryUtils'].append(vm_metric.memoryUtil)
        stats['networks'].append(vm_metric.network)
        stats['numOfContainers'].append(vm_metric.numOfContainers)
        stats['time'].append(vm_metric.createdOn.strftime("%H:%M"))


    return {'output' : stats, 'message': "Virtual machine resource activity history found", "status":200}


    

def getFavoriteVMs():
    user = authController.getUserWithSessionCookie()
    favorites = favoriteModel.Favorite().getByQuery([("userID", "==", user.id)])
    
    favorite_vms = []
    for favorite in favorites:
        vm=virtualMachineModel.VirtualMachine(id=favorite.virtualMachineID)
        vm.reload()
        favorite_vms.append(vm)
    # Add GPU objects to vm list 
    for vm in favorite_vms:
        # Only show one GPU per row in table
        gpu_list = []
        if vm.gpuIDs:
            gpu = gpuModel.GPU(id=vm.gpuIDs[0])
            gpu.reload()
            gpu_list.append(gpu.toJson())
        vm['gpu'] = gpu_list
        vm.toJson()

    return {'output': favorite_vms, 'message': "Successfully found favorite virtual machines.", "status":200}


def postAddFavoriteVM(vm_id):
    user = authController.getUserWithSessionCookie()
    favorite_id = favoriteModel.Favorite(virtualMachineID=vm_id, userID=user.id).save()
    
    if not favorite_id:
        return {'message': "Failed to add virtual machine to favorites.", "status": 404}

    return {'output': favorite_id, 'message': "Successfully saved the virtual machine as favorite.", "status":201}


def deleteFavoriteVM(vm_id):
    user = authController.getUserWithSessionCookie()
    favorites = favoriteModel.Favorite().getByQuery([("userID", "==", user.id), ("virtualMachineID", "==", vm_id)])

    if not favorites or len(favorites) > 1:
        return {"message": "Favorite not found", "status":404}

    favorites[0].remove()

    return {'message': "Successfully deleted favorite.", "status":203}

# ================================================
# Get list of base images 
# ================================================
def getBaseImages():
    base_images = baseImageModel.BaseImage().getByQuery()

    if not base_images:
        return {"message": "Base images not found", "status":404}
    
    return {'output': base_images, 'message': "Successfully found favorite virtual machines.", "status":200}



# TODO: change to redirect when CORS issue fixed
# Returns URL for now
def getVMMonitorURL(vm_id):
    buyer = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    print("VM IS")
    print(vm)
    if not vm:
        return {"message": 'VM not found', "status": 404}

    if vm.status != 0:
        return {"message": "You can only monitor a running container. Current status is {}".format(vm.statusAsString()), "status": 403}

    url = "{}:{}/m/{}".format(os.getenv("TERMINAL_APP_DOMAIN"), os.getenv("TERMINAL_APP_PORT"), vm_id)
    print(url)
    return {"output": url, "message": "URL created successfully", "status": 200}

# ================================================
# DEPRECATED
# ================================================
def createKeyPair():
    buyer = authController.getUserWithSessionCookie()
    name = request.json.get("name")
    temp_dir = './temp'
    filename = buyer.id+"."+name

    src_filepath = temp_dir + "/" + filename
    dest_filepath = "key/{}/{}".format(buyer.id, filename)

    # set ttl as 180s
    ttl = "180"

    # Create key pair in temp folder
    keygen_process = subprocess.run(['ssh-keygen', '-f', src_filepath, '-N', ""], capture_output=True)
    output = str(keygen_process.stdout)
    fingerprint = output.split("The key fingerprint is:\\n")[1].split()[0]
    
    
    # write public key to storage
    helper.storageUploadBlob(os.getenv("FIREBASE_STORAGE_BUCKET"), src_filepath, dest_filepath)

    # write to database
    kp=keyPairModel.KeyPair(name=name, buyerID=buyer.id, fingerprint=fingerprint, keyFilePath=dest_filepath)
    kp.save()

    # schedule a job to delete public key after ttl
    timedDeleteProcess = subprocess.Popen(["python3", temp_dir+"/timedDelete.py", filename, '-s', ttl])

    # send file to user before private key gets deleted 
    # return send_from_directory(temp_dir, filename, as_attachment=True)
    return make_response(jsonify({'message':'success!'}))
    
    
