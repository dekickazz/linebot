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
# ======================================================================================================================
app = Flask(__name__)

channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

if not channel_access_token or not channel_secret:
    print("กรุณาตั้งค่า Environment Variables: LINE_CHANNEL_ACCESS_TOKEN และ LINE_CHANNEL_SECRET บน Render.com")
    exit()

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ======================================================================================================================
# ส่วนของการสร้าง Webhook Endpoint
# ======================================================================================================================
@app.route("/callback", methods=['POST'])
def callback():
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
# ส่วนของการจัดการ Event ที่ได้รับจาก LINE (***ส่วนที่แก้ไข***)
# ======================================================================================================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # แปลงข้อความที่รับมาเป็นตัวพิมพ์เล็กทั้งหมด
    user_message = event.message.text.lower()

    # ใช้โครงสร้าง if/elif/else เพื่อให้ทำงานถูกต้อง
    # และเปลี่ยนเงื่อนไขเป็นตัวพิมพ์เล็กทั้งหมด
    if user_message == 'flt ops':
        reply_message = 'เดือนนี้โดนตัดตารางหรือยัง?'
    elif user_message == 'engineer':
        reply_message = 'APU INOP NA KA'
    elif user_message == 'gs':
        reply_message = 'หวานเผ็ด'
    elif user_message == 'ramp':
        reply_message = 'แร้มป์พลังม้า'
    else:
        # กรณีไม่ตรงกับเงื่อนไขใดๆ เลย
        reply_message = 'สวัสดีครับ! กรุณาเลือกเมนูด้านล่างเพื่อดูข้อมูลที่ต้องการครับ'

    # ส่งข้อความตอบกลับ
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# ======================================================================================================================
# ส่วนของการรันแอปพลิเคชัน
# ======================================================================================================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
