# ニュースの取得
import requests
import os

def fetch_news():
    API_KEY = os.getenv('NEWS_API_KEY')
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Japan economy OR Japan technology OR Japan business", 
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 30,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    return articles

import uuid
import json

AZURE_KEY = os.getenv('AZURE_TRANSLATOR_API_KEY')
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
AZURE_LOCATION = "JapanEast"

def translate_text(texts):
    path = '/translate'
    constructed_url = AZURE_ENDPOINT + path
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['ja']
    }
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': texts}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

# ストリームリットで表示
import streamlit as st
import time

news_list = fetch_news()
start_time = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime())
index = st.session_state.get("index", 0)  # 未定義なら0を使う

st.title("🗞 ニュース翻訳＆読み上げステーション")
st.write(start_time)

# セッションステートで表示インデックスを管理
if "index" not in st.session_state:
    st.session_state.index = 0

key = st.text_input("キーボード操作（n: 次、p: 前）", "")

if key.lower() == "n" and st.session_state.index < len(news_list) - 1:
    st.session_state.index += 1
elif key.lower() == "p" and st.session_state.index > 0:
    st.session_state.index -= 1

article = news_list[st.session_state.index]
english = f"{article['title']}\n\n{article['description']}"
japanese = translate_text(english)
st.subheader(st.session_state.index + 1)
st.subheader("📰 英語原文")
st.write(english)
st.subheader("🌐 日本語訳")
st.write(japanese)    