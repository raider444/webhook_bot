"""
This  dirty script listens websocket, receives submitted
JSON messages, formats them to  user-readable fromat and
sends them to telegram

This  script is configured  by OS environment variables:

BOT_TOKEN - Telegram bot token, received from BotFathher
PROXY_URL - proxy server URL (eg.: socks5://proxy.tg.io)
PROXY_USER - username
PROXY_PASSWORD - password
USER_LIST - comma-separated chat_id list.  (only commas,
no additional spaces allowed)
"""

import os
import logging
from flask import Flask, request, json
import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

webhookbot = Flask(__name__)

TG_TOKEN = os.environ['BOT_TOKEN']
PROXY_URL = os.environ['PROXY_URL']
PROXY_AUTH = {
    'username': os.environ['PROXY_USER'],
    'password': os.environ['PROXY_PASSWORD'],
}
USER_LIST = os.environ['RCPTS'].split(",")

def parse_webhook(msg):
    """
    This function parses webhook message (msg=string)
    """
    try:
        items = msg.get('commonLabels', None)
    except:
        return msg
    data = ''
    for item in items:
        data = data + '<b>' + item + ': </b>' + items[item] + '\n'
    return data

def send_content(msg, user_id, token=TG_TOKEN):
    """
    Send formated message to telegram
    msg (string) - Message body
    user_id (string) - chat id (internal telegram user or group chat ID)
    token (string) - Telegram bot token
    """
    proxy_params = telegram.utils.request.Request(
        proxy_url=PROXY_URL,
        urllib3_proxy_kwargs=PROXY_AUTH
    )
    bot = telegram.Bot(token=token, request=proxy_params)
    bot.sendMessage(chat_id=user_id, text=parse_webhook(msg), parse_mode='HTML')

@webhookbot.route('/webhook', methods=['POST'])
def webhook():
    """
    Receives and checs http request body.
    Returns 400 error code if request body is not a correct JSON.
    """
    if not request.is_json:
        return webhookbot.make_response((json.dumps({'result': 'bad request'}, 400)))
    data = request.json
    for user in USER_LIST:
        print(user)
        send_content(msg=data, user_id=user)
    response = webhookbot.response_class(
        response='{"result":"ok"}',
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    webhookbot.run(host='0.0.0.0', port=23456)
