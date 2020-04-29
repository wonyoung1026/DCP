from ..models import virtualMachineModel, keyPairModel, gpuModel,containerModel, vmTransactionModel, gpuTransactionModel,baseImageModel,userImageModel
from flask import request, make_response, jsonify
from . import authController, helper 
import datetime
import os
import requests
import json
# ===============================================================
# Buyer purchase instance
# ===============================================================
def postPurchaseVM():
    buyer = authController.getUserWithSessionCookie()
    vm_id = request.get_json().get("virtualMachineID")
    gpu_ids = request.get_json().get("gpuIDs")
    base_image_id = request.get_json().get("baseImageID")

    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm:
        return {'message': 'Virtual machine not found', 'status': 404}

    if vm.providerID == buyer.id:
        return {'message': "You can't purchase your own instance.", 'status': 401}

    # Insert container into DB (status as "pending")
    container_id = containerModel.Container(buyerID=buyer.id, imageID=base_image_id, virtualMachineID=vm_id, status=1, costRate=0).save()
    if not container_id:
        return {'message': 'Failed to insert container in database', 'status': 500}
    
    # ---------------------------------------------------------------
    # Send request to instnace manager app to create a container in provider machine
    # ---------------------------------------------------------------        
    
    instance_manager_path = "container/"+container_id+"/create"
    instance_manager_data = json.dumps({"baseImageID":base_image_id, "ipAddress":str(vm.ipAddress), "gpuIDs": gpu_ids})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    print("RESPONSE")
    print(instance_manager_response.text)
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}


    if not instance_manager_response:
        containerModel.Container(id=container_id).remove()
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}

    # container cost rate
    container_cost_rate = vm.price

    # ---------------------------------------------------------------
    # Update database
    # ---------------------------------------------------------------        
    #  create VM transaction 
    vmTransactionModel.VMTransaction(virtualMachineID=vm.id, buyerID=buyer.id, providerID=vm.providerID,
                                        totalPrice=0, paid=False, startTime=helper.getCurrentTime(),
                                        pricePerHour=vm.price, containerID=container_id).save()

    # Add container ID to GPU collection
    new_gpu_id_list = []
    for gpu_id in gpu_ids:
        if not gpu_id in vm.gpuIDs:
            return {'message': "GPU does not belong to the virtual machine.", 'status': 401}
        
        gpu = gpuModel.GPU(id=gpu_id)
        gpu.reload()
        
        # add gpu price to container price
        container_cost_rate += gpu.price 

        gpu.containerID = container_id
        gpu.save()

        # Create GPU Transaction
        gpuTransactionModel.GPUTransaction(gpuID=gpu.id, buyerID=buyer.id, providerID=vm.providerID, 
                                    totalPrice=0, paid=False, startTime=helper.getCurrentTime(),
                                    pricePerHour=gpu.price, containerID=container_id).save()
    
    # Update price and status to running 
    container_id = containerModel.Container(id=container_id, status=0, costRate=container_cost_rate).save()

    return {'message': "Purchase success.", 'status': 201}



# ===============================================================
# Buyer get my containers
# ===============================================================
def getMyContainers():
    buyer = authController.getUserWithSessionCookie()
    container_list = containerModel.Container.getByQuery([("buyerID", "==", buyer.id)])

    for container in container_list:
        vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
        vm.reload()
        # only 1 proessor for list elements
        container.processor = vm.processor[0] if vm.processor else ""
        
        # only fetch 1 GPU for list elements
        gpu =gpuModel.GPU(id=vm.gpuIDs[0] if vm.gpuIDs else "")
        gpu.reload()

        container.providerEmail = vm.providerEmail
        container.gpu = gpu.processor
        container.stringStatus = container.statusAsString()
        container.toJson()
    
    return {'output': container_list, 'message': "Successfully found containers", 'status': 200}


