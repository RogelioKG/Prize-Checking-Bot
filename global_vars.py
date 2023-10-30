# standard library
import os
import sys

# third party library
from linebot import (
    LineBotApi, WebhookHandler
)

# User Channel Access Token
line_bot_api = LineBotApi('...')

# User Channel Secret
handler = WebhookHandler('...')

# 統一發票開獎 RSS XML
URL = "https://invoice.etax.nat.gov.tw/invoice.xml"

# 父目錄
try:
    PATH = os.environ['LAMBDA_TASK_ROOT'] + "/"
except KeyError:
    PATH = sys.path[0] + "\\"
