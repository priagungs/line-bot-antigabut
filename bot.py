# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

import time

kata_kasar = [
    'ajg', 'bgst', 'kampret', 'anjing', 'bangsat', 'qntl', 'kontol', 'ngentot', 'ngentiaw', 'bct', 'bacot', 'anjir', 'jir', 'anjay'
]

app = Flask(__name__)

line_bot_api = LineBotApi('WRwK6zLY9ZJzx9ak/ymI8ez/n+rUgzJeUC+rkWGC9BVvgxaUqKtIpMYmQtYeT+9gqDoVIxeyX8x/XLYV4N194aHJyON2PXPvTFFKF8InxzgrwsnakZm/PPNy14YKKNMYdcl77pbWN/Th86ryTOh9ZQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('9fdd23dedd08e371a7a08e824cadef78') #Your Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    if(text == '!profile'):
        user_profile = line_bot_api.get_profile(event.source.user_id)
        text_message = TextSendMessage(text =
            'Nama : ' + user_profile.display_name +
            '\nStatus : ' + user_profile.status_message +
            '\nPicture : ' + user_profile.picture_url)
        line_bot_api.reply_message(event.reply_token, text_message)

    elif(text.split()[0] == '!gabut' and len(text.split() >=2)):
        text_message = TextSendMessage(
            text = 'Gabut maneh ' + text.split('!gabut ')[1]
        )
        line_bot_api.reply_message(event.reply_token, text_message)
    else:
        text = text.split()
        for word in text:
            if word in kata_kasar:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = 'ih ga boleh ngomong kasar :('))
                break

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
