from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            ImageSendMessage, AudioMessage)
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
    print(
        "Invalid signature. Please check your channel access token/channel secret."
    )
    abort(400)
  return 'OK'


# Text message events
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
  print("enter txt msg event handler")

  user_id = event.source.user_id
  text = event.message.text.strip()
  # print("------" + event.reply_token + "------")
  # print("------" + text + "------")
  try:
    msg = TextSendMessage(text=event.message.text)
  except Exception as e:
    msg = TextSendMessage(text=str(e))
  try:
    line_bot_api.reply_message(event.reply_token, msg)
  except Exception as e:
    print("error" + str(e))


# Text message events
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
  user_id = event.source.user_id

  msg_content = line_bot_api.get_message_content(event.message.id)
  # audio_data = b''
  # for chunk in msg_content.iter_content():
  #   audio_data += chunk
  # print("--------" + str(audio_data) + "----------")
  # bucket_name = "testing_bucket"
  # upload_blob_from_memory(bucket_name, audio_data, f'{user_id}.mp3')

  # file_name = user_id+'.mp3'
  path='/Users/daphne/desktop'
  with open('OutputFile.mp3', 'wb') as fd:
      for chunk in msg_content.iter_content():
          fd.write(chunk)
        
  #reply message
  msg = "Audio message successfully received!"
  try:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
  except Exception as e:
    print("error" + str(e))


@app.route("/", methods=['GET'])
def home():
  return "hi"


if __name__ == "__main__":
  # app.run()
  app.run(host='0.0.0.0', port=80)
