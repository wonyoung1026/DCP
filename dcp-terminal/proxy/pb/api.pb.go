// Code generated by protoc-gen-go. DO NOT EDIT.
// source: api.proto

/*
Package pbrpc is a generated protocol buffer package.

It is generated from these files:
	api.proto

It has these top-level messages:
	Empty
	Pong
	Err
	ContainerID
	LogOpts
	Container
	Containers
	Io
	WindowSize
	ExecOptions
*/
package pbrpc

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type Empty struct {
	Auth string `protobuf:"bytes,1,opt,name=auth" json:"auth,omitempty"`
}

func (m *Empty) Reset()                    { *m = Empty{} }
func (m *Empty) String() string            { return proto.CompactTextString(m) }
func (*Empty) ProtoMessage()               {}
func (*Empty) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{0} }

func (m *Empty) GetAuth() string {
	if m != nil {
		return m.Auth
	}
	return ""
}

type Pong struct {
	Msg string `protobuf:"bytes,1,opt,name=msg" json:"msg,omitempty"`
}

func (m *Pong) Reset()                    { *m = Pong{} }
func (m *Pong) String() string            { return proto.CompactTextString(m) }
func (*Pong) ProtoMessage()               {}
func (*Pong) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{1} }

func (m *Pong) GetMsg() string {
	if m != nil {
		return m.Msg
	}
	return ""
}

type Err struct {
	Err string `protobuf:"bytes,1,opt,name=err" json:"err,omitempty"`
}

func (m *Err) Reset()                    { *m = Err{} }
func (m *Err) String() string            { return proto.CompactTextString(m) }
func (*Err) ProtoMessage()               {}
func (*Err) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{2} }

func (m *Err) GetErr() string {
	if m != nil {
		return m.Err
	}
	return ""
}

type ContainerID struct {
	Id   string `protobuf:"bytes,1,opt,name=id" json:"id,omitempty"`
	Auth string `protobuf:"bytes,2,opt,name=auth" json:"auth,omitempty"`
}

func (m *ContainerID) Reset()                    { *m = ContainerID{} }
func (m *ContainerID) String() string            { return proto.CompactTextString(m) }
func (*ContainerID) ProtoMessage()               {}
func (*ContainerID) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{3} }

func (m *ContainerID) GetId() string {
	if m != nil {
		return m.Id
	}
	return ""
}

func (m *ContainerID) GetAuth() string {
	if m != nil {
		return m.Auth
	}
	return ""
}

type LogOpts struct {
	C      *ContainerID `protobuf:"bytes,1,opt,name=c" json:"c,omitempty"`
	Follow bool         `protobuf:"varint,2,opt,name=follow" json:"follow,omitempty"`
	Tail   string       `protobuf:"bytes,3,opt,name=tail" json:"tail,omitempty"`
}

func (m *LogOpts) Reset()                    { *m = LogOpts{} }
func (m *LogOpts) String() string            { return proto.CompactTextString(m) }
func (*LogOpts) ProtoMessage()               {}
func (*LogOpts) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{4} }

func (m *LogOpts) GetC() *ContainerID {
	if m != nil {
		return m.C
	}
	return nil
}

func (m *LogOpts) GetFollow() bool {
	if m != nil {
		return m.Follow
	}
	return false
}

func (m *LogOpts) GetTail() string {
	if m != nil {
		return m.Tail
	}
	return ""
}

// Container instance
type Container struct {
	Id            string   `protobuf:"bytes,1,opt,name=id" json:"id,omitempty"`
	Name          string   `protobuf:"bytes,2,opt,name=name" json:"name,omitempty"`
	Image         string   `protobuf:"bytes,3,opt,name=image" json:"image,omitempty"`
	Command       string   `protobuf:"bytes,4,opt,name=command" json:"command,omitempty"`
	State         string   `protobuf:"bytes,5,opt,name=state" json:"state,omitempty"`
	Status        string   `protobuf:"bytes,6,opt,name=status" json:"status,omitempty"`
	Ips           []string `protobuf:"bytes,7,rep,name=ips" json:"ips,omitempty"`
	Shell         string   `protobuf:"bytes,8,opt,name=shell" json:"shell,omitempty"`
	PodName       string   `protobuf:"bytes,9,opt,name=pod_name,json=podName" json:"pod_name,omitempty"`
	ContainerName string   `protobuf:"bytes,10,opt,name=container_name,json=containerName" json:"container_name,omitempty"`
	Namespace     string   `protobuf:"bytes,11,opt,name=namespace" json:"namespace,omitempty"`
	RunningNode   string   `protobuf:"bytes,12,opt,name=running_node,json=runningNode" json:"running_node,omitempty"`
	LocServer     string   `protobuf:"bytes,13,opt,name=loc_server,json=locServer" json:"loc_server,omitempty"`
	ExecCmd       string   `protobuf:"bytes,14,opt,name=execCmd" json:"execCmd,omitempty"`
	ExecUser      string   `protobuf:"bytes,15,opt,name=execUser" json:"execUser,omitempty"`
	ExecEnv       string   `protobuf:"bytes,16,opt,name=execEnv" json:"execEnv,omitempty"`
}

