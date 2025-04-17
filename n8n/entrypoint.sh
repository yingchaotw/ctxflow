#!/bin/sh

# 輸出啟動腳本的日誌，方便 debug
echo "⏳ 啟動腳本開始..."

# 啟動 n8n 背景執行
n8n start &

# 等待 n8n 真的跑起來
echo "⏳ 等待 n8n API 啟動..."
until curl -u $N8N_BASIC_AUTH_USER:$N8N_BASIC_AUTH_PASSWORD -s http://localhost:5678/rest/workflows > /dev/null; do
  echo "⏳ n8n 尚未啟動，等待中..."
  sleep 2
done

# 匯入 workflow（會略過重複）
echo "🚀 匯入 MCP workflow..."
curl -X POST http://localhost:5678/rest/workflows \
  -u $N8N_BASIC_AUTH_USER:$N8N_BASIC_AUTH_PASSWORD \
  -H "Content-Type: application/json" \
  -d @/data/mcp-workflow.json

# 防止 container 結束
echo "🕐 等待容器中的進程..."
wait