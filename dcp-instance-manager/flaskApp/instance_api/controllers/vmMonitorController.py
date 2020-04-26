from flask import jsonify, make_response
from . import helper
import os
import json
import subprocess
from flaskApp.instance_api.instance_models import vmMetricModel

#helper
def convert_to_list(li):
    li = str(li).split("\\n")
    li = li[1:len(li) - 1]
    return li

#to return container info
#id, cpu, pid, memory list of values
# id = String, cpu,memory = float, pid = int
def containerMonitor():
    id = subprocess.check_output("docker stats --no-stream | awk '{ print $1 }'", shell=True)
    cpu = subprocess.check_output("docker stats --no-stream | awk '{ print $3 }'", shell=True)
    pid = subprocess.check_output("docker stats --no-stream | awk '{ print $14 }'", shell=True)
    memory = subprocess.check_output("docker stats --no-stream | awk '{ print $7 }'", shell=True)
    id, cpu, pid,memory = convert_to_list(id), convert_to_list(cpu), convert_to_list(pid),convert_to_list(memory)
    cpu = [float(c.replace('%', '')) for c in cpu]
    pid = [int(p) for p in pid]
    memory = [mem.replace('%', '') for mem in memory]
    memory = [str(float(mem) * len(id)) for mem in memory]
    ret = {'cpu': cpu, 'memory': memory, 'pid': pid, 'id': id}
    return ret

#to return cpu info
#cpu =float, memory = float, network = String(in Bytes), numOfContainers = int
def cpuMonitor(provider_endpoint):

    #cpu = subprocess.check_output("top -b -n1 | grep -Po '[0-9.]+ id' | awk '{print 100-$1}'", shell=True)
    command_list = [
        "top -b -n1 | grep -Po '[0-9.]+ id' | awk '{print 100-$1}'\n",
        "free | grep Mem | awk '{print $3/$2 * 100.0}'",
        "sudo iptables -L INPUT -n -v\n",
        "docker ps -q $1 | wc -l"
    ]
    ssh_cpu_process = helper.createSshProcess(provider_endpoint, command_list[0])
    ssh_cpu_output, ssh_cpu_errors = ssh_cpu_process.communicate()

    if ssh_cpu_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while printing CPU Util",
                        "error": ssh_cpu_errors}), 400)
    
    cpu = float(str(ssh_cpu_output).split("\\n")[0].replace('b\'', ''))

    ssh_memory_process = helper.createSshProcess(provider_endpoint, command_list[1])
    ssh_memory_output, ssh_memory_errors = ssh_memory_process.communicate()
    
    if ssh_memory_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while printing Memory Util",
                        "error": ssh_memory_errors}), 400)

    memory = float(str(ssh_memory_output).split("\\n")[0].replace('b\'', ''))

    ssh_network_process = helper.createSshProcess(provider_endpoint, command_list[2])
    ssh_network_output, ssh_network_errors = ssh_network_process.communicate()

    if ssh_network_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while printing Network Util",
                        "error": ssh_network_errors}), 400)

    network = str(ssh_network_output).split("packets,")[1].split("bytes")[0].strip()
    
    ssh_numCont_process = helper.createSshProcess(provider_endpoint, command_list[3])
    ssh_numCont_output, ssh_numCont_errors = ssh_numCont_process.communicate()

    if ssh_numCont_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while printing numCont Util",
                        "error": ssh_numCont_errors}), 400)
    container = int(ssh_numCont_output.split("\\n")[0].replace('b\'', '').strip())
    
    vmID = ""

    vm_info = vmMetricModel.VmMetric(cpuUtil=cpu, memoryUtil=memory, network=network, numOfContainers=container, id=vmID).save()
    #ret = {'cpu':cpu, 'memory':memory, 'numOfContainers': container, 'network':network, 'id':id}
    
    return make_response(jsonify({"message":"VM info update", "output": vm_info}),200)

#to return gpu info
#gpu, memory,uuid are lists of values
#gpu, memory = float
#uuid = String
def gpuMonitor():
    id = subprocess.check_output("nvidia-smi -L", shell=True)
    gpu = subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv", shell=True)
    mem = subprocess.check_output("nvidia-smi --query-gpu=utilization.memory --format=csv", shell=True)
    id = str(id).split("\\n")[0:-1]
    gpu = convert_to_list(gpu)
    gpu = [float(gp.replace(' %','')) for gp in gpu]
    mem = convert_to_list(mem)
    mem = [float(me.replace(' %','')) for me in mem]
    id = [m.split("UUID:")[1].strip().replace(')', '') for m in id]
    ret = {'gpu':gpu , 'memory':mem, 'uuid':id, }
    return ret