func (m *Container) Reset()                    { *m = Container{} }
func (m *Container) String() string            { return proto.CompactTextString(m) }
func (*Container) ProtoMessage()               {}
func (*Container) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{5} }

func (m *Container) GetId() string {
	if m != nil {
		return m.Id
	}
	return ""
}

func (m *Container) GetName() string {
	if m != nil {
		return m.Name
	}
	return ""
}

func (m *Container) GetImage() string {
	if m != nil {
		return m.Image
	}
	return ""
}

func (m *Container) GetCommand() string {
	if m != nil {
		return m.Command
	}
	return ""
}

func (m *Container) GetState() string {
	if m != nil {
		return m.State
	}
	return ""
}

func (m *Container) GetStatus() string {
	if m != nil {
		return m.Status
	}
	return ""
}

func (m *Container) GetIps() []string {
	if m != nil {
		return m.Ips
	}
	return nil
}

func (m *Container) GetShell() string {
	if m != nil {
		return m.Shell
	}
	return ""
}

func (m *Container) GetPodName() string {
	if m != nil {
		return m.PodName
	}
	return ""
}

func (m *Container) GetContainerName() string {
	if m != nil {
		return m.ContainerName
	}
	return ""
}

func (m *Container) GetNamespace() string {
	if m != nil {
		return m.Namespace
	}
	return ""
}

func (m *Container) GetRunningNode() string {
	if m != nil {
		return m.RunningNode
	}
	return ""
}

func (m *Container) GetLocServer() string {
	if m != nil {
		return m.LocServer
	}
	return ""
}

func (m *Container) GetExecCmd() string {
	if m != nil {
		return m.ExecCmd
	}
	return ""
}

func (m *Container) GetExecUser() string {
	if m != nil {
		return m.ExecUser
	}
	return ""
}

func (m *Container) GetExecEnv() string {
	if m != nil {
		return m.ExecEnv
	}
	return ""
}

type Containers struct {
	Cs []*Container `protobuf:"bytes,1,rep,name=cs" json:"cs,omitempty"`
}

func (m *Containers) Reset()                    { *m = Containers{} }
func (m *Containers) String() string            { return proto.CompactTextString(m) }
func (*Containers) ProtoMessage()               {}
func (*Containers) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{6} }

func (m *Containers) GetCs() []*Container {
	if m != nil {
		return m.Cs
	}
	return nil
}

type Io struct {
	In  []byte `protobuf:"bytes,1,opt,name=in,proto3" json:"in,omitempty"`
	Out []byte `protobuf:"bytes,2,opt,name=out,proto3" json:"out,omitempty"`
}

func (m *Io) Reset()                    { *m = Io{} }
func (m *Io) String() string            { return proto.CompactTextString(m) }
func (*Io) ProtoMessage()               {}
func (*Io) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{7} }

func (m *Io) GetIn() []byte {
	if m != nil {
		return m.In
	}
	return nil
}

func (m *Io) GetOut() []byte {
	if m != nil {
		return m.Out
	}
	return nil
}

type WindowSize struct {
	Height int32 `protobuf:"varint,1,opt,name=height" json:"height,omitempty"`
	Width  int32 `protobuf:"varint,2,opt,name=width" json:"width,omitempty"`
}

func (m *WindowSize) Reset()                    { *m = WindowSize{} }
func (m *WindowSize) String() string            { return proto.CompactTextString(m) }
func (*WindowSize) ProtoMessage()               {}
func (*WindowSize) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{8} }

func (m *WindowSize) GetHeight() int32 {
	if m != nil {
		return m.Height
	}
	return 0
}

func (m *WindowSize) GetWidth() int32 {
	if m != nil {
		return m.Width
	}
	return 0
}

