package docker

import (
	"context"
	"fmt"
	"io"
	"strconv"
	"strings"
	"time"

	apiTypes "github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/filters"
	"github.com/docker/docker/client"
	"github.com/sirupsen/logrus"

	"github.com/wrfly/container-web-tty/config"
	"github.com/wrfly/container-web-tty/types"
)

type DockerCli struct {
	cli         *client.Client
	containers  *types.Containers
	listOptions apiTypes.ContainerListOptions
	lastList    time.Time
}

func NewCli(conf config.DockerConfig) (*DockerCli, error) {
	host := conf.DockerHost
	if host[:1] == "/" {
		host = "unix://" + host
	} else {
		host = "tcp://" + host
	}
	version := "v1.24"
	logrus.Infof("Docker connecting to %s", host)
	UA := map[string]string{"User-Agent": "engine-api-cli-1.0"}
	cli, err := client.NewClient(host, version, nil, UA)
	if err != nil {
		logrus.Errorf("create new docker client error: %s", err)
		return nil, err
	}

	// update docker version
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	v, err := cli.ServerVersion(ctx)
	if err != nil {
		return nil, err
	}
	cli, err = client.NewClient(host, v.APIVersion, nil, UA)
	if err != nil {
		logrus.Errorf("create new docker client error: %s", err)
		return nil, err
	}

	listOptions, err := buildListOptions(conf.PsOptions)
	if err != nil {
		return nil, fmt.Errorf("build ps options error: %s", err)
	}
	logrus.Debugf("list options: %+v", listOptions)

	ping, err := cli.Ping(ctx)
	if err != nil {
		return nil, err
	}
	logrus.Infof("New docker client: API [%s]", ping.APIVersion)
	dockerCli := &DockerCli{
		cli:         cli,
		containers:  &types.Containers{},
		listOptions: listOptions,
	}
	logrus.Infof("Warm up containers info...")

	// when docker restarted, should restart the program as well
	// since the socket file is gone (as the restart of docker daemon)
	// see #30
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		dockerCli.listContainers(ctx, true)
		cancel()

		dockerCli.watchEvents() // will block here
		logrus.Fatal("lost connection to docker daemon")
	}()

	return dockerCli, nil
}

func getContainerIP(networkSettings interface{}) (ips []string) {
	defer func() {
		if len(ips) == 0 {
			ips = []string{"null"}
		}
	}()

	if networkSettings == nil {
		return
	}
	switch networkSettings.(type) {
	case *apiTypes.SummaryNetworkSettings:
		network := networkSettings.(*apiTypes.SummaryNetworkSettings)
		for net := range network.Networks {
			if network.Networks[net] == nil {
				continue
			}
			ips = append(ips, network.Networks[net].IPAddress)
		}
	case *apiTypes.NetworkSettings:
		network := networkSettings.(*apiTypes.NetworkSettings)
		for net := range network.Networks {
			if network.Networks[net] == nil {
				continue
			}
			ips = append(ips, network.Networks[net].IPAddress)
		}
	}

	return
}

func (docker *DockerCli) watchEvents() {
	eventChan, errChan := docker.cli.Events(context.Background(), apiTypes.EventsOptions{})

	go func() {
		for event := range eventChan {
			if event.Type != "container" {
				continue
			}
			logrus.Debugf("container event: %+v", event)
			switch event.Action {
			case "start", "destroy":
				ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
				docker.listContainers(ctx, true)
				cancel()
			}
		}
	}()

	logrus.Errorf("docker cli watch events error: %s", <-errChan)
}

func (docker *DockerCli) GetInfo(ctx context.Context, cid string) types.Container {
	if docker.containers.Len() == 0 {
		logrus.Debugf("zero containers, get cid %s", cid)
		docker.List(ctx)
	}

	// find in containers
	if container := docker.containers.Find(cid); container.ID != "" {
		if container.Shell == "" {
			shell := docker.getShell(ctx, cid)
			container.Shell = shell
			docker.containers.SetShell(cid, shell)
		}
		logrus.Debugf("found valid container: %s (%s)", container.ID, container.Shell)
		return container
	}

	// didn't get this container, this is rarelly happens
	cjson, err := docker.cli.ContainerInspect(ctx, cid)
	if err != nil {
		logrus.Errorf("inspect container %s error: %s", cid, err)
		return types.Container{}
	}

	c := docker.convertCjsonToContainre(cjson)
	if c.ID != "" {
		docker.containers.Append(c)
	}
	return c
}