# ===============================================================
# Buyer terminates own container and saves the image
# ===============================================================
def postTerminateMyContainerWithSave(container_id):
    buyer = authController.getUserWithSessionCookie()

    container = containerModel.Container(id=container_id)
    container.reload()
    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to stop the container", "status": 401}
    if container.status != 4:
        return {"message": "You can only terminate a stopped container. Current status is {}".format(container.statusAsString()), "status": 403}

    user_image_name = request.get_json().get("userImageName")
    user_image_description = request.get_json().get("userImageDescription")
    user_image_id = userImageModel.UserImage(name= user_image_name, description=user_image_description, buyerID=buyer.id).save()

    vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
    vm.reload()
    if not vm:
        return {'message': 'Virtual machine not found', 'status': 404}

    # ---------------------------------------------------------------
    # Terminate container and push image to DCP registry with given user_image_id via instance manager app 
    # ---------------------------------------------------------------        
    instance_manager_path = "container/"+container_id+"/terminate/s"
    instance_manager_data = json.dumps({"ipAddress":vm.ipAddress, "userImageID": user_image_id})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})

    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}

    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}


    # ---------------------------------------------------------------
    # Update database
    # ---------------------------------------------------------------    
    containerModel.Container(id=container.id).remove()


    return {"output":user_image_id,"message": 'Container deleted and image saved successfully', "status": 201}


# ===============================================================
# Buyer terminates own container without saving the image
# ===============================================================
def postTerminateMyContainerWithoutSave(container_id):
    buyer = authController.getUserWithSessionCookie()

    container = containerModel.Container(id=container_id)
    container.reload()
    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to stop the container", "status": 401}
    if container.status != 4:
        return {"message": "You can only terminate a stopped container. Current status is {}".format(container.statusAsString()), "status": 403}


    vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
    vm.reload()
    if not vm:
        return {'message': 'Virtual machine not found', 'status': 404}

    # ---------------------------------------------------------------
    # Terminate container via instance manager app
    # ---------------------------------------------------------------        
    instance_manager_path = "container/"+container_id+"/terminate"
    instance_manager_data = json.dumps({"ipAddress":vm.ipAddress})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}

    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}

    


    # ---------------------------------------------------------------
    # Update database
    # ---------------------------------------------------------------    
    containerModel.Container(id=container.id).remove()

    return {"message": 'Container delete without save success', "status": 201}

# ===============================================================
# Buyer starts own container
# ===============================================================
def postStartMyContainer(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()
    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to stop the container", "status": 401}
    if container.status != 4:
        return {"message": "You can only start a stopped container. Current status is {}".format(container.statusAsString()), "status": 403}

    gpu_ids = request.get_json().get("gpuIDs")

    vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
    vm.reload()
    if not vm:
        return {'message': 'Virtual machine not found', 'status': 404}

    if vm.providerID == buyer.id:
        return {'message': "You can't purchase your own instance.", 'status': 401}
    
    
    # ---------------------------------------------------------------
    # Start running container via instance manager app
    # ---------------------------------------------------------------        
    instance_manager_path = "container/"+container_id+"/start"
    instance_manager_data = json.dumps({"ipAddress":vm.ipAddress, "gpuIDs": gpu_ids})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}

    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}


    # ---------------------------------------------------------------
    # Update database
    # ---------------------------------------------------------------    

    # container cost rate
    container_cost_rate = vm.price

    #  create VM transaction 
    vmTransactionModel.VMTransaction(virtualMachineID=vm.id, buyerID=buyer.id, providerID=vm.providerID,
                                        totalPrice=0, paid=False, startTime=helper.getCurrentTime(),
                                        pricePerHour=vm.price, containerID=container.id).save()

    
    for gpu_id in gpu_ids:
        gpu = gpuModel.GPU(id=gpu_id)
        gpu.reload()
        if not gpu:
            continue
        gpu.containerID =container.id
        gpu.save()

        # add gpu price to container price
        container_cost_rate += gpu.price

        # Create GPU Transaction
        gpuTransactionModel.GPUTransaction(gpuID=gpu.id, buyerID=buyer.id, providerID=vm.providerID, 
                                    totalPrice=0, paid=False, startTime=helper.getCurrentTime(),
                                    pricePerHour=gpu.price, containerID=container_id).save()

    # Update price and status to running 
    container_id = containerModel.Container(id=container_id, status=0, costRate=container_cost_rate).save()

    return {'message': "Container start success.", 'status': 201}

