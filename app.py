import os
... from flask import Flask, request, abort
... from linebot import LineBotApi, WebhookHandler
... from linebot.exceptions import InvalidSignatureError
... from linebot.models import MessageEvent, TextMessage, TextSendMessage
... 
... app = Flask(__name__)
... 
... # ดึงข้อมูล Access Token และ Channel Secret จาก Environment Variables
... # เพื่อความปลอดภัย เราจะไม่เก็บค่าเหล่านี้ไว้ในโค้ดโดยตรง
... channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
... channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
... 
... # ตรวจสอบว่าได้ตั้งค่า Environment Variables ครบถ้วนหรือไม่
... if not channel_access_token or not channel_secret:
...     print("กรุณาตั้งค่า Environment Variables: LINE_CHANNEL_ACCESS_TOKEN และ LINE_CHANNEL_SECRET")
...     exit()
... 
... line_bot_api = LineBotApi(channel_access_token)
... handler = WebhookHandler(channel_secret)
... 
... # สร้าง Endpoint สำหรับรับ Webhook จาก LINE
... @app.route("/callback", methods=['POST'])
... def callback():
...     # รับ X-Line-Signature header value
...     signature = request.headers['X-Line-Signature']
... 
...     # รับ request body เป็น text
...     body = request.get_data(as_text=True)
...     app.logger.info("Request body: " + body)
... 
...     # จัดการ webhook body
...     try:
...         handler.handle(body, signature)
...     except InvalidSignatureError:
...         abort(400)

    return 'OK'

# จัดการกับข้อความที่ได้รับ (Handle MessageEvent ที่เป็น TextMessage)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower() # แปลงข้อความเป็นตัวพิมพ์เล็กเพื่อง่ายต่อการเปรียบเทียบ

    # ตรวจสอบข้อความที่มาจาก Rich Menu หรือการพิมพ์ของผู้ใช้
    if user_message == 'promotion':
        reply_message = 'นี่คือโปรโมชั่นสุดพิเศษประจำเดือนนี้ครับ!'
    elif user_message == 'products':
        reply_message = 'สินค้าของเรามีดังนี้ครับ...\n1. สินค้า A\n2. สินค้า B\n3. สินค้า C'
    else:
        # หากไม่ตรงกับเงื่อนไขใดๆ ให้ส่งข้อความตอบกลับเริ่มต้น
        reply_message = 'สวัสดีครับ! กรุณาเลือกเมนูด้านล่างเพื่อดูข้อมูลที่ต้องการครับ'

    # ส่งข้อความตอบกลับ
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
