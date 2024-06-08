import base64
import hashlib
import hmac
import html
import time

import gradio as gr
import requests

key = "aVwDprJBYvnz1NBs8W7GBuaHQDeoynolGF5IdsxyYP6lyCzxAOG38hleJo43NnB6"

params = {
    "activate": True,
    "language string": "ja",
}

language_codes = {
    # Auto': 'auto',
    'Korean': 'ko',
    'English': 'en',
    'Japanese': 'ja',
    'Chinese Simplified': 'zh-CN',
    'Chinese Traditional': 'zh-TW',
    'Vietnamese': 'vi',
    'Thai': 'th',
    'Indonesian': 'id',
    'French': 'fr',
    'Spanish': 'es',
    'Russian': 'ru',
    'German': 'de',
    'Italian': 'it'
}


def generate_hmac():
    ts = int(time.time() * 1000)
    url = 'https://apis.naver.com/papago/papago_app/n2mt/translate'
    url = url[:255]

    h = hmac.new(key.encode(), digestmod=hashlib.sha1)
    h.update(url.encode())
    h.update(str(ts).encode())

    return {
        'msgpad': ts,
        'md': base64.b64encode(h.digest()).decode()
    }


def translate(string, source, target):
    response = requests.post(
        'https://apis.naver.com/papago/papago_app/n2mt/translate',
        params=generate_hmac(),
        data={
            'source': source,
            'target': target,
            'text': string
        },
        headers={
            "User-Agent": "okhttp/4.9.1"
        }
    )

    return response.json()['message']['result']['translatedText']


def input_modifier(string):
    if not params['activate']:
        return string

    return translate(string, params['language string'], 'en')


def output_modifier(string):
    if not params['activate']:
        return string

    translated_str = translate(html.unescape(string), 'en', params['language string'])
    return html.escape(translated_str)


def bot_prefix_modifier(string):
    return string


def ui():
    language_name = list(language_codes.keys())[list(language_codes.values()).index(params['language string'])]

    with gr.Accordion("Papago Translate", open=True):
        with gr.Row():
            activate = gr.Checkbox(value=params['activate'], label='Activate translation')
            language = gr.Dropdown(value=language_name, choices=[k for k in language_codes], label='Language')

    activate.change(lambda x: params.update({"activate": x}), activate, None)
    language.change(lambda x: params.update({"language string": language_codes[x]}), language, None)
