from flask import jsonify, make_response
from . import helper
from threading import Timer
from random import choice
import os


# Creating centos container from scratch
def createBaseContainer(provider_endpoint):
    
    # Running centos docker container in background
    # TODO: Be able to manually assign container's name depending on Client's own choice

    command_list = [
        #"docker run -d --name centos_ssh --privileged -p 5000:22 centos /usr/sbin/init\n"
        "docker run -d --name fyp_base_container --cap-add=SYS_ADMIN -e \"container=docker\" -v /sys/fs/cgroup:/sys/fs/cgroup -p 5000:22 centos:7 /usr/sbin/init\n",
        "docker exec fyp_base_container yum -y install openssh-server openssh-clients initscripts passwd\n",
        "docker exec fyp_base_container service sshd start\n",
        "docker commit fyp_base_container fyp_base_image\n",
        "docker stop fyp_base_container\n"
        "docker rm fyp_base_container\n"
    ]
    
    ssh_process = helper.createSshProcess(provider_endpoint, command_list)
    ssh_output, ssh_errors = ssh_process.communicate()

    if ssh_process.returncode:
        return make_response(jsonify({"message": "Something went wrong while creating base container",
                            "error": ssh_errors}), 400)
    
    return make_response(jsonify({"message":"Container run succesful",
                            "output":ssh_output}), 200)


# Running base image container
# TODO: To make unique naming-convention, add index parameter (unique 한 delimeter) 
def runContainer(buyer_endpoint, provider_endpoint, buyer_id, password, public_key, port_num):

    port_num = checkPort(provider_endpoint, port_num)

    command_list1 = [
        "docker run -d --name {a} --cap-add=SYS_ADMIN -e \"container=docker\" -v /sys/fs/cgroup:/sys/fs/cgroup -p {b}:22 fyp_base_image".format(a=buyer_id, b=str(port_num))
    ]
    
    ssh_process1 = helper.createSshProcess(provider_endpoint, command_list1)
    ssh_errors1 = ssh_process1.communicate()[1]

    if ssh_process1.returncode:
        return make_response(jsonify({"message": "Something went wrong while running docker container",
                            "error": ssh_errors1}), 400)
                            
    command_list2 = [
        "docker exec -i {} passwd root\n".format(buyer_id), "{}\n".format(password), "{}\n".format(password)
    ]

    ssh_process2 = helper.createSshProcess(provider_endpoint, command_list2)
    ssh_errors2 = ssh_process2.communicate()[1]

    if ssh_process2.returncode:
        return make_response(jsonify({"message": "Something went wrong while running docker container",
                            "error": ssh_errors2}), 400)

    remote_path = "/home/centos/.ssh"

    scp_process3 = helper.transmitPrivateKeyScpProcess(buyer_endpoint, remote_path)
    scp_errors3 = scp_process3.communicate()[1]

    if scp_process3.returncode:
        return make_response(jsonify({"message": "Something went wrong while passing private key to the Buyer machine",
                            "error": scp_errors3}), 400)


    scp_process4 = helper.transmitPrivateKeyScpProcess(provider_endpoint, remote_path)
    scp_errors4 = scp_process4.communicate()[1]

    if scp_process4.returncode:
        return make_response(jsonify({"message": "Something went wrong while passing private key to the Provider machine",
                            "error": scp_errors4}), 400)

    scp_process5 = helper.transmitPublicKeyScpProcess(provider_endpoint, remote_path)
    scp_errors5 = scp_process5.communicate()[1]

    if scp_process5.returncode:
        return make_response(jsonify({"message": "Something went wrong while passing private key to the Provider machine",
                            "error": scp_errors5}), 400)

    command_list6 = [
        "docker inspect -f \"{a} .NetworkSettings.IPAddress {b}\" {c}".format(a="{{" ,b="}}", c=buyer_id)
    ]

    ssh_process6 = helper.createSshProcess(provider_endpoint, command_list6)
    ipAddress, ssh_errors6 = ssh_process6.communicate()
    ipAddress = ipAddress.rstrip()

    if ssh_process6.returncode:
        return make_response(jsonify({"message": "Something went wrong while checking IP address of the container",
                            "error": ssh_errors6}), 400)
    
    command_list7 = [
        "ssh-keygen -R {}\n".format(ipAddress),
        "sshpass -p fyppassword ssh-copy-id -o StrictHostKeyChecking=no -i /home/centos/.ssh/{} root@{}\n".format(public_key, ipAddress)
    ]      

    ssh_process7 = helper.createSshProcess(provider_endpoint, command_list7)
    ssh_errors7 = ssh_process7.communicate()[1]

    if ssh_process7.returncode:
        return make_response(jsonify({"message": "Something went wrong while passing public key to the container",
                            "error": ssh_errors7}), 400)

    t = Timer(10.0, removeKeys, [provider_endpoint])
    t.start()
    
    return make_response(jsonify({"message":"Passing public key to the container successful", 
                            "output":port_num}), 200)


# Terminating base image container
def terminateContainer(provider_endpoint, buyer_id):
    command_list1 = [
        "docker stop {}\n".format(buyer_id),
        "docker rm {}\n".format(buyer_id)
    ]

    ssh_process1 = helper.createSshProcess(provider_endpoint, command_list1)
    ssh_errors = ssh_process1.communicate()[1]

    if ssh_process1.returncode:
        return make_response(jsonify({"message": "Something went wrong while deleting container",
                            "error": ssh_errors}), 400)
    
    return make_response(jsonify({"message":"Deleting Container successful", 
                            "output":"Successful"}), 200)


BUYER_KEY = os.getenv("BUYER_KEY_PATH")
PROVIDER_KEY = os.getenv("PROVIDER_KEY_PATH")

# Removing keys from provider host after some time
def removeKeys(provider_endpoint):

    index_private = BUYER_KEY.rfind("/")
    private_key = BUYER_KEY[index_private + 1:]

    print(private_key)

    index_public = PROVIDER_KEY.rfind("/")
    public_key = PROVIDER_KEY[index_public + 1:]

    print(public_key)

    remote_path = "/home/centos/.ssh"
    
    command_list1 = [
        "cd {}\n".format(remote_path),
        "rm {a} {b}\n".format(a=private_key, b=public_key)
    ]

    ssh_process1 = helper.createSshProcess(provider_endpoint, command_list1)
    
    if ssh_process1.returncode:
        print("Unsuccessful!")

    print("Successful!")


# Check if port can be used. If the port is already in use, randomly assign another free port in the range [5000, 6000]
# Return newly created port no. 
def checkPort(provider_endpoint, port_num):
    command_list1 = [
        #"docker container ls --format \" {a}.Ports{b} \" -a\n".format(a="{{", b="}}")
        "sudo docker ps -q | sudo xargs -n1 docker port\n"
    ]

    ssh_process1 = helper.createSshProcess(provider_endpoint, command_list1)
    ssh_output1 = ssh_process1.communicate()[0]

    if ssh_process1.returncode:
        print("Something wrong")
    
    if ssh_output1 is '':
        return port_num

    port_list = ssh_output1.rstrip("\n").split("\n")
    for n in range(len(port_list)):
        start = port_list[n].find(":")
        new_item = port_list[n][start+1:]
        port_list[n] = int(new_item)

    fixed_port_num = choice([i for i in range(5000,6000) if i not in port_list])

    return fixed_port_num
    