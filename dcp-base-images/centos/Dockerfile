# Wrapper around centos-ssh for DCP 
# More details here : https://hub.docker.com/r/jdeathe/centos-ssh
FROM jdeathe/centos-ssh:2.6.1

ARG SKEL_PATH=/etc/skel
RUN mv ${SKEL_PATH}/.bashrc ${SKEL_PATH}/.bashrc.old

COPY /centos/src/dcp-bash ${SKEL_PATH}/.bashrc

CMD ["/usr/bin/supervisord", "--configuration=/etc/supervisord.conf"]