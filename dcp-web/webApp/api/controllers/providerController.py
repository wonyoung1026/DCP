from flask import request, jsonify
from ..models import virtualMachineModel, gpuModel, vmTransactionModel, gpuTransactionModel, containerModel, gpuMetricModel
from . import authController, helper
import os
import requests
import datetime
import json
# ===============================================================
# Preregister provider VM
# - Called when provider has only input IP address
# - Displays fetched specs to the provider for confirmation
# 
#                   OR 
# 
# Update provider VM ip address
# ===============================================================
def getPreregisterVM():
    ip = request.args.get("ip")
    if not ip:
        return {'message': "IP address cannot be blank.", "status": 403}
    
    vm_list = virtualMachineModel.VirtualMachine.getByQuery([("ipAddress","==",ip)])
    
    if vm_list:
        return {'message': "IP address is already being used by {} (Virtual Machine ID #{}).".format(vm_list[0].providerEmail, vm_list[0].id), "status": 403}

    # ---------------------------------------------------------------
    # System check on provider host
    # ---------------------------------------------------------------
    instance_manager_path = "remote/provider/spec"
    instance_manager_data = json.dumps({"providerEndpoint":str(ip)})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    print("RESPONSE")
    print(instance_manager_response.text)

    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}
    
    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}



    # TO BE DELETED:dummy response 
    # res = {
    #     "message" : "System check successful.",
    #     "output": {
    #         "processor": ["processor1"],
    #         "memory": ["memory1", "m2", "m3"],
    #         "disk": ["disk1"]
    #         # ,
    #         # "gpu": [{
    #         #     "processor" : "gpu1-processor",
    #         #     "uuid" : "gpu1-uuid"
    #         # }, {
    #         #     "processor" : "gpu2-processor",
    #         #     "uuid" : "gpu2-uuid"
    #         # }]
    #     }
    # }
    scanned_spec = instance_manager_response_json.get("output")

    provider = authController.getUserWithSessionCookie()

    # ---------------------------------------------------------------
    # Update IP address if vmID param exists (includes if system specs have been changed)
    # ---------------------------------------------------------------
    vm_id = request.args.get("vmID")
    if vm_id:
        existing_vm = virtualMachineModel.VirtualMachine(id=vm_id)
        existing_vm.reload()

        if existing_vm.providerID != provider.id:
            return {"message": "You are not authorized to update IP address", "status": 401}
        
        # TODO: check if container running in the instance via instance manager app
        

        running_container_list = []
        if running_container_list:
            return {"message": "There are still running containers in the machine ({})".format(running_container_list), "status": 403}

        existing_gpu_list = []
        for gpu_id in existing_vm.gpuIDs:
            gpu = gpuModel.GPU(id=gpu_id)
            gpu.reload()
            existing_gpu_list.append(gpu.toJson())
        
        # Check if previous specs match the new spec
        processor_is_same = len(set(existing_vm.get("processor")) & set(scanned_spec.get("processor"))) == len(existing_vm.get("processor"))
        memory_is_same = len(set(existing_vm.get("memory")) & set(scanned_spec.get("memory"))) == len(existing_vm.get("memory"))
        disk_is_same = len(set(existing_vm.get("disk")) & set(scanned_spec.get("disk"))) == len(existing_vm.get("disk"))

        pairs = zip(sorted(existing_gpu_list, key = lambda i: (i['uuid'])), sorted(scanned_spec.get("gpu"), key = lambda i: (i['uuid']))) if scanned_spec.get("gpu") else []

        gpu_is_same = any(x!=y for x,y in pairs) if pairs else True

        if not processor_is_same or not memory_is_same or not disk_is_same or not gpu_is_same:
            return {"message": "Please check your hardwares. If you have changed hardware, please register as a new VM.", "status": 403}

        existing_vm.ipAddress = ip
        existing_vm.save()

        existing_vm["gpu"] = existing_gpu_list
        return {'output': existing_vm.toJson(), 'message': "Virtual machine preregister spec check.", "status":203}


    # ---------------------------------------------------------------
    # Preregister provider VM based on scanned system specs 
    # - Insert VM, GPU into DB first (price = -1, expireTime = 30min)
    # - if user confirmation not received, the instance will expire
    # ---------------------------------------------------------------
    expire_time = helper.getCurrentTime() + datetime.timedelta(minutes=30)
    
    # VM
    vm_id = virtualMachineModel.VirtualMachine(processor=scanned_spec.get("processor"), memory=scanned_spec.get("memory"), disk=scanned_spec.get("disk"), 
                                                 ipAddress= ip, providerID=provider.id, numberOfDisconnections=0,
                                                 providerEmail=provider.email, isHidden=False, status=0,
                                                 name="", price=-1, expireTime=expire_time).save()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()

    # GPU
    gpu_id_list = []
    gpu_list_with_id = scanned_spec.get("gpu") if scanned_spec.get("gpu") else []
    for i in range(len(gpu_list_with_id)):
        gpu_id = gpuModel.GPU(processor=gpu_list_with_id[i].get("processor"), uuid=gpu_list_with_id[i].get("uuid"), virtualMachineID=vm.id,
                                price=-1, expireTime=expire_time).save()
        gpu_id_list.append(gpu_id)
        gpu_list_with_id[i]["id"] = gpu_id

    # Add gpu IDs to VM and save
    vm.gpuIDs = gpu_id_list
    vm.save()

    vm["gpu"] = gpu_list_with_id

    return {'output': vm.toJson(), 'message': "Virtual machine preregister spec check.", "status":200}


