import os
import json
import requests
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
flow_api_key = os.getenv("Flow_API")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.form.get('prompt')
    if not user_prompt:
        return "<article><p>请输入你的问题！</p></article>"

    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "stream": False  # 这里设置为 False，因为 HTMX 不支持处理原始流式返回
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {flow_api_key}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        ai_text = data['choices'][0]['message']['content']
        return render_template('response.html', ai_reply=ai_text)

    except requests.exceptions.RequestException as e:
        print(f"API 请求错误: {e}")
        return "<article><p>抱歉，请求失败。</p></article>"
    except (KeyError, IndexError) as e:
        print(f"解析失败: {e}")
        return "<article><p>抱歉，AI 回复解析失败。</p></article>"

if __name__ == '__main__':
    app.run(debug=True)
