#! /bin/bash

# ssh -o StrictHostKeyChecking=no -i /dcp/keys/FYP_KP.pem -p 2024 centos@3.86.27.38
KEY_PATH=$DCP_KEY_PATH/$DCP_KEY_NAME
ssh -o StrictHostKeyChecking=no -i $KEY_PATH -p $DESTINATION_PORT $DESTINATION_USER@$DESTINATION_IP
