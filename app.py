# -*- coding: utf-8 -*-

# ======================================================================================================================
# ส่วนของการ import Library ที่จำเป็น
# ======================================================================================================================
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ======================================================================================================================
# ส่วนของการตั้งค่า Config และเชื่อมต่อกับ LINE API
# โค้ดส่วนนี้ทั้งหมดต้องอยู่ชิดขอบซ้ายสุด (ไม่มีการย่อหน้า)
# ======================================================================================================================
app = Flask(__name__)

# ดึงข้อมูล Access Token และ Channel Secret จาก Environment Variables
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

# ตรวจสอบว่าได้ตั้งค่า Environment Variables ครบถ้วนหรือไม่
if not channel_access_token or not channel_secret:
    print("กรุณาตั้งค่า Environment Variables: LINE_CHANNEL_ACCESS_TOKEN และ LINE_CHANNEL_SECRET บน Render.com")
    exit()

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ======================================================================================================================
# ส่วนของการสร้าง Webhook Endpoint
# โค้ดส่วนนี้ทั้งหมดต้องอยู่ชิดขอบซ้ายสุด (ไม่มีการย่อหน้า)
# ======================================================================================================================
@app.route("/callback", methods=['POST'])
def callback():
    # โค้ดที่อยู่ข้างในฟังก์ชันนี้ ต้องย่อหน้าเข้าไป 1 ระดับ (4 spaces)
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel secret/access token.")
        abort(400)

    return 'OK'

# ======================================================================================================================
# ส่วนของการจัดการ Event ที่ได้รับจาก LINE
# โค้ดส่วนนี้ทั้งหมดต้องอยู่ชิดขอบซ้ายสุด (ไม่มีการย่อหน้า)
# ======================================================================================================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # โค้ดที่อยู่ข้างในฟังก์ชันนี้ ต้องย่อหน้าเข้าไป 1 ระดับ (4 spaces)
    user_message = event.message.text.lower()

    if user_message == 'promotion':
        reply_message = 'นี่คือโปรโมชั่นสุดพิเศษประจำเดือนนี้ครับ!'
    elif user_message == 'products':
        reply_message = 'สินค้าของเรามีดังนี้ครับ...\n1. สินค้า A\n2. สินค้า B\n3. สินค้า C'
    else:
        reply_message = 'สวัสดีครับ! กรุณาเลือกเมนูด้านล่างเพื่อดูข้อมูลที่ต้องการครับ'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# ======================================================================================================================
# ส่วนของการรันแอปพลิเคชัน
# โค้ดส่วนนี้ทั้งหมดต้องอยู่ชิดขอบซ้ายสุด (ไม่มีการย่อหน้า)
# ======================================================================================================================
if __name__ == "__main__":
    # การดึง Port มาจาก Environment Variable ของ Render
    # หรือใช้ Port 5000 หากเป็นการรันในเครื่องตัวเอง
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