type ExecOptions struct {
	Cmd  *Io         `protobuf:"bytes,1,opt,name=cmd" json:"cmd,omitempty"`
	C    *Container  `protobuf:"bytes,2,opt,name=c" json:"c,omitempty"`
	Err  string      `protobuf:"bytes,3,opt,name=err" json:"err,omitempty"`
	Auth string      `protobuf:"bytes,4,opt,name=auth" json:"auth,omitempty"`
	Ws   *WindowSize `protobuf:"bytes,5,opt,name=ws" json:"ws,omitempty"`
}

func (m *ExecOptions) Reset()                    { *m = ExecOptions{} }
func (m *ExecOptions) String() string            { return proto.CompactTextString(m) }
func (*ExecOptions) ProtoMessage()               {}
func (*ExecOptions) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{9} }

func (m *ExecOptions) GetCmd() *Io {
	if m != nil {
		return m.Cmd
	}
	return nil
}

func (m *ExecOptions) GetC() *Container {
	if m != nil {
		return m.C
	}
	return nil
}

func (m *ExecOptions) GetErr() string {
	if m != nil {
		return m.Err
	}
	return ""
}

func (m *ExecOptions) GetAuth() string {
	if m != nil {
		return m.Auth
	}
	return ""
}

func (m *ExecOptions) GetWs() *WindowSize {
	if m != nil {
		return m.Ws
	}
	return nil
}

