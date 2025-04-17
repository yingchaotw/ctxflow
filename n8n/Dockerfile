FROM n8nio/n8n

LABEL maintainer="yingchao <yingchao.tw@google.com>"

# 切換為 root 安裝套件
USER root

# 設定台灣 apk 鏡像（Alpine 套件管理用）
# 安裝需要的 node 模組與系統工具
RUN echo "https://alpine.cs.nycu.edu.tw/v3.19/main" > /etc/apk/repositories && \
    echo "https://alpine.cs.nycu.edu.tw/v3.19/community" >> /etc/apk/repositories && \
    apk update && apk add --no-cache curl nano && \
    npm install --location=global moment axios && \
    rm -rf /var/cache/apk/*

# 複製啟動腳本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && ls -l /entrypoint.sh

# 切換回 node 使用者
USER node

ENTRYPOINT ["/entrypoint.sh"]