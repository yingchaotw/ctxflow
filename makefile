# ============================
# 🔧 設定：優先使用 USER_COMPOSE_CMD，如果沒設就自動偵測
# ============================

# 使用者可手動指定，例如 make up COMPOSE_CMD="podman compose"
USER_COMPOSE_CMD ?=

# 自動偵測 COMPOSE_CMD，如果 USER_COMPOSE_CMD 沒指定
ifeq ($(origin USER_COMPOSE_CMD), undefined)
  PODMAN := $(shell command -v podman 2>/dev/null)
  DOCKER_COMPOSE := $(shell command -v docker 2>/dev/null)
  DOCKER_COMPOSE_LEGACY := $(shell command -v docker-compose 2>/dev/null)

# 自動偵測可用的 compose 工具，優先順序：podman → docker compose → docker-compose
  ifneq ($(PODMAN),)
    COMPOSE_CMD := podman compose
  else ifneq ($(DOCKER_COMPOSE),)
    COMPOSE_CMD := docker compose
  else ifneq ($(DOCKER_COMPOSE_LEGACY),)
    COMPOSE_CMD := docker-compose
  else
    $(error ❌ 沒有找到 docker、docker-compose 或 podman，請安裝其中一個工具)
  endif
else
  COMPOSE_CMD := $(USER_COMPOSE_CMD)
endif

# ============================
# Docker / Podman 共用變數
# ============================

COMPOSE_FILES  = --env-file ../.env
COMPOSE_FILES += -f docker-compose.mcp.yml
COMPOSE_FILES += -f docker-compose.n8n.yml 

NETWORK_NAME = internal

# 載入 .env 檔
ifneq (,$(wildcard .env))
	include .env
	export
endif

.PHONY: up down build logs ps restart \
        sh-mcp sh-n8n sh-aiaw network

## 啟動所有服務
up: network
	$(COMPOSE_CMD) $(COMPOSE_FILES) up -d

## 關閉所有服務
down:
	$(COMPOSE_CMD) $(COMPOSE_FILES) down

## 重建所有映像
build:
	$(COMPOSE_CMD) $(COMPOSE_FILES) build

## 查看 log（持續監看）
logs:
	$(COMPOSE_CMD) $(COMPOSE_FILES) logs -f --tail=100

## 查看 container 狀態
ps:
	$(COMPOSE_CMD) $(COMPOSE_FILES) ps

## 重啟服務
restart: down up

## 建立 internal 網路（如果還沒建立）
network:
	@if ! docker network inspect $(NETWORK_NAME) >/dev/null 2>&1; then \
		echo "🔧 建立 network $(NETWORK_NAME)"; \
		docker network create $(NETWORK_NAME); \
	else \
		echo "✅ network $(NETWORK_NAME) 已存在"; \
	fi

## 進入容器 shell（mcp）
sh-mcp:
	@cid=$$(docker ps -qf "name=mcp"); \
	if [ -n "$$cid" ]; then \
		docker exec -it $$cid /bin/sh; \
	else \
		echo "❌ mcp 容器未啟動"; \
	fi

## 進入容器 shell（n8n）
sh-n8n:
	@cid=$$(docker ps -qf "name=n8n"); \
	if [ -n "$$cid" ]; then \
		docker exec -it $$cid /bin/sh; \
	else \
		echo "❌ n8n 容器未啟動"; \
	fi

## 顯示所有可用指令的簡介
help:
	@echo "Available commands:"
	@echo "  up        - Start all services (docker-compose/podman)"
	@echo "  down      - Stop all services"
	@echo "  build     - Rebuild all images"
	@echo "  logs      - Show logs (follow mode)"
	@echo "  ps        - Show container status"
	@echo "  restart   - Restart all services (down + up)"
	@echo "  network   - Ensure the internal Docker network exists"
	@echo "  sh-mcp    - Access the mcp container's shell"
	@echo "  sh-n8n    - Access the n8n container's shell"
	@echo "  help      - Show this help message"