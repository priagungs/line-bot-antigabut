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
import json

kata_kasar = [
    'ajg', 'bgst', 'kampret', 'anjing', 'bangsat', 'qntl', 'kontol', 'ngentot', 'ngentiaw', 'bct', 'bacot', 'anjir', 'jir', 'anjay', 'kmprt', 'tai', 'goblok', 'goblog', 'gblg', 'gblk',
    'babi', 'jancuk', 'cuk', 'tolol', 'bego', 'bodo'
]

# load data from json
with open('data.json', 'w') as fp:
    data = json.load(fp)

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

    elif(text.split()[0] == '!gabut' and len(text.split()) >=2):
        text_message = TextSendMessage(
            text = 'Gabut maneh ' + text.split('!gabut ')[1]
        )
        line_bot_api.reply_message(event.reply_token, text_message)

    elif(text.split()[0] == '!schedule'):
        if(len(text.split() >= 4)):
            deadline = text.split('!schedule')[1].split('"')[0]
            desc = text.split('!schedule')[1].split('"')[1]
            time_struct = time.strptime(deadline, " %d/%m/%Y %H:%M ")
            deadline_dict = {
                "time" : {
                    "day" : time_struct.tm_mday,
                    "month" : time_struct.tm_mon,
                    "year" : time_struct.tm_year,
                    "hour" : time_struct.tm_hour,
                    "minute" : time_struct.tm_min,
                },
                "desc" : desc
            }
            data["schedule"].append(deadline_dict)
            with open('data.json', 'w') as fp:
                json.dump(data, fp, sort_keys=True, indent=4)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = 'Schedule has been successfully added'
                )
            )

    elif(text == '!listschedule'):
        no = 1
        msg = ''
        for schd in data["schedule"]:
            day = schd["time"]["day"]
            mon = schd["time"]["month"]
            yr = schd["time"]["year"]
            hr = schd["time"]["hour"]
            mnt = schd["time"]["minute"]
            msg = msg + no + '.\n' + schd['desc'] +'\n' + 'deadline : ' + '%d/%d/%d %d:%d' %(day, mon, yr, hr, mnt) + '\n\n'
            no = no+1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = msg))
    elif(text == '!help'):
        line_bot_api.reply_message(event.reply_token, [
                TextSendMessage(
                    text = 'keywords : \n\n!profile : get your profile\n\n!gabut <insert_name_here> : blame other for their gabutness'
                ),
                TextSendMessage(
                    text = 'Any idea for future development ? contact me on 08561229561'
                )
            ]
        )

    else:
        text = text.lower().split()
        for word in text:
            if word in kata_kasar:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = 'ih ga boleh ngomong kasar :('))
                break

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(
        text = 'Do something useful dude!\nSend !help for more information\n=======\nThis bot is Created by : Priagung S'
    ))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
