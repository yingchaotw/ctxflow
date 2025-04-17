import os
import pickle
import base64
import json
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 如果修改了範圍，刪除已經存儲的 token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """使用 OAuth 2.0 驗證 Gmail API，並返回授權的服務實例"""
    creds = None
    # token.json 文件儲存使用者的訪問和刷新令牌，並在授權過程中被創建
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    
    # 如果沒有有效的憑證，則讓使用者登錄
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 儲存憑證，以便下次使用
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # 建立 Gmail API 服務實例
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')

def list_messages(service, user_id='me'):
    """列出使用者的 Gmail 郵件"""
    try:
        # 呼叫 Gmail API，取得郵件列表
        results = service.users().messages().list(userId=user_id).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No messages found.')
        else:
            print('Messages:')
            for message in messages[:5]:  # 只列出前 5 封郵件
                msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
                print(f"Message snippet: {msg['snippet']}")
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    """主要的運行邏輯"""
    service = authenticate_gmail()
    list_messages(service)

if __name__ == '__main__':
    main()
