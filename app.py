from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('ZJwBYdB/zL8W3WyJoBEc9IWuHfjhG2cUlz/Rs+bs0FWDtcK6bVCJe6feoAB8bAsop8djREi/8B8RUbf9rn7nvHoPW5C7dL1W3MxDHCICICoPbgT8hIYwKErx0XIDlGoiqwhouhUPYkVOjCDFk7iqAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0df3aab4979a1ee97c4e2dd888aaf40e')

app = Flask(__name__)

# username of anto.io account
user = 'ding'
# key of permission, generated on control panel anto.io
key = 'XjSstPYUztfnFLDaOeVj20i1hAJXJBv2wTIRXDcu'
# your default thing.
thing = 'LED_CONTROL'

anto = antolib.Anto(user, key, thing)


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
def handle_message(event):
    message = event.message.text.split(" ")
    channel = message[0]
    status = message[1]
    anto.pub(channel, 1 if status=='on' else 0)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Turn {} {}".format(status, channel)))

if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