# ===============================================================
# Register provider VM
# - Called when provider has confirmed system specs on 2nd page VM sell page
# ===============================================================
def postRegisterVM():
    vm_id = request.get_json().get("preregisteredID")
    vm_price = request.get_json().get("vmPrice")
    gpu = request.get_json().get("gpu")

    provider = authController.getUserWithSessionCookie()

    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    
    if not vm:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if not vm_price:
        return {"message": 'Virtual machine price has to be set', "status": 403}
    
    if provider.id != vm.providerID:
        return {"message": 'Not authorized', "status": 401}


    # ---------------------------------------------------------------
    # Initial set up on provider host 
    # ---------------------------------------------------------------
    instance_manager_path = "remote/provider/init"
    instance_manager_data = json.dumps({"providerEndpoint":str(vm.ipAddress), "vmID":str(vm.id)})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}
    
    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}

    # ---------------------------------------------------------------
    # 1. Update VM attributes with user input (e.g. price)
    # 2. Remove expire time set during preregister
    # 3. Repeat the steps for GPUs
    # ---------------------------------------------------------------
    vm.price = int(vm_price)
    vm.providerEmail = provider.email
    vm.expireTime = None


    # Update GPU price
    for gpu_dict in gpu:
        gpu = gpuModel.GPU(id=gpu_dict.get("id"))
        gpu.reload()
        if not gpu:
            return {"message": 'GPU not found', "status": 404}
        
        if gpu_dict.get("price"):
            gpu.price = int(gpu_dict.get("price"))
        else:
            return {"message": 'GPU price has to be set', "status": 403}

        gpu.expireTime = None
        gpu.save()
    
    # Update VM only if all GPU have been properly updated
    vm.save()
    
    return {'output': vm, 'message': "Virtual machine has been registered.", "status":201}

    
# ===============================================================
# Get provider VMs
# ===============================================================
def getMyVMs():
    provider = authController.getUserWithSessionCookie()
    
    # Only fetch those with prices set
    # NOTE: price set as -1 when preregistered
    vm_list = virtualMachineModel.VirtualMachine.getByQuery([("providerID", "==", provider.id),("price",">=",0)])

    for vm in vm_list:
        # Only show one GPU in table for efficiency
        gpu_list = []
        if vm.gpuIDs:
            gpu = gpuModel.GPU(id=vm.gpuIDs[0])
            gpu.reload()
            if gpu.price >= 0:
                gpu_list.append(gpu.toJson())

        vm['gpu'] = gpu_list
        vm.stringStatus = vm.statusAsString()
        vm.toJson()


    return {'output': vm_list, 'message': "Virtual machines found", "status": 200}

