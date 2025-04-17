# main.py

import os
from dotenv import load_dotenv  # 用於加載 .env 文件
from mcp_server import app as fastapi_app  # FastAPI 的 app
from mcp_server import dispatcher  # ✅ 原本 app.py 匯入的地方

# 這邊不用跑 uvicorn，Dockerfile 會跑

# 加載 .env 文件
load_dotenv()

# 初始化 plugins
print("📦 初始化 MCP Plugin / Agent 中...")
_ = dispatcher.AGENTS  # 強制載入 agents

print("✅ 初始化完成")

# 讀取 API KEY（可選，或直接在別的地方用 os.getenv() 取）
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

# 可選：debug log
print(f"✅ Loaded API Keys")
print(f"🔑 OpenAI: {openai_key[:6]}...")  # 不建議印全 Key，安全性
print(f"🔑 Gemini: {gemini_key[:6]}...")
print(f"🔑 DeepSeek: {deepseek_key[:6]}...")