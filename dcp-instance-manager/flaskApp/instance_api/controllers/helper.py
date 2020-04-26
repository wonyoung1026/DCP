
from subprocess import Popen, PIPE
import os
import io

MASTER_KEY_DIR = os.getenv("MASTER_PRIVATE_KEY_DIR")
MASTER_USERNAME = os.getenv("MASTER_USERNAME")
BUYER_KEY = os.getenv("BUYER_KEY_PATH")
PROVIDER_KEY = os.getenv("PROVIDER_KEY_PATH")

def createSshProcess(provider_endpoint, command_list):
    proc= Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '{a}'.format(a=MASTER_KEY_DIR), '{b}@{c}'.format(b=MASTER_USERNAME, c=provider_endpoint)], 
                    stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    universal_newlines=True, bufsize=1)
    
    for command in command_list:
        proc.stdin.write(command)

    return proc

def createScpProcess(local_file_path, remote_address, remote_file_path):
    return Popen(["scp", "-o", "StrictHostKeyChecking=no","-i", MASTER_KEY_DIR, "-r", local_file_path, "{}@{}:{}".format(MASTER_USERNAME, remote_address, remote_file_path)])

def transmitPrivateKeyScpProcess(remote_address, remote_key_path):
    return Popen(['scp', '-o', 'StrictHostKeyChecking=no', '-i', MASTER_KEY_DIR, BUYER_KEY,  '{}@{}:{}'.format(MASTER_USERNAME, remote_address, remote_key_path)])

def transmitPublicKeyScpProcess(remote_address, remote_key_path):
    return Popen(['scp', '-o', 'StrictHostKeyChecking=no', '-i', MASTER_KEY_DIR, PROVIDER_KEY,  '{}@{}:{}'.format(MASTER_USERNAME, remote_address, remote_key_path)])