# ===============================================================
# Buyer stops own container
# ===============================================================
def postStopMyContainer(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()
    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to stop the container", "status": 401}
    if container.status != 0:
        return {"message": "You can only stop a running container. Current status is {}".format(container.statusAsString()), "status": 403}

    vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
    vm.reload()
    if not vm:
        return {'message': 'Virtual machine not found', 'status': 404}

    # ---------------------------------------------------------------
    # Stop running container via instance manager app
    # ---------------------------------------------------------------    
    instance_manager_path = "container/"+container_id+"/stop"
    instance_manager_data = json.dumps({"ipAddress":vm.ipAddress})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json", "data-type":"json"})
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}

    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}

    # ---------------------------------------------------------------
    # Update database
    # ---------------------------------------------------------------    

    # IF SUCCESSFULLY STOPPED, detach container from GPU
    gpu_list = gpuModel.GPU.getByQuery([("containerID", "==", container.id)])
    for gpu in gpu_list:
        gpu.containerID = None
        gpu.save()

        # Stop GPU transction fees
        gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery([("gpuID","==",gpu.id),("containerID","==",container.id)])
        for transaction in gpu_transaction_list:
            if not transaction.endTime and transaction.buyerID == buyer.id:
                transaction.endTime = helper.getCurrentTime()
                transaction.totalPrice = helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime) * helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
                transaction.save()
    
    # Stop VM trnasaction fees 
    vm_transaction_list = vmTransactionModel.VMTransaction.getByQuery([("virtualMachineID","==",container.virtualMachineID), ("containerID", "==",container.id)])
    for transaction in vm_transaction_list:
        if not transaction.endTime and transaction.buyerID == buyer.id:
                transaction.endTime = helper.getCurrentTime()
                transaction.totalPrice = helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime) * helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
                transaction.save()

    # Update price and status to running 
    container_id = containerModel.Container(id=container_id, status=4, costRate=0).save()

    return {'output': container.id, 'message': "Container stop success", "status": 201}