# ===============================================================
# Get provider VM
# ===============================================================
def getMyVM(vm_id):
    provider = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm or vm.price < 0:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to hide the virtual machine", "status": 401}

    
    # ---------------------------------------------------------------
    # 1. Query for number of containers attached
    # 2. Add additional attributes (e.g. earnings) to VM
    # ---------------------------------------------------------------
    container_list = containerModel.Container.getByQuery([("virtualMachineID", "==", vm.id)])
    vm.numberOfContainers = len(container_list)
    vm.dueEarnings = 0
    vm.totalEarnings = 0

    # Add GPU detalis
    gpu_list = []
    for gpu_id in vm.gpuIDs:
        gpu = gpuModel.GPU(id=gpu_id)
        gpu.reload()
                
        # Update gpu status : if vacant 0, otherise 1
        gpu.status = 0 if not gpu.containerID else 1
        gpu.pop("'containerID", None)
        
        if gpu.price >= 0:
            gpu_list.append(gpu.toJson())

        # Add gpu transaction details
        gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery([("gpuID","==",gpu_id)])
        for transaction in gpu_transaction_list:
            if not transaction.paid:
                vm.dueEarnings += transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            
            vm.totalEarnings += transaction.totalPrice

    vm.gpu = gpu_list

    # Add vm transaction details
    vm_transaction_list = vmTransactionModel.VMTransaction.getByQuery([("virtualMachineID","==",vm.id)])
    for transaction in vm_transaction_list:
        if not transaction.paid:
            vm.dueEarnings += transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)

        vm.totalEarnings += transaction.totalPrice
    
    return {'output': vm, 'message': "Virtual machine found", "status": 200}

# ===============================================================
# Hide VM from market
# ===============================================================
def hideMyVM(vm_id):
    provider = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to hide the virtual machine", "status": 401}
    
    vm.isHidden = True
    vm.save()
    return {'output': vm.id, 'message': "Virtual machines hidden", "status": 200}

# ===============================================================
# Make VM visible on market 
# ===============================================================
def showMyVM(vm_id):
    provider = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to show the virtual machine", "status": 401}
    
    vm.isHidden = False
    vm.save()
    return {'output': vm.id, 'message': "Virtual machines shown", "status": 200}

# ===============================================================
# Update provider VM (e.g. price and name)
# ===============================================================
def updateMyVM(vm_id):
    provider = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to update the virtual machine", "status": 401}

    vm.price = int(request.get_json().get("price"))
    vm.name = request.get_json().get("name")
    vm.save()
    return {'output': vm.id, 'message': "Virtual machine updated", "status": 202}

# ===============================================================
# Terminate provider VM
# ===============================================================
def terminateMyVM(vm_id):
    provider = authController.getUserWithSessionCookie()
    vm = virtualMachineModel.VirtualMachine(id=vm_id)
    vm.reload()
    if not vm:
        return {"message": 'Virtual machine not found', "status": 404}
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to terminate the virtual machine", "status": 401}
    
    container_list = containerModel.Container.getByQuery([("virtualMachineID", "==", vm.id)])
    if container_list:
        return {"message": "There shouldn't be any container in order to terminate.", "status": 403}

    # ---------------------------------------------------------------
    # Terminate VM monitor container via instance manager app
    # ---------------------------------------------------------------        
    instance_manager_path = "/vm/container/"+vm.id+"/terminate"
    instance_manager_data = json.dumps({"ipAddress":vm.ipAddress})
    instance_manager_url = "{}:{}/{}".format(os.getenv("INSTANCE_MANAGER_APP_DOMAIN"), os.getenv("INSTANCE_MANAGER_APP_PORT"), instance_manager_path)
    instance_manager_response = requests.get(instance_manager_url, data=instance_manager_data, headers={"content-type":"application/json"})
    print("RESPONSE")
    print(instance_manager_response.text)
    try:
        instance_manager_response_json = json.loads(instance_manager_response.text)
    except:
        return {'message': instance_manager_response.text, 'status': instance_manager_response.status_code}

    if not instance_manager_response:
        return {'message': instance_manager_response_json.get("message"), 'status': instance_manager_response.status_code}


    # ---------------------------------------------------------------
    # 1. Delete connected GPU
    # 2. Delete VM
    # ---------------------------------------------------------------
    
    for gpu_id in vm.gpuIDs:
        gpu = gpuModel.GPU(id=gpu_id)
        gpu.remove()
        
    vm.remove()

    return {'message': "Virtual machines terminated", "status": 203}

