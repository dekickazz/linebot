# -*- coding: utf-8 -*-

# ======================================================================================================================
# ส่วนของการ import Library ที่จำเป็น
# ***ส่วนที่เพิ่มเข้ามา***: เราต้อง import เครื่องมือสำหรับสร้าง Flex Message
# ======================================================================================================================
import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, BubbleContainer, BoxComponent,
    TextComponent, ButtonComponent, SeparatorComponent,
    URIAction, MessageAction
)

# ======================================================================================================================
# ส่วนของการตั้งค่า Config และเชื่อมต่อกับ LINE API (เหมือนเดิม)
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
# ส่วนของการสร้าง Webhook Endpoint (เหมือนเดิม)
# ======================================================================================================================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ======================================================================================================================
# ส่วนของการจัดการ Event ที่ได้รับจาก LINE (***ส่วนที่แก้ไขหลัก***)
# ======================================================================================================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    # --- ตอบกลับด้วย Flex Message เมื่อกด FLT OPS ---
    if user_message == 'flt ops':
        # นี่คือ JSON ของเมนูย่อย FLT OPS ที่เราออกแบบไว้
        flex_message_json = {
          "type": "bubble",
          "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "FLT OPS Menu", "weight": "bold", "size": "xl" } ] },
          "body": {
            "type": "box", "layout": "vertical", "spacing": "md",
            "contents": [
              { "type": "button", "style": "primary", "action": { "type": "message", "label": "FCOM", "text": "show_fcom_menu" } },
              { "type": "button", "style": "primary", "action": { "type": "message", "label": "FCTM", "text": "show_fctm_info" } }
            ]
          }
        }
        # สร้าง FlexSendMessage จาก JSON
        flex_message = FlexSendMessage(
            alt_text='เมนู FLT OPS',
            contents=flex_message_json
        )
        # ส่งข้อความตอบกลับ
        line_bot_api.reply_message(event.reply_token, flex_message)
        return

    # --- ตอบกลับด้วย Flex Message เมื่อกด FCOM ---
    elif user_message == 'show_fcom_menu':
        flex_message_json = {
          "type": "bubble",
          "header": { "type": "box", "layout": "vertical", "contents": [ { "type": "text", "text": "FCOM Links", "weight": "bold", "size": "xl" } ] },
          "body": {
            "type": "box", "layout": "vertical", "spacing": "md",
            "contents": [
              { "type": "button", "style": "secondary", "action": { "type": "message", "label": "Link 1", "text": "get_fcom_link_1" } },
              { "type": "button", "style": "secondary", "action": { "type": "message", "label": "Link 2", "text": "get_fcom_link_2" } },
              { "type": "button", "style": "secondary", "action": { "type": "message", "label": "Link 3", "text": "get_fcom_link_3" } }
            ]
          },
          "footer": {
            "type": "box", "layout": "vertical",
            "contents": [ { "type": "button", "style": "link", "height": "sm", "action": { "type": "message", "label": "Back to FLT OPS", "text": "flt ops" } } ]
          }
        }
        flex_message = FlexSendMessage(alt_text='เมนู FCOM', contents=flex_message_json)
        line_bot_api.reply_message(event.reply_token, flex_message)
        return

    # --- ตรรกะการตอบข้อความธรรมดา ---
    reply_message = ''
    
    if user_message == 'engineer':
        reply_message = 'APU INOP NA KA'
    elif user_message == 'gs':
        reply_message = 'หวานเผ็ด'
    elif user_message == 'ramp':
        reply_message = 'แร้มป์พลังม้า'
    elif user_message == 'show_fctm_info':
        reply_message = 'นี่คือข้อมูลของ FCTM ครับ...'
    elif user_message == 'get_fcom_link_1':
        reply_message = 'นี่คือลิงก์สำหรับหัวข้อที่ 1:\nhttps://example.com/fcom/1'
    elif user_message == 'get_fcom_link_2':
        reply_message = 'นี่คือลิงก์สำหรับหัวข้อที่ 2:\nhttps://example.com/fcom/2'
    elif user_message == 'get_fcom_link_3':
        reply_message = 'นี่คือลิงก์สำหรับหัวข้อที่ 3:\nhttps://example.com/fcom/3'
    else:
        # ถ้าไม่มีอะไรตรงเลย ให้ตอบกลับเป็นข้อความเริ่มต้น
        reply_message = 'สวัสดีครับ! กรุณาเลือกเมนูเพื่อดูข้อมูลที่ต้องการครับ'

    # ส่งข้อความตอบกลับ (ถ้ามี)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# ======================================================================================================================
# ส่วนของการรันแอปพลิเคชัน (เหมือนเดิม)
# ======================================================================================================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

