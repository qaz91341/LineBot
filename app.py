#載入LineBot所需要的模組
from flask import Flask, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('ZN8JgdTk20zbNP0KPdRWYM2CPdxEkCmZZQQy5nhGgC1XWyOHKfVK9Rr3ryksfhMhRKv8PYeUsL6LlsFZHEdwOPt3mDiCSw8kBeUJdxkIzn4o7xpm3ttMqH3IMU++qDnsSkzZoN3fRep1XcduexKw0gdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('531e4f66f61dd1967850544943768a1e')

#push成功後會傳送message給此ID的帳號
line_bot_api.push_message('Ued071ac7750a89300583606813ec35eb', TextSendMessage(text='準備完成'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
import re
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    reply_arr = []
    if re.match("你是誰", message):
        #回覆特定字
        sticker_message = StickerSendMessage(
            package_id='446',
            sticker_id='1990'
        )
        reply_arr.append(sticker_message)
        reply_arr.append(TextSendMessage("偷尼史塔克"))
        line_bot_api.reply_message(event.reply_token,TextSendMessage("偷尼史塔克"))
    elif re.match("你要去哪裡",message):
        #回覆位置
        location_message = LocationSendMessage(
            title= "天安門",
            address= "北京市东城区 邮政编码: 100051",
            latitude= 39.908874242716614,
            longitude= 116.39746996721439
        )
        reply_arr.append(location_message)
        reply_arr.append(TextSendMessage("去擋坦克"))
        line_bot_api.reply_message(event.reply_token,reply_arr)
    elif re.match('我誰',message):
        #回覆圖片
        image_message = ImageSendMessage(
        original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
        preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
        )
        reply_arr.append(image_message)
        reply_arr.append(TextSendMessage("我誰~"))
        line_bot_api.reply_message(event.reply_token, reply_arr)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("沒對到我的特定字 我只能跟著你回覆 ㄏㄏ \n" + message))
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token,message)

#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)