
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yingchaotw/ctxflow)


# 🧠 ctxflow

ctxflow（context + workflow）整合了 MCP Server 和 n8n，為您提供一個自動化流程平台。  
利用 Docker Compose 管理多容器架構，輕鬆實現 AI 上下文處理和工作流程串接。

> [!CAUTION]
> - 切勿將 `.env` 文件推送到公開倉庫。  
> - `.env` 檔案包含敏感資料（如 API 金鑰），請妥善管理。

---

## 📦 架構

```bash
private_deploy                    # 儲存私密的 API 金鑰與環境變數（.env 檔案）
├── ctxflow/                      # ctxflow 子模組（包含 MCP Server 和 n8n 配置）
│   ├── LICENSE                   # 開放源碼授權（MIT License）
│   ├── .github                   # GitHub 配置資料夾，包含 CI/CD 配置
│   ├── .gitignore                # Git 忽略檔案，指定不追蹤的檔案與資料夾
│   ├── Readme.md                 # 這個專案的 README 檔案，包含專案簡介與使用說明
│   ├── docker-compose.mcp.yml    # MCP Server 的 Docker Compose 配置檔案
│   ├── docker-compose.n8n.yml    # n8n 的 Docker Compose 配置檔案
│   ├── docker-compose.yml        # 統一的 Docker Compose 配置檔案，包含 MCP 和 n8n
│   ├── docker.md                 # 介紹如何安裝和配置容器引擎
│   ├── makefile                  # Makefile 配置檔案，用於管理常用的 Docker 操作指令
│   ├── mcp-server                # MCP 伺服器相關檔案
│   │   ├── Dockerfile            # MCP Server 的 Dockerfile，指定如何構建 MCP Server 映像
│   │   ├── agents                # 存放 MCP 代理程式（例如 chatgpt_agent.py、rag_agent.py 等）
│   │   │   ├── __init__.py       # 初始化代理程式的模組
│   │   │   ├── chatgpt_agent.py  # ChatGPT 代理程式
│   │   │   ├── claude_agent.py   # Claude 代理程式
│   │   │   ├── gmail_agnet.py    # Gmail 代理程式
│   │   │   └── rag_agent.py      # RAG（Retriever-Augmented Generation）代理程式
│   │   ├── core                  # 核心邏輯
│   │   │   └── messages.py       # 用於處理訊息的邏輯模組
│   │   ├── dispatcher.py         # 載入代理程式並進行處理的調度器
│   │   ├── main.py               # 程式進入點，啟動 FastAPI 應用
│   │   ├── mcp_server.py         # FastAPI 應用程式配置，負責處理 API 請求
│   │   └── requirements.txt      # MCP Server 所需的 Python 套件
│   └── n8n                       # n8n 配置檔案
│       ├── Dockerfile            # 自建的 n8n 映像的 Dockerfile
│       ├── entrypoint.sh         # n8n 容器啟動時執行的腳本
│       └── mcp-workflow.json     # n8n 工作流程配置檔案，包含工作流設計
├── .env                          # 環境變數設定檔，包含專案的 API 金鑰與其他配置
└── n8n_data                      # n8n 資料存放位置（將容器內部的 /home/node/.n8n 目錄映射到這裡）
    ├── binaryData                # n8n 的二進制檔案資料
    ├── config                    # n8n 的配置資料夾
    ├── crash.journal             # n8n 崩潰日誌檔案
    ├── database.sqlite           # n8n 資料庫檔案，儲存工作流程與執行紀錄
    ├── git                       # 用於存放 Git 配置
    ├── n8nEventLog-1.log         # n8n 事件日誌檔案
    ├── n8nEventLog.log           # n8n 事件日誌檔案
    └── ssh                       # 用於 n8n 連接 SSH 的資料夾

```

---

## 🚀 使用方式

### 1. 修改 `.env` 設定環境變數

> [!NOTE]
> 參考 `.env.example` 重新命名為 `.env`，並設置所需的環境變數。以下是範例：
> ```bash
> MCP_API_KEY=your_api_key_here
> N8N_USERNAME=your_n8n_username
> N8N_PASSWORD=your_n8n_password
> ```

### 2. 啟動服務

使用以下指令來啟動服務：

```bash
docker-compose up --build
```

啟動後，可以通過以下 URL 訪問服務：
- MCP Server ➜ [http://localhost:8000](http://localhost:8000)
- n8n ➜ [http://localhost:5678](http://localhost:5678)

### 3. 關閉服務

停止服務並移除容器：

```bash
docker-compose down     # 停止容器
docker-compose down -v  # 停止並刪除所有資源（包括容器、網路、卷等）
```

### 4. 其他指令

```bash
docker-compose ps    # 查看容器狀態
docker-compose start # 啟動容器
docker-compose stop  # 停止容器
docker-compose logs  # 查看日誌
```

---

## 🔁 測試 MCP API

您可以使用 `curl` 測試 MCP API：

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u001", "message": "Hi"}'
```

---

## 📡 測試 n8n → MCP

在 n8n 中建立 webhook 節點和 HTTP request

 節點，並將其配置為呼叫 MCP API 並返回處理資料。

---

## ✅ 未來可以做的事

- 整合更多 AI 技術，如 RAG 和 LLM。
- 使用 n8n 設定定時觸發，管理資料 pipeline。
- 擴展服務，加入 Redis、Postgres 等資料庫或快取系統。

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.