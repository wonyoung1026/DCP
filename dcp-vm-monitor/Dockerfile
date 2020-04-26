# =============================================
# SSH tunnel Dockerfile
# =============================================

# NOTE: private key should be in the same directory 
FROM alpine:3.11
ENV DCP_KEY_PATH="/dcp/keys"
ENV DCP_KEY_NAME="FYP_KP.pem"
ENV DCP_ENTRYPOINT_PATH="/usr/local/bin"

RUN apk add --no-cache \
  openssh-client \
  ca-certificates \
  bash && \ 
  mkdir -p ${DCP_KEY_PATH}
COPY secrets/${DCP_KEY_NAME} ${DCP_KEY_PATH}

COPY src/dcp-monitor-entrypoint.sh ${DCP_ENTRYPOINT_PATH}/dcp-monitor-entrypoint.sh

RUN chmod 600 ${DCP_KEY_PATH}/${DCP_KEY_NAME} && \
    chmod +x ${DCP_ENTRYPOINT_PATH}/dcp-monitor-entrypoint.sh
