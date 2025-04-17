
# Docker/Podman

這個專案使用 Docker 或 Podman 來管理容器化的服務。透過簡單的 Makefile 命令，可以輕鬆啟動、關閉、重建、查看服務狀態，並進行容器的操作。

## 先決條件

請確保已經安裝 Docker 或 Podman。你可以選擇使用其中之一來使用這個 Makefile：

- **Docker** 或 **Docker Compose** [Docker 安裝指南](https://docs.docker.com/get-docker/)
- **Podman** [Podman 安裝指南](https://podman.io/getting-started/installation)

如果沒有手動設定 `USER_COMPOSE_CMD`，Makefile 會自動偵測並使用 `podman` → `docker compose` → `docker-compose` 的順序，選擇其中一個作為 `COMPOSE_CMD`。

## 設定

### 1. 手動指定 Compose 工具

如果你希望手動指定使用的 Compose 工具，可以在執行 `make` 指令時，透過 `COMPOSE_CMD` 變數來設定。例如：

```bash
make up COMPOSE_CMD="podman compose"
```

### 2. 自動偵測 Compose 工具

如果沒設定 `COMPOSE_CMD`，Makefile 會自動偵測是否有安裝以下工具，並按順序選擇：

- `podman`
- `docker compose`
- `docker-compose`

如果都沒安裝，會顯示錯誤訊息，並提示你安裝其中一個工具。

### 3. `.env` 檔案

如果專案中有 `.env` 檔案，Makefile 會自動載入並將其中的變數匯入到環境變數中。

## 可用命令

以下是可以在專案根目錄使用的命令：

| 命令              | 描述                                                             |
|-------------------|------------------------------------------------------------------|
| `make up`         | 啟動所有服務，並確保所需的 Docker 網路已存在。如果網路尚未建立，會自動建立。 |
| `make down`       | 關閉所有服務並停止所有容器。                                       |
| `make build`      | 重建所有映像檔，通常用於更新或修改容器映像後。                     |
| `make logs`       | 查看所有容器的運行日誌，並持續監控。會顯示最近 100 行的日誌。       |
| `make ps`         | 查看所有容器的當前狀態，包括是否正在運行。                         |
| `make restart`    | 重啟所有服務，相當於先停止所有容器，再啟動它們。                   |
| `make network`    | 檢查並確保內部的 Docker 網路存在。如果不存在，會自動建立它。           |
| `make sh-mcp`     | 進入名為 `mcp` 的容器，並啟動一個 shell 會話。                     |
| `make sh-n8n`     | 進入名為 `n8n` 的容器，並啟動一個 shell 會話。                     |
| `make help`       | 顯示所有可用的命令及其簡要說明。                                   |

## 範例

### 啟動服務：

```bash
make up
```

### 查看容器狀態：

```bash
make ps
```

### 查看容器日誌：

```bash
make logs
```

### 進入 `mcp` 容器的 shell：

```bash
make sh-mcp
```

## 開發環境

- 請確保安裝了 Docker 或 Podman。
- 確保 `docker-compose.mcp.yml` 和 `docker-compose.n8n.yml` 等配置檔案存在。

## 常見問題與排錯

- **容器未啟動**：如果容器未啟動，可以使用 `make logs` 查看詳細的錯誤訊息。
- **網路不存在**：如果發現 Docker 網路不存在，可以使用 `make network` 來創建網路。

## 注意事項

- 在執行 `make` 命令前，確保容器映像檔已經建立。
- 若容器未啟動，進入容器的命令將無法執行。
