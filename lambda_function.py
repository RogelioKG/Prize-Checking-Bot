# third party library
from flask import Flask, request, abort

# local library
from linebot_modules import *
from prizes import *
from flex import *
from global_vars import line_bot_api, handler


app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    msg: str = event.message.text
    reply_messages = []
    
    if msg == "@輸入發票最後三碼":
        reply_messages.append(TextSendMessage(text="請輸入發票最後三碼進行對獎！"))
    
    elif msg == "@前期中獎號碼":
        # reply_messages.append(TextSendMessage(text=mono_num(1)+"\n\n"+mono_num(2)))
        prizeinfos = [mono_num(1), mono_num(2)]
        reply_messages.append(FlexSendMessage(alt_text=formatted(prizeinfos[0]), contents=multi_invo(prizeinfos)))

    elif msg == "@本期中獎號碼":
        # reply_messages.append(TextSendMessage(text=mono_num(0)))
        prizeinfo = mono_num(0)
        reply_messages.append(FlexSendMessage(alt_text=formatted(prizeinfo), contents=invo(prizeinfo)))

    elif len(msg) == 3 and msg.isdigit():
        prizeinfo = mono_num(0)
        win, reply_text = last_three_digit(msg, prizeinfo)
        if win:
            reply_messages.append(FlexSendMessage(alt_text=formatted(prizeinfo), contents=invo(prizeinfo)))
        reply_messages.append(TextSendMessage(text=reply_text))

    line_bot_api.reply_message(event.reply_token, reply_messages)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
