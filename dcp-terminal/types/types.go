package types

// Container instance
type Container struct {
	// common
	ID, Name       string
	Image, Command string
	State, Status  string // "running"  "Up 13 minutes"
	IPs            []string
	Shell          string

	// k8s
	PodName, ContainerName string
	Namespace, RunningNode string

	// remote location server address
	// use this to locate the container
	// in the proxy mode
	LocServer string

	// exec commands in arguments
	// permit user to execute any command
	// in that container
	Exec ExecOptions
}

// ContainerActionMessage tells the web browser the action's status
type ContainerActionMessage struct {
	Error   string `json:"err"`
	Code    int    `json:"code"`
	Message string `json:"msg"`
}

type InitMessage struct {
	Arguments string `json:"Arguments,omitempty"`
	AuthToken string `json:"AuthToken,omitempty"`
}

type LogOptions struct {
	ID     string
	Follow bool
	Tail   string
}

type ContainerAct int

const (
	EXEC ContainerAct = iota
	LOGS
)

type ExecOptions struct {
	User string
	Env  string
	Cmd  string
	// alias as `p`
	Privileged bool
}
