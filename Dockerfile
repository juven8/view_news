# ベースイメージ：Pythonを含んだ軽量な環境
FROM python:3.10-slim

# FFmpegのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# Streamlitの起動
CMD ["streamlit", "run", "view_news.py"]