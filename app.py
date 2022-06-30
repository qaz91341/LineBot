#載入LineBot所需要的模組
from flask import Flask, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from bs4 import BeautifulSoup as bs
import requests
import logging #用來留log
logging.basicConfig(level=logging.INFO)

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
        reply_arr = reply_name()
        line_bot_api.reply_message(event.reply_token,reply_arr)
    elif re.match("你要去哪裡",message):
        #回覆位置
        reply_arr = reply_place()
        line_bot_api.reply_message(event.reply_token,reply_arr)
    elif re.match("我誰",message):
        #回覆圖片
        reply_arr = reply_who()
        line_bot_api.reply_message(event.reply_token, reply_arr)
    elif re.match("ptt",message):
        #回覆圖片
        reply_arr = climb_ptt()
        line_bot_api.reply_message(event.reply_token, reply_arr)
        
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("沒對到我的特定字 我只能跟著你回覆 ㄏㄏ \n" + message))
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token,message)

def reply_name():
    reply_arr =[]
    sticker_message = StickerSendMessage(
            package_id='446',
            sticker_id='1990'
        )
    reply_arr.append(sticker_message)
    reply_arr.append(TextSendMessage("偷尼史塔克"))
    return reply_arr

def reply_place():
    reply_arr =[]
    location_message = LocationSendMessage(
        title= "天安門",
        address= "北京市东城区 邮政编码: 100051",
        latitude= 39.908874242716614,
        longitude= 116.39746996721439
    )
    reply_arr.append(location_message)
    reply_arr.append(TextSendMessage("去擋坦克"))
    return reply_arr

def reply_who():
    reply_arr =[]
    image_message = ImageSendMessage(
    original_content_url='https://i.imgur.com/j6Q0QuXl.jpg',
    preview_image_url='https://i.imgur.com/j6Q0QuXl.jpgg'
    )
    reply_arr.append(image_message)
    reply_arr.append(TextSendMessage("努股誰永?"))
    return reply_arr

def climb_ptt():
    ###發request 取得原始碼
    url = "https://www.ptt.cc/bbs/Stock/index.html"
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
    }

    res = requests.get(url, headers = headers)
    #print(res.text)
    soup = bs(res.text,features="xml")
    data = soup.select("div.r-ent")

    reply_arr = []
    reply_arr.append(TextSendMessage("------------------------------------------------------------\n"+"標題 :[新聞] 瑞士科學期刊刊登高端疫苗「保護力84%」\n" +"連結: https://www.ptt.cc/bbs/Stock/M.1656595430.A.053.html \n " +"時間 :6/30 \n " +"推文數量 :47 \n" ))
    reply_arr.append(TextSendMessage("121312333333333333333333333333333333333333333"))
    reply_message = ""
    i = 0
    for sample in data :
        
        title = sample.select("div.title")[0].text.strip()
        if "刪除" in title: 
            continue
        i = i+1
        # if i%5==0 or i == len(data):
        #     if len(reply_arr) < 5:
        #         reply_arr.append(TextSendMessage(reply_message))
        #         reply_message = str()

        if i == 3:
            break


        
        reply_message += "-" * 60 
        reply_message += "標題 :" + title 

        #連結
        raw_link = sample.select("div.title a")[0]["href"]
        domain_name = "https://www.ptt.cc"
        link = domain_name + raw_link
        reply_message += "連結: " + link 
        

        
        if "公告" in title or "閒聊" in title: 
            continue
        #時間
        date = sample.select("div.date")[0].text.strip()
        reply_message += "時間 :" + date 

        #推文數量
        if len(sample.select("span.hl")) == 0 :
            continue
        push_num = sample.select("span.hl")[0].text
        
        reply_message += "推文數量 :" + push_num

    # reply_arr.append(TextSendMessage(reply_message))

    return reply_arr


#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
