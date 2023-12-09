from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, AudioMessage)
import os
import openai
from openai import OpenAI
import mfcc_obj
import NLP_obj
from datetime import datetime, timezone, timedelta
from pydub import AudioSegment
import sys
import wave
import requests
import subprocess
from dotenv import load_dotenv

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
    try:
        msg = TextSendMessage(text=event.message.text)
    except Exception as e:
        msg = TextSendMessage(text=str(e))
    try:
        line_bot_api.reply_message(event.reply_token, msg)
    except Exception as e:
        print("error" + str(e))


# Audio message events
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):

    user_id = event.source.user_id
    msg_content = line_bot_api.get_message_content(event.message.id)

    #reply message
    msg = "Audio message successfully received!"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    CurrTime = dt2.strftime("%Y-%m-%d_%H:%M:%S")  # 將時間轉換為 string

    #create m4a file
    file_name = CurrTime + '.m4a'

    with open(file_name, 'wb') as fd:
        for chunk in msg_content.iter_content():
            fd.write(chunk)

    try:
        openai.api_key = os.environ['OPENAI_API_KEY']

    except KeyError:
        sys.stderr.write("""
        You haven't set up your API key yet.

        If you don't have an API key yet, visit:

        https://platform.openai.com/signup

        1. Make an account or sign in
        2. Click "View API Keys" from the top right menu.
        3. Click "Create new secret key"

        Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
        """)
        exit(1)

    client = OpenAI()

    #open m4a file
    m4a_file = open(file_name, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1",
                                                  file=m4a_file,
                                                  response_format="text")
    print("successfully generate transcript!")

    path = 'output.txt'
    f = open(path, 'w')
    f.write(transcript)
    f.close()

    #implement NLP
    NLP = NLP_features(path)
    NLP.generate_features()
    print(NLP.feature_table)

    wav_filename = 'output.wav'
    sound = AudioSegment.from_file(file_name, format='m4a')
    sound.export(wav_filename, format='wav')

    #implement MFCC
    MFCC = mfcc_obj.mfcc_features(wav_filename)
    MFCC.mfcc_feature_calculation()
    MFCC.mfcc_output("testdoc")


@app.route("/", methods=['GET'])
def home():
    return "hi"


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=80)
