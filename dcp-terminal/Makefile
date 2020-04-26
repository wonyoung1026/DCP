NAME = container-web-tty
PKG = github.com/wrfly/$(NAME)
BIN = bin
IMAGE := wrfly/$(NAME)

VERSION := $(shell cat VERSION)
COMMITID := $(shell git rev-parse --short HEAD)
BUILDAT := $(shell date +%Y-%m-%d)

CTIMEVAR = -X main.CommitID=$(COMMITID) \
	-X main.Version=$(VERSION) \
	-X main.BuildAt=$(BUILDAT)
GO_LDFLAGS = -ldflags "-s -w $(CTIMEVAR)"
GO_LDFLAGS_STATIC = -ldflags "-w $(CTIMEVAR) -extldflags -static"

export GO111MODULE=on

.PHONY: build
build:
	mkdir -p bin
	CGO_ENABLED=0 go build $(GO_LDFLAGS) -o $(BIN)/$(NAME) .

.PHONY: test
test:
	go test -cover -v ./...

.PHONY: dev
dev: asset build
	./$(BIN)/$(NAME) -d

.PHONY: release
release:
	GOOS=linux GOARCH=amd64 go build $(GO_LDFLAGS) -o $(BIN)/$(NAME)_linux_amd64 .
	GOOS=darwin GOARCH=amd64 go build $(GO_LDFLAGS) -o $(BIN)/$(NAME)_darwin_amd64 .
	tar -C $(BIN) -czf $(BIN)/$(NAME)_linux_amd64.tgz $(NAME)_linux_amd64
	tar -C $(BIN) -czf $(BIN)/$(NAME)_darwin_amd64.tgz $(NAME)_darwin_amd64

.PHONY: image
image:
	docker build -t $(IMAGE) .

.PHONY: push-image
push-image:
	docker push $(IMAGE)

.PHONY: push-develop
push-develop:
	docker tag $(IMAGE) $(IMAGE):develop
	docker push $(IMAGE):develop

.PHONY: push-tag
push-tag:
	docker tag $(IMAGE) $(IMAGE):$(VERSION)
	docker push $(IMAGE):$(VERSION)

.PHONY: api
api:
	protoc -I proxy/pb proxy/pb/api.proto --go_out=plugins=grpc:proxy/pb/

.PHONY: proto
proto:
	proteus proto -f /tmp -p github.com/wrfly/container-web-tty/types --verbose
	cp /tmp/github.com/wrfly/container-web-tty/types/generated.proto proxy/pb

## --- these stages are copied from gotty for asset building --- ##
.PHONY: asset
asset: clear static/js static/css static/html
	bindata \
		-pkg $(PKG)/route/asset \
		-src static/

clear:
	rm -rf static

static:
	mkdir -p static

static/html: static
	cp resources/*.html static/
	cp resources/favicon.png static/favicon.png

static/js: static js/dist/gotty-bundle.js
	mkdir -p static/js
	cp resources/*.js static/js/
	cp js/dist/gotty-bundle.js static/js/gotty-bundle.js

static/css: static js/node_modules/xterm/css/xterm.css
	mkdir -p static/css
	cp resources/*.css static/css
	cp js/node_modules/xterm/css/xterm.css static/css/xterm.css

js/node_modules/xterm/dist/xterm.css:
	cd js && \
	npm install

# .PHONY: js/dist/gotty-bundle.js
js/dist/gotty-bundle.js: js/node_modules/webpack
	cd js && \
	`npm bin`/webpack

js/node_modules/webpack:
	cd js && \
	npm install

tools:
	go get github.com/wrfly/bindata

genOptions:
	@$(BIN)/$(NAME) -h | \
		grep -A 100 OPTION | \
		sed "s/(default.*//" | \
		sed "s/\\[.*//g"