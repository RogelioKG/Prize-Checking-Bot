# standard library
from typing import Any
import json

# third party library
from flask import Flask, request

# local library
from services.prizes import PrizeInfo
from services.flex import *
from globals.linebot_modules import invo, multi_invo
from globals.variables import line_bot_api, handler


app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback() -> dict[str, Any]:
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            "statusCode": 502,
            "body": json.dumps(
                "Invalid signature. Please check your channel access token/channel secret."
            ),
        }
    return {
        "statusCode": 200,
        "body": json.dumps("Success."),
    }


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    msg: str = event.message.text
    reply_messages = []
    
    if msg == "@輸入發票最後三碼":
        reply_messages.append(TextSendMessage(text="請輸入發票最後三碼進行對獎！"))
    
    elif msg == "@前期中獎號碼":
        prizeinfos = [PrizeInfo.fetch_num(1), PrizeInfo.fetch_num(2)]
        reply_messages.append(FlexSendMessage(alt_text=prizeinfos[0].format(), contents=multi_invo(prizeinfos)))

    elif msg == "@本期中獎號碼":
        prizeinfo = PrizeInfo.fetch_num(0)
        reply_messages.append(FlexSendMessage(alt_text=prizeinfo.format(), contents=invo(prizeinfo)))

    elif len(msg) == 3 and msg.isdigit():
        prizeinfo = PrizeInfo.fetch_num(0)
        win, reply_text = prizeinfo.check_invoice(msg)
        if win:
            # 若有贏得獎項，同時將中獎號碼 bubble 也一併傳出
            reply_messages.append(FlexSendMessage(alt_text=prizeinfo.format(), contents=invo(prizeinfo)))
        reply_messages.append(TextSendMessage(text=reply_text))
    else:
        reply_messages.append(TextSendMessage(text="嗯？你可以再說一次嗎？"))

    line_bot_api.reply_message(event.reply_token, reply_messages)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