// DCP GetMonitorInfo

func (docker *DockerCli) GetMonitorInfo(ctx context.Context, cid string) types.Container {
	if docker.containers.Len() == 0 {
		logrus.Debugf("zero containers, get cid %s", cid)
		docker.List(ctx)
	}

	// find in containers
	if container := docker.containers.Find(cid); container.ID != "" {
		if container.Shell == "" {
			shell := docker.getMonitorShell(ctx, cid)
			container.Shell = shell
			docker.containers.SetShell(cid, shell)
		}
		logrus.Debugf("found valid container: %s (%s)", container.ID, container.Shell)
		return container
	}

	// didn't get this container, this is rarelly happens
	cjson, err := docker.cli.ContainerInspect(ctx, cid)
	if err != nil {
		logrus.Errorf("inspect container %s error: %s", cid, err)
		return types.Container{}
	}

	c := docker.convertMonitorCjsonToContainre(cjson)
	if c.ID != "" {
		docker.containers.Append(c)
	}
	return c
}


func (docker *DockerCli) convertMonitorCjsonToContainre(cjson apiTypes.ContainerJSON) types.Container {
	if cjson.Config == nil {
		// WTF?
		return types.Container{}
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()
	shell := docker.getMonitorShell(ctx, cjson.ID)

	c := types.Container{
		ID:      cjson.ID,
		Name:    cjson.Name,
		Image:   cjson.Image,
		Command: fmt.Sprintf("%s", cjson.Config.Cmd),
		IPs:     getContainerIP(cjson.NetworkSettings),
		Status:  cjson.State.Status,
		State:   cjson.State.Status,
		Shell:   shell,
	}

	return c
}

func (docker *DockerCli) convertCjsonToContainre(cjson apiTypes.ContainerJSON) types.Container {
	if cjson.Config == nil {
		// WTF?
		return types.Container{}
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()
	shell := docker.getShell(ctx, cjson.ID)

	c := types.Container{
		ID:      cjson.ID,
		Name:    cjson.Name,
		Image:   cjson.Image,
		Command: fmt.Sprintf("%s", cjson.Config.Cmd),
		IPs:     getContainerIP(cjson.NetworkSettings),
		Status:  cjson.State.Status,
		State:   cjson.State.Status,
		Shell:   shell,
	}

	return c
}

func (docker *DockerCli) listContainers(ctx context.Context, force bool) []types.Container {
	if time.Now().Sub(docker.lastList) < time.Minute && !force {
		return docker.containers.List()
	}

	start := time.Now()
	logrus.Debug("list conatiners")
	cs, err := docker.cli.ContainerList(ctx, docker.listOptions)
	if err != nil {
		logrus.Errorf("list containers eror: %s", err)
		return nil
	}

	containers := make([]types.Container, len(cs))
	var (
		ips   []string
		shell string
	)
	for i, container := range cs {
		if old := docker.containers.Find(container.ID); old.ID != "" {
			shell = old.Shell
			ips = old.IPs
		} else {
			ips = getContainerIP(container.NetworkSettings)
		}
		containers[i] = types.Container{
			ID:      container.ID,
			Name:    container.Names[0][1:],
			Image:   container.Image,
			Command: container.Command,
			IPs:     ips,
			Status:  container.Status,
			State:   container.State,
			Shell:   shell,
		}
	}

	docker.containers.Set(containers)

	docker.lastList = time.Now()
	logrus.Debugf("list %d containers, use %s", len(containers), time.Now().Sub(start))
	return containers
}

func (docker *DockerCli) List(ctx context.Context) []types.Container {
	return docker.listContainers(ctx, false)
}

func (docker *DockerCli) exist(ctx context.Context, cid, path string) bool {
	_, err := docker.cli.ContainerStatPath(ctx, cid, path)
	if err != nil {
		return false
	}
	return true
}

func (docker *DockerCli) getShell(ctx context.Context, cid string) string {
	// for _, sh := range config.SHELL_LIST {
	// 	if docker.exist(ctx, cid, sh) {
	// 		logrus.Debugf("container [%s] use [%s]", cid, sh)
	// 		return sh
	// 	}
	// }
	
	// // generally it won't come so far
	// return ""
	// DCP custom
	// if (t == "m"){
	// 	return "/usr/local/bin/dcp-cmonitor-entrypoint.sh"
	// }
	// else{
		return "/usr/local/bin/dcp-tunnel-entrypoint.sh"
	// }

}

func (docker *DockerCli) getMonitorShell(ctx context.Context, cid string) string {
	// DCP custom
	return "/usr/local/bin/dcp-monitor-entrypoint.sh"

}

func (docker *DockerCli) Start(ctx context.Context, cid string) error {
	return docker.cli.ContainerStart(ctx, cid, apiTypes.ContainerStartOptions{})
}

func (docker *DockerCli) Stop(ctx context.Context, cid string) error {
	// Notice: is there a need to config this stop duration?
	duration := time.Second * 5
	return docker.cli.ContainerStop(ctx, cid, &duration)
}

func (docker *DockerCli) Restart(ctx context.Context, cid string) error {
	// restart immediately
	return docker.cli.ContainerRestart(ctx, cid, nil)
}

func buildListOptions(options string) (apiTypes.ContainerListOptions, error) {
	// ["-a", "-f", "key=val"]
	// https://docs.docker.com/engine/reference/commandline/ps/#filtering
	listOptions := apiTypes.ContainerListOptions{Filters: filters.NewArgs()}
	args := strings.Split(options, " ")
	for i, arg := range args {
		switch arg {
		case "-a", "--all":
			listOptions.All = true
		case "-f", "--filter":
			if i+1 < len(arg) {
				f := args[i+1]
				kv := strings.Split(f, "=")
				if len(kv) != 2 {
					return listOptions, fmt.Errorf("bad filter %s", f)
				}
				listOptions.Filters.Add(kv[0], kv[1])
			}
		case "-n", "--last":
			if i+1 < len(arg) {
				f := args[i+1]
				intF, err := strconv.Atoi(f)
				if err != nil {
					return listOptions, err
				}
				listOptions.Limit = intF
			}
		case "-l", "--latest":
			listOptions.Latest = true
		}
	}
	return listOptions, nil
}

func (docker *DockerCli) Exec(ctx context.Context, container types.Container) (types.TTY, error) {
	cmds := []string{container.Shell}
	opts := container.Exec
	if cmd := opts.Cmd; cmd != "" {
		cmds = append(cmds, "-c")
		cmds = append(cmds, fmt.Sprintf("\"\"%s\"\"", cmd))
	}
	logrus.Debugf("exec cmd: %v", cmds)

	execConfig := apiTypes.ExecConfig{
		AttachStdin:  true,
		AttachStderr: true,
		AttachStdout: true,
		Tty:          true,
		Privileged:   opts.Privileged,
		Cmd:          cmds,
		Env:          []string{"HISTCONTROL=ignoredups", "TERM=xterm"},
	}
	if opts.User != "" {
		execConfig.User = opts.User
	}
	if opts.Env != "" {
		execConfig.Env = append(execConfig.Env,
			strings.Split(opts.Env, " ")...)
	}

	response, err := docker.cli.ContainerExecCreate(ctx, container.ID, execConfig)
	if err != nil {
		return nil, err
	}

	execID := response.ID
	if execID == "" {
		return nil, fmt.Errorf("exec ID empty")
	}

	resp, err := docker.cli.ContainerExecAttach(ctx, execID, execConfig)
	if err != nil {
		return nil, err
	}

	resizeFunc := func(width int, height int) error {
		return docker.cli.ContainerExecResize(ctx, execID,
			apiTypes.ResizeOptions{
				Width:  uint(width),
				Height: uint(height),
			})
	}

	return newExecInjector(resp, resizeFunc), nil
}

func (docker *DockerCli) Close() error {
	return docker.cli.Close()
}

func (docker *DockerCli) Logs(ctx context.Context, opts types.LogOptions) (io.ReadCloser, error) {
	return docker.cli.ContainerLogs(ctx, opts.ID, apiTypes.ContainerLogsOptions{
		ShowStderr: true,
		ShowStdout: true,
		Follow:     opts.Follow,
		Tail:       opts.Tail,
	})
}
