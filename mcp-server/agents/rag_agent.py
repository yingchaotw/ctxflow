# mcp-server/agents/rag_agent.py
import openai
from your_vector_database import VectorDatabase  # 這裡是指向向量資料庫
from mcp_server.messages import MCPMessage

class RAGAgent:
    def __init__(self):
        self.db = VectorDatabase()  # 初始化向量資料庫
        openai.api_key = 'your-openai-api-key'

    def handle(self, message: MCPMessage):
        if message.action != "chat":
            return {"error": f"Unsupported action: {message.action}"}
        
        # Step 1: 從資料庫中檢索與訊息相關的資料
        query_result = self.db.search(message.content)
        
        # Step 2: 使用 LLM（GPT-4）生成回應，並把檢索結果放進去
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"你可以從以下資料中生成回應：\n{query_result}\n用於回答：{message.content}",
            max_tokens=150
        )

        return {
            "response": response.choices[0].text.strip()
        }
