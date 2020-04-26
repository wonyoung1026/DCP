#! /bin/bash
KEY_PATH=$DCP_KEY_PATH/$DCP_KEY_NAME
ssh -o StrictHostKeyChecking=no -t -t -i $KEY_PATH $DESTINATION_USER@$DESTINATION_IP << EOF
    glances -t 5 --disable-process --disable-log --disable-autodiscover --hide-kernel-threads
EOF