# ===============================================================
# Get provider GPU list
# ===============================================================
def getMyGPUs():
    provider = authController.getUserWithSessionCookie()
    vm_list = virtualMachineModel.VirtualMachine.getByQuery([("providerID", "==", provider.id), ("price", ">=", 0)])
    gpu_list = []
    
    # ---------------------------------------------------------------
    # Add additional attributes (e.g. whether the GPU is occupied)
    # ---------------------------------------------------------------
    for vm in vm_list:
        for gpu_id in vm.gpuIDs:
            gpu = gpuModel.GPU(id=gpu_id)
            gpu.reload()
            
            # Append name VM host name in parentheses
            gpu.hostID = vm.id + "(" + vm.name + ")" if vm.name else vm.id
            gpu.isVacant = True if not gpu.containerID else False

            if gpu.price >= 0:
                gpu_list.append(gpu.toJson())

    return {'output': gpu_list, 'message': "GPUs found", "status": 200}


# ===============================================================
# Get provider GPU
# ===============================================================
def getMyGPU(gpu_id):
    provider = authController.getUserWithSessionCookie()

    gpu = gpuModel.GPU(id=gpu_id)
    gpu.reload()
    
    if gpu.price < 0:
        return {'message': "GPU not found", "status": 404}

    vm = virtualMachineModel.VirtualMachine(id=gpu.virtualMachineID)
    vm.reload()
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to get GPU (ID #{})".format(gpu.id), "status": 401}


    # ---------------------------------------------------------------
    # Add additional attributes (e.g. whether the GPU is occupied)
    # ---------------------------------------------------------------
    gpu.virtualMachineID = vm.id + "(" + vm.name + ")" if vm.name else vm.id
    gpu.isVacant = True if not gpu.containerID else False

    gpu.dueEarnings = 0
    gpu.totalEarnings = 0
    # Add GPU transaction details
    gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery([("gpuID","==",gpu.id)])
    for transaction in gpu_transaction_list:
        if not transaction.paid:
            gpu.dueEarnings += transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
        
        gpu.totalEarnings += transaction.totalPrice

    gpu.toJson()

    return {'output': gpu, 'message': "GPU found", "status": 200}

# ===============================================================
# Update GPU (e.g. GPU price, name)
# ===============================================================
def updateMyGPU(gpu_id):
    provider = authController.getUserWithSessionCookie()

    gpu = gpuModel.GPU(id=gpu_id)
    gpu.reload()
    
    if not gpu:
        return {"message": 'GPU not found', "status": 404}

    vm = virtualMachineModel.VirtualMachine(id=gpu.virtualMachineID)
    vm.reload()
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to update GPU (ID #{})".format(gpu.id), "status": 401}
    


    gpu.price = int(request.get_json().get("price"))
    gpu.name = request.get_json().get("name")
    gpu.save()

    return {'output': gpu.id, 'message': "Virtual machines updated", "status": 202}

# ===============================================================
# Get GPU monitoring data
# ===============================================================
def getGPUMonitoring(gpu_id):
    provider = authController.getUserWithSessionCookie()

    gpu = gpuModel.GPU(id=gpu_id)
    gpu.reload()

    if not gpu:
        return {'message': "Virtual machine not found", "status": 404}
    
    vm = virtualMachineModel.VirtualMachine(id=gpu.virtualMachineID)
    vm.reload()
    
    if vm.providerID != provider.id:
        return {"message": "You are not authorized to update GPU (ID #{})".format(gpu.id), "status": 401}

    # ---------------------------------------------------------------
    # Past 2 hours GPU metrics
    # ---------------------------------------------------------------
    n=-2
    n_hours_ago_dt = helper.getCurrentTime() + datetime.timedelta(hours=n)

    gpu_metrics = gpuMetricModel.GPUMetric.getByQuery([("gpuUUID", "==", gpu.uuid), ('createdOn', ">=", n_hours_ago_dt)])

    stats = {
        'gpuUtils' : [],
        'memoryUtils' : [],
        'time' : []
    }
    
    for gpu_metric in gpu_metrics:
        stats['gpuUtils'].append(gpu_metric.gpuUtil)
        stats['memoryUtils'].append(gpu_metric.memoryUtil)
        stats['time'].append(gpu_metric.createdOn.strftime("%H:%M"))
    
    return {'output' : stats, 'message': "GPU resource activity history found", "status":200}


# ===============================================================
# Get provider dashboard data
# ===============================================================
def getMyDashboard():
    provider = authController.getUserWithSessionCookie()
    
    current_year = helper.getCurrentTime().year
    current_month = helper.getCurrentTime().month


    # ---------------------------------------------------------------
    # Earnings & Earnings line chart
    # ---------------------------------------------------------------
    # past n months earnings for dashboard line chart
    past_months_earnings = helper.getPastNDict("m", 6)

    annual_earnings = 0
    monthly_earnings = 0

    # Add up VM transaction earnings
    vm_transaction_list = vmTransactionModel.VMTransaction.getByQuery(triplets=[("providerID","==",provider.id)])
    for transaction in vm_transaction_list:
        if transaction.endTime:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime)*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            if transaction.endTime.year == current_year:
                annual_earnings += price
            if transaction.endTime.month == current_month:
                monthly_earnings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(transaction.endTime.year, transaction.endTime.month)
            if key in past_months_earnings:
                past_months_earnings[key] += price
        else:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            annual_earnings += price
            monthly_earnings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(helper.getCurrentTime().year, helper.getCurrentTime().month)
            if key in past_months_earnings:
                past_months_earnings[key] += price


    # Add up GPU transaction earnings
    gpu_transaction_list = gpuTransactionModel.GPUTransaction.getByQuery(triplets=[("providerID","==",provider.id)])
    for transaction in vm_transaction_list:
        if transaction.endTime:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, transaction.endTime)*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            if transaction.endTime.year == current_year:
                annual_earnings += price
            if transaction.endTime.month == current_month:
                monthly_earnings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(transaction.endTime.year, transaction.endTime.month)
            if key in past_months_earnings:
                past_months_earnings[key] += price
        else:
            price = transaction.totalPrice if transaction.totalPrice else helper.getTimeDifferenceInSeconds(transaction.startTime, helper.getCurrentTime())*helper.hourlyPriceToSecondlyPrice(transaction.pricePerHour)
            annual_earnings += price
            monthly_earnings += price

            # Dashboard line chart data
            key = helper.yearMonthKeyFormat(helper.getCurrentTime().year, helper.getCurrentTime().month)
            if key in past_months_earnings:
                past_months_earnings[key] += price
    
    # ---------------------------------------------------------------
    # VM status
    # ---------------------------------------------------------------
    vm_list = virtualMachineModel.VirtualMachine.getByQuery([("providerID","==",provider.id)])
    running_number = 0
    pending_number = 0
    unstable_number = 0
    disconnected_number = 0

    for vm in vm_list:
        if vm.status == 0:
            running_number += 1
        elif vm.status == 1:
            pending_number += 1
        elif vm.status == 2:
            unstable_number += 1
        elif vm.status == 3:
            disconnected_number += 1
    
    dashboard_data = {
        'monthly_earnings': int(monthly_earnings),
        'annual_earnings': int(annual_earnings),
        
        'notification':0,
        
        # Past 6 months
        "chart_data" : past_months_earnings,

        # VM virtualMachineModel.py 참고 
        'instance_overview':{
            'running':running_number,
            'pending': pending_number,
            'unstable':unstable_number,
            'disconnected':disconnected_number
        }
    }

    return {'output' : dashboard_data, 'message': "Dashboard data found", "status":200}


# ===============================================================
# Get provider billing overview
# ===============================================================
def getMyBillingOverview():
    pass