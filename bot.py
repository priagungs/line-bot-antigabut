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
)

import time

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
    found = True
    if(text.split()[0] == '!profile'):
        if(len(text.split()) == 1):
            user_profile = line_bot_api.get_profile(event.source.user_id)
        else:
            if(isinstance(event.source, SourceRoom)):
                list_member = line_bot_api.get_room_member_ids(event.source.room_id)
            elif(isinstance(event.source, SourceGroup)):
                list_member = line_bot_api.get_group_member_ids(event.source.group_id)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text = 'masuk bray'
                    )
                )
                found = False

            if found:
                member_name = text.split('!profile ')
                for mem_id in list_member.member_ids:
                    if(member_name.lower() in line_bot_api.get_profile(mem_id).display_name):
                        user_profile = line_bot_api.get_profile(mem_id)
                        found = False
                        break
            if not found:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text = 'sorry, no member has name ' + member_name
                    )
                )

        if found:
            text_message = TextSendMessage(text =
                'Nama : ' + user_profile.display_name +
                '\nStatus : ' + user_profile.status_message +
                '\nPicture : ' + user_profile.picture_url)
            line_bot_api.reply_message(event.reply_token, text_message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