# ===============================================================
# Buyer updates own container (e.g. name)
# ===============================================================
def updateMyContainer(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()
    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to update the container", "status": 401}  
    
    container.name = request.get_json().get("name")
    container.save()

    return {'output': container.id, 'message': "Container updated", "status": 202}



# ===============================================================
# Buyer gets own container related data
# ===============================================================
def getMyContainer(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()
    if buyer.id != container.buyerID:
        return make_response(jsonify({'message': "Not authorized."}), 401)

    # Check DCP base image first and then check personal image 
    base_image = baseImageModel.BaseImage(id=container.imageID)
    base_image.reload()
    if not base_image:
        base_image = userImageModel.UserImage(id=container.imageID)
    container.baseImage = base_image

    vm = virtualMachineModel.VirtualMachine(id=container.virtualMachineID)
    vm.reload()
    # Remove sensitive data fields
    vm.pop('ipAddress', None)
    vm.pop('isHidden', None)

 
    # Calclate total due spendings from transactions
    due_spendings = 0

    vm_transaction_list = vmTransactionModel.VMTransaction.getByQuery([("containerID", "==", container.id), ("virtualMachineID", "==", vm.id)])
    
    for transaction in vm_transaction_list:
        if not transaction.paid:
            due_spendings += transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)

    gpu_list = gpuModel.GPU.getByQuery([("containerID", "==", container.id)])
    for gpu in gpu_list:
        gpu.pop('uuid', None)
        gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery([("containerID", "==", container.id), ("gpuID", "==", gpu.id)])
        for transaction in gpu_transaction_list:
            due_spendings += transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
        gpu.toJson()

    container.dueSpendings = due_spendings

    output = {
        'container' : container.toJson(),
        'vm': vm.toJson(),
        'gpuList': gpu_list
    }
    
    return {'output': output, 'message': 'Container #{} found'.format(container.id), 'status': 200}


# ===============================================================
# Buyer recharges credit
# ===============================================================
def rechargeUserCredit(amount):
    buyer = authController.getUserWithSessionCookie()
    buyer.credit = buyer.credit+int(amount)
    buyer.save()
    return {'message': "Rechage Success", 'status': 202}



# ===============================================================
# Buyer gets GPU info of selected VM
# ===============================================================
def getVMGPUs(vm_id):
    buyer = authController.getUserWithSessionCookie()

    gpu_list = gpuModel.GPU.getByQuery([("virtualMachineID","==", vm_id)])

    for gpu in gpu_list:
        gpu.status = 0 if not gpu.containerID else 1
        gpu.pop("containerID", None)
        gpu.pop("uuid", None)
        gpu.toJson()
    
    return {'output':gpu_list,'message': 'GPUs found', 'status': 200}
    


# ===============================================================
# Get buyer dashboard data
# ===============================================================
def getMyDashboard():
    buyer = authController.getUserWithSessionCookie()
    
    current_year = helper.getCurrentTime().year
    current_month = helper.getCurrentTime().month


    # ---------------------------------------------------------------
    # Earnings & Earnings line chart
    # ---------------------------------------------------------------
    # past n months earnings for dashboard line chart
    past_months_spendings = helper.getPastNDict("m", 6)

    annual_spendings = 0
    monthly_spendings = 0

    # Add up VM transaction earnings
    vm_transaction_list = vmTransactionModel.VMTransaction.getByQuery(triplets=[("buyerID","==",buyer.id)])
    for transaction in vm_transaction_list:
        if transaction.endTime:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime)*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            if transaction.endTime.year == current_year:
                annual_spendings += price
            if transaction.endTime.month == current_month:
                monthly_spendings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(transaction.endTime.year, transaction.endTime.month)
            if key in past_months_spendings:
                past_months_spendings[key] += price
        
        else:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            annual_spendings += price
            monthly_spendings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(helper.getCurrentTime().year, helper.getCurrentTime().month)

            if key in past_months_spendings:
                past_months_spendings[key] += price


    # Add up GPU transaction earnings
    gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery(triplets=[("buyerID","==",buyer.id)])
    for transaction in vm_transaction_list:
        if transaction.endTime:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime)*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            if transaction.endTime.year == current_year:
                annual_spendings += price
            if transaction.endTime.month == current_month:
                monthly_spendings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(transaction.endTime.year, transaction.endTime.month)
            if key in past_months_spendings:
                past_months_spendings[key] += price
        
        else:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            annual_spendings += price
            monthly_spendings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(helper.getCurrentTime().year, helper.getCurrentTime().month)
            if key in past_months_spendings:
                past_months_spendings[key] += price
    
    # ---------------------------------------------------------------
    # container status
    # ---------------------------------------------------------------
    container_list = containerModel.Container.getByQuery([("buyerID","==",buyer.id)])
    running_number = 0
    pending_number = 0
    unstable_number = 0
    disconnected_number = 0

    for container in container_list:
        if container.status == 0:
            running_number += 1
        elif container.status == 1:
            pending_number += 1
        elif container.status == 2:
            unstable_number += 1
        elif container.status == 3:
            disconnected_number += 1
    
    dashboard_data = {
        'monthly_spendings': int(monthly_spendings),
        'annual_spendings': int(annual_spendings),
        'credit': buyer.credit,

        'notification':0,
        
        # Past 6 months
        "chart_data" : past_months_spendings,

        # VM virtualMachineModel.py 참고 
        'instance_overview':{
            'running':running_number,
            'pending': pending_number,
            'unstable':unstable_number,
            'disconnected':disconnected_number
        }
    }

    return {'output' : dashboard_data, 'message': "Dashboard data found", "status":200}
# TODO: change to redirect when CORS issue fixed
# Returns URL for now
def getShellURL(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()

    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to access the container", "status": 401}
    if container.status != 0:
        return {"message": "Shell can only be launched for a running container. Current status is {}".format(container.statusAsString()), "status": 403}

    url = "{}:{}/e/{}".format(os.getenv("TERMINAL_APP_DOMAIN"), os.getenv("TERMINAL_APP_PORT"), container_id)

    return {"output": url, "message": "URL created successfully", "status": 200}


# TODO: change to redirect when CORS issue fixed
# Returns URL for now
def getContainerMonitorURL(container_id):
    buyer = authController.getUserWithSessionCookie()
    container = containerModel.Container(id=container_id)
    container.reload()

    if not container:
        return {"message": 'Container not found', "status": 404}
    if container.buyerID != buyer.id:
        return {"message": "You are not authorized to monitor this instance", "status": 401}
    if container.status != 0:
        return {"message": "You can only monitor a running container. Current status is {}".format(container.statusAsString()), "status": 403}

    url = "{}:{}/m/{}".format(os.getenv("TERMINAL_APP_DOMAIN"), os.getenv("TERMINAL_APP_PORT"), container_id)

    return {"output": url, "message": "URL created successfully", "status": 200}
