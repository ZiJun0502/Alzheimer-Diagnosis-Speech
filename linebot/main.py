from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, AudioMessage
)

import os
import uuid

load_dotenv()
print(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
print(os.getenv('LINE_CHANNEL_SECRET'))

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# Initialize the bot
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# Text message events
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    try:
        msg = TextSendMessage(text=event.message.text)
    except Exception as e:
        msg = TextSendMessage(text=str(e))
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
  

# Audio message events
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    pass

@app.route("/", methods=['GET'])
def home():
    return "hi"


if __name__ == "__main__":
    app.run()