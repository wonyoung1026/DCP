package route

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
)

func (server *Server) handleMonitorRedirect(c *gin.Context) {
	containerID := c.Param("cid")
	execID := server.setContainerID(containerID)
	if query := c.Request.URL.RawQuery; query != "" {
		c.Redirect(302, "/monitor/"+execID+"?"+c.Request.URL.RawQuery)
	} else {
		c.Redirect(302, "/monitor/"+execID)
	}
}

func (server *Server) handleMonitor(c *gin.Context, counter *counter) {
	execID := c.Param("eid")
	containerID, ok := server.getContainerID(execID)
	if !ok {
		c.String(http.StatusBadRequest, fmt.Sprintf("exec id %s not found", execID))
		return
	}

	server.m.RLock()
	masterTTY, ok := server.masters[execID]
	server.m.RUnlock()
	if ok { // exec ID exist, use the same master
		log.Infof("using exist master for exec %s", execID)
		server.processShare(c, execID, masterTTY)
		return
	}

	cInfo := server.containerCli.GetMonitorInfo(c.Request.Context(), containerID)
	server.generateHandleWS(c.Request.Context(), execID, counter, cInfo).
		ServeHTTP(c.Writer, c.Request)
}

