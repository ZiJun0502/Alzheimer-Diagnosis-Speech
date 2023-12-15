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

    user_id = event.source.user_id
    text = "I can only receive audio message, please send an audio message around 30 sec"
    try:
        msg = TextSendMessage(text=text)
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
    reply_arr=[]

    msg = "Audio message successfully received! Start anylizing, please hold on..."
    reply_arr.append(msg)
    
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

    path = 'output.txt'
    f = open(path, 'w')
    f.write(transcript)
    f.close()

    #implement NLP
    NLP = NLP_features(path)
    NLP.generate_features()
    print(NLP.feature_table)

      wav_filename = 'output.wav'
      # sound = AudioSegment.from_file(m4a_file, format="m4a")
      # sound.export(wav_filename, format='wav')

      # # # fh = open("Baycrest2103.wav", "rb")
      # # file_path = wav_filename

      # # # Read and rewrite the file with soundfile
      # # data, samplerate = soundfile.read(file_path)
      # # soundfile.write(file_path, data, samplerate)

      # # # Now try to open the file with wave
      # # with wave.open(file_path) as file:
      # #     print('File opened!')
      command = f"ffmpeg -i {file_name} -ar 16000 {wav_filename}"
      subprocess.run(command, shell=True)

    #implement MFCC
    MFCC = mfcc_obj.mfcc_features(wav_filename)
    MFCC.mfcc_feature_calculation()
    MFCC.mfcc_output("testdoc")
    
    msg = "the final result is..."
    reply_arr.append(msg)
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_arr))
    


@app.route("/", methods=['GET'])
def home():
    
    user_ids = line_bot_api.get_friend_ids()
    Init_msg = "hi there! I'm AD diagnoser! Welcome to start trial with me!\n You can start with telling a strory with the picture below to start diagnosing process"
    img_URL = "https://www.google.com/url?sa=i&url=https%3A%2F%2Frebecca1812.pixnet.net%2Fblog%2Fpost%2F68894631-%255B%25E7%25B7%25B4%25E5%25AF%25AB%25E4%25BD%259C%2526%25E6%258F%2590%25E5%258D%2587%25E5%258F%25A3%25E8%25AA%25AA%255D-%25E7%259C%258B%25E5%259C%2596%25E8%25AA%25AA%25E6%2595%2585%25E4%25BA%258B3&psig=AOvVaw164L82xXG9KKTOxEU4qFaU&ust=1702483684452000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCPjPlo2kioMDFQAAAAAdAAAAABAD"
    
    for user_id in user_ids:
        line_bot_api.push_message(user_id, TextSendMessage(text=Init_msg))
        line_bot_api.push_message(user_id, ImageSendMessage(original_content_url=img_URL, preview_image_url=img_URL))
    
    return "hi"


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=80)