func init() {
	proto.RegisterType((*Empty)(nil), "pbrpc.empty")
	proto.RegisterType((*Pong)(nil), "pbrpc.pong")
	proto.RegisterType((*Err)(nil), "pbrpc.err")
	proto.RegisterType((*ContainerID)(nil), "pbrpc.ContainerID")
	proto.RegisterType((*LogOpts)(nil), "pbrpc.logOpts")
	proto.RegisterType((*Container)(nil), "pbrpc.Container")
	proto.RegisterType((*Containers)(nil), "pbrpc.Containers")
	proto.RegisterType((*Io)(nil), "pbrpc.io")
	proto.RegisterType((*WindowSize)(nil), "pbrpc.windowSize")
	proto.RegisterType((*ExecOptions)(nil), "pbrpc.execOptions")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// Client API for ContainerServer service

type ContainerServerClient interface {
	GetInfo(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Container, error)
	List(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*Containers, error)
	Start(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error)
	Stop(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error)
	Restart(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error)
	Exec(ctx context.Context, opts ...grpc.CallOption) (ContainerServer_ExecClient, error)
	Ping(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*Pong, error)
	Logs(ctx context.Context, in *LogOpts, opts ...grpc.CallOption) (ContainerServer_LogsClient, error)
}

type containerServerClient struct {
	cc *grpc.ClientConn
}

func NewContainerServerClient(cc *grpc.ClientConn) ContainerServerClient {
	return &containerServerClient{cc}
}

func (c *containerServerClient) GetInfo(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Container, error) {
	out := new(Container)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/GetInfo", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) List(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*Containers, error) {
	out := new(Containers)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/List", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) Start(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error) {
	out := new(Err)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/Start", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) Stop(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error) {
	out := new(Err)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/Stop", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) Restart(ctx context.Context, in *ContainerID, opts ...grpc.CallOption) (*Err, error) {
	out := new(Err)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/Restart", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) Exec(ctx context.Context, opts ...grpc.CallOption) (ContainerServer_ExecClient, error) {
	stream, err := grpc.NewClientStream(ctx, &_ContainerServer_serviceDesc.Streams[0], c.cc, "/pbrpc.containerServer/Exec", opts...)
	if err != nil {
		return nil, err
	}
	x := &containerServerExecClient{stream}
	return x, nil
}

type ContainerServer_ExecClient interface {
	Send(*ExecOptions) error
	Recv() (*ExecOptions, error)
	grpc.ClientStream
}

type containerServerExecClient struct {
	grpc.ClientStream
}

func (x *containerServerExecClient) Send(m *ExecOptions) error {
	return x.ClientStream.SendMsg(m)
}

func (x *containerServerExecClient) Recv() (*ExecOptions, error) {
	m := new(ExecOptions)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *containerServerClient) Ping(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*Pong, error) {
	out := new(Pong)
	err := grpc.Invoke(ctx, "/pbrpc.containerServer/Ping", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *containerServerClient) Logs(ctx context.Context, in *LogOpts, opts ...grpc.CallOption) (ContainerServer_LogsClient, error) {
	stream, err := grpc.NewClientStream(ctx, &_ContainerServer_serviceDesc.Streams[1], c.cc, "/pbrpc.containerServer/Logs", opts...)
	if err != nil {
		return nil, err
	}
	x := &containerServerLogsClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type ContainerServer_LogsClient interface {
	Recv() (*Io, error)
	grpc.ClientStream
}

type containerServerLogsClient struct {
	grpc.ClientStream
}

func (x *containerServerLogsClient) Recv() (*Io, error) {
	m := new(Io)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// Server API for ContainerServer service

type ContainerServerServer interface {
	GetInfo(context.Context, *ContainerID) (*Container, error)
	List(context.Context, *Empty) (*Containers, error)
	Start(context.Context, *ContainerID) (*Err, error)
	Stop(context.Context, *ContainerID) (*Err, error)
	Restart(context.Context, *ContainerID) (*Err, error)
	Exec(ContainerServer_ExecServer) error
	Ping(context.Context, *Empty) (*Pong, error)
	Logs(*LogOpts, ContainerServer_LogsServer) error
}

func RegisterContainerServerServer(s *grpc.Server, srv ContainerServerServer) {
	s.RegisterService(&_ContainerServer_serviceDesc, srv)
}

func _ContainerServer_GetInfo_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ContainerID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).GetInfo(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/GetInfo",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).GetInfo(ctx, req.(*ContainerID))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_List_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).List(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/List",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).List(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_Start_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ContainerID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).Start(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/Start",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).Start(ctx, req.(*ContainerID))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_Stop_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ContainerID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).Stop(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/Stop",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).Stop(ctx, req.(*ContainerID))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_Restart_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ContainerID)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).Restart(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/Restart",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).Restart(ctx, req.(*ContainerID))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_Exec_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(ContainerServerServer).Exec(&containerServerExecServer{stream})
}

type ContainerServer_ExecServer interface {
	Send(*ExecOptions) error
	Recv() (*ExecOptions, error)
	grpc.ServerStream
}

type containerServerExecServer struct {
	grpc.ServerStream
}

func (x *containerServerExecServer) Send(m *ExecOptions) error {
	return x.ServerStream.SendMsg(m)
}

func (x *containerServerExecServer) Recv() (*ExecOptions, error) {
	m := new(ExecOptions)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func _ContainerServer_Ping_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ContainerServerServer).Ping(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pbrpc.containerServer/Ping",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ContainerServerServer).Ping(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _ContainerServer_Logs_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(LogOpts)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(ContainerServerServer).Logs(m, &containerServerLogsServer{stream})
}

type ContainerServer_LogsServer interface {
	Send(*Io) error
	grpc.ServerStream
}

type containerServerLogsServer struct {
	grpc.ServerStream
}

func (x *containerServerLogsServer) Send(m *Io) error {
	return x.ServerStream.SendMsg(m)
}

var _ContainerServer_serviceDesc = grpc.ServiceDesc{
	ServiceName: "pbrpc.containerServer",
	HandlerType: (*ContainerServerServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetInfo",
			Handler:    _ContainerServer_GetInfo_Handler,
		},
		{
			MethodName: "List",
			Handler:    _ContainerServer_List_Handler,
		},
		{
			MethodName: "Start",
			Handler:    _ContainerServer_Start_Handler,
		},
		{
			MethodName: "Stop",
			Handler:    _ContainerServer_Stop_Handler,
		},
		{
			MethodName: "Restart",
			Handler:    _ContainerServer_Restart_Handler,
		},
		{
			MethodName: "Ping",
			Handler:    _ContainerServer_Ping_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "Exec",
			Handler:       _ContainerServer_Exec_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
		{
			StreamName:    "Logs",
			Handler:       _ContainerServer_Logs_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "api.proto",
}

func init() { proto.RegisterFile("api.proto", fileDescriptor0) }

var fileDescriptor0 = []byte{
	// 664 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x8c, 0x54, 0xcd, 0x6e, 0xdb, 0x38,
	0x10, 0xb6, 0x7e, 0x1c, 0xdb, 0x23, 0xc7, 0x49, 0x88, 0xc5, 0x2e, 0xd7, 0xd9, 0x2d, 0x1c, 0x15,
	0x29, 0x5c, 0x14, 0x30, 0x12, 0xb7, 0xa7, 0x5e, 0xd3, 0xa0, 0x08, 0x10, 0x24, 0x85, 0x8c, 0xa2,
	0xc7, 0x40, 0x91, 0x18, 0x99, 0x80, 0x44, 0x12, 0x24, 0x1d, 0xa7, 0x7d, 0x8d, 0x3e, 0x44, 0x1f,
	0xb0, 0x2f, 0x50, 0x90, 0xa2, 0xe4, 0x20, 0xf1, 0x21, 0xb7, 0xf9, 0x66, 0xbe, 0x19, 0x7d, 0xe2,
	0x37, 0x24, 0x0c, 0x52, 0x41, 0x67, 0x42, 0x72, 0xcd, 0x51, 0x57, 0xdc, 0x4a, 0x91, 0xc5, 0x87,
	0xd0, 0x25, 0x95, 0xd0, 0xdf, 0x11, 0x82, 0x30, 0x5d, 0xe9, 0x25, 0xf6, 0x26, 0xde, 0x74, 0x90,
	0xd8, 0x38, 0xc6, 0x10, 0x0a, 0xce, 0x0a, 0xb4, 0x0f, 0x41, 0xa5, 0x0a, 0x57, 0x32, 0x61, 0xfc,
	0x0f, 0x04, 0x44, 0x4a, 0x53, 0x20, 0x52, 0x36, 0x05, 0x22, 0x65, 0x7c, 0x0a, 0xd1, 0x19, 0x67,
	0x3a, 0xa5, 0x8c, 0xc8, 0x8b, 0x4f, 0x68, 0x04, 0x3e, 0xcd, 0x5d, 0xdd, 0xa7, 0x79, 0xfb, 0x15,
	0xff, 0xd1, 0x57, 0xbe, 0x41, 0xaf, 0xe4, 0xc5, 0xb5, 0xd0, 0x0a, 0x4d, 0xc0, 0xcb, 0x2c, 0x3b,
	0x9a, 0xa3, 0x99, 0x15, 0x38, 0x7b, 0x34, 0x2d, 0xf1, 0x32, 0xf4, 0x37, 0xec, 0xdc, 0xf1, 0xb2,
	0xe4, 0x6b, 0x3b, 0xa2, 0x9f, 0x38, 0x64, 0x06, 0xeb, 0x94, 0x96, 0x38, 0xa8, 0x07, 0x9b, 0x38,
	0xfe, 0x15, 0xc0, 0xa0, 0x6d, 0xdf, 0x26, 0x85, 0xa5, 0x15, 0x69, 0xa4, 0x98, 0x18, 0xfd, 0x05,
	0x5d, 0x5a, 0xa5, 0x05, 0x71, 0x63, 0x6a, 0x80, 0x30, 0xf4, 0x32, 0x5e, 0x55, 0x29, 0xcb, 0x71,
	0x68, 0xf3, 0x0d, 0x34, 0x7c, 0xa5, 0x53, 0x4d, 0x70, 0xb7, 0xe6, 0x5b, 0x60, 0x34, 0x9a, 0x60,
	0xa5, 0xf0, 0x8e, 0x4d, 0x3b, 0x64, 0x4e, 0x8b, 0x0a, 0x85, 0x7b, 0x93, 0xc0, 0x9c, 0x16, 0x15,
	0xca, 0xf6, 0x2f, 0x49, 0x59, 0xe2, 0xbe, 0xeb, 0x37, 0x00, 0xfd, 0x0b, 0x7d, 0xc1, 0xf3, 0x1b,
	0xab, 0x6e, 0x50, 0x7f, 0x50, 0xf0, 0xfc, 0xca, 0x08, 0x3c, 0x86, 0x51, 0xd6, 0xfc, 0x51, 0x4d,
	0x00, 0x4b, 0xd8, 0x6d, 0xb3, 0x96, 0xf6, 0x1f, 0x0c, 0x4c, 0x51, 0x89, 0x34, 0x23, 0x38, 0xb2,
	0x8c, 0x4d, 0x02, 0x1d, 0xc1, 0x50, 0xae, 0x18, 0xa3, 0xac, 0xb8, 0x61, 0x3c, 0x27, 0x78, 0x68,
	0x09, 0x91, 0xcb, 0x5d, 0xf1, 0x9c, 0xa0, 0xff, 0x01, 0x4a, 0x9e, 0xdd, 0x28, 0x22, 0xef, 0x89,
	0xc4, 0xbb, 0xf5, 0x84, 0x92, 0x67, 0x0b, 0x9b, 0x30, 0x27, 0x42, 0x1e, 0x48, 0x76, 0x56, 0xe5,
	0x78, 0x54, 0x0b, 0x74, 0x10, 0x8d, 0xa1, 0x6f, 0xc2, 0xaf, 0x8a, 0x48, 0xbc, 0x67, 0x4b, 0x2d,
	0x6e, 0xba, 0xce, 0xd9, 0x3d, 0xde, 0xdf, 0x74, 0x9d, 0xb3, 0xfb, 0x78, 0x06, 0xd0, 0x1a, 0x65,
	0xb6, 0xc0, 0xcf, 0x14, 0xf6, 0x26, 0xc1, 0x34, 0x9a, 0xef, 0x3f, 0x5d, 0x83, 0xc4, 0xcf, 0x54,
	0xfc, 0x06, 0x7c, 0xca, 0xad, 0xa3, 0xcc, 0x3a, 0x3a, 0x4c, 0x7c, 0xca, 0xcc, 0xf9, 0xf2, 0x95,
	0xb6, 0x86, 0x0e, 0x13, 0x13, 0xc6, 0x1f, 0x01, 0xd6, 0x94, 0xe5, 0x7c, 0xbd, 0xa0, 0x3f, 0xac,
	0x2f, 0x4b, 0x42, 0x8b, 0xa5, 0xb6, 0x3d, 0xdd, 0xc4, 0x21, 0xe3, 0xc2, 0x9a, 0xe6, 0x6e, 0x2b,
	0xbb, 0x49, 0x0d, 0xe2, 0x9f, 0x1e, 0x44, 0x46, 0xdf, 0xb5, 0xd0, 0x94, 0x33, 0x85, 0x0e, 0x21,
	0xc8, 0xaa, 0xdc, 0x6d, 0xe7, 0xc0, 0xc9, 0xa2, 0x3c, 0x31, 0x59, 0xf4, 0xca, 0x2c, 0xae, 0x6f,
	0x4b, 0xcf, 0x15, 0x7b, 0x59, 0x73, 0x51, 0x82, 0xf6, 0xa2, 0xb4, 0x37, 0x21, 0xdc, 0xdc, 0x04,
	0x74, 0x04, 0xfe, 0x5a, 0xd9, 0x5d, 0x8a, 0xe6, 0x07, 0x6e, 0xcc, 0x46, 0x7f, 0xe2, 0xaf, 0xd5,
	0xfc, 0xb7, 0x0f, 0x7b, 0xad, 0xd7, 0xce, 0x8d, 0x53, 0xe8, 0x7d, 0x26, 0xfa, 0x82, 0xdd, 0x71,
	0xb4, 0xe5, 0xd6, 0x8c, 0x9f, 0x09, 0x8a, 0x3b, 0xe8, 0x2d, 0x84, 0x97, 0x54, 0x69, 0x34, 0x74,
	0x35, 0xfb, 0x06, 0x8c, 0x0f, 0x9e, 0x32, 0x95, 0xa5, 0x76, 0x17, 0x3a, 0x95, 0x7a, 0xeb, 0x6c,
	0x68, 0xfa, 0xa5, 0x99, 0x3a, 0x85, 0x70, 0xa1, 0xb9, 0x78, 0x01, 0xf3, 0x1d, 0xf4, 0x12, 0xa2,
	0x5e, 0x38, 0xf6, 0x03, 0x84, 0xe7, 0x0f, 0x24, 0x6b, 0x99, 0x8f, 0x5c, 0x19, 0x6f, 0xc9, 0xc5,
	0x9d, 0xa9, 0x77, 0xe2, 0xa1, 0xd7, 0x10, 0x7e, 0xa1, 0xac, 0x78, 0xf2, 0x8b, 0x91, 0x43, 0xe6,
	0x5d, 0x8b, 0x3b, 0xe8, 0x18, 0xc2, 0x4b, 0x5e, 0x28, 0x34, 0x72, 0x69, 0xf7, 0x10, 0x8d, 0x37,
	0xfe, 0xc6, 0x9d, 0x13, 0xef, 0x76, 0xc7, 0xbe, 0x99, 0xef, 0xff, 0x04, 0x00, 0x00, 0xff, 0xff,
	0xd5, 0x70, 0x81, 0x92, 0x40, 0x05, 0x00, 0x00,
}
