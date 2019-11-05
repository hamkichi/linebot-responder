# -*- coding: utf-8 -*-
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
import responder

from argparse import ArgumentParser

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

api = responder.API(debug=True)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@api.route("/")
def nopage(req, resp):
    resp.text = "This is not a webpage you are looking for."
    resp.status_code = api.status_codes.HTTP_404


@api.route("/healthz")
def healthcheck(req, resp):
    resp.text = "OK"


@api.route("/callback")
async def callback(req, resp):
    if req.method == "post":
        signature = req.headers['X-Line-Signature']

        # get request body as text
        body = await req.text
        print("Request body: " + body)
        sys.stdout.flush()

        # parse webhook body
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            resp.status_code = api.status_codes.HTTP_503
            return

        # if event is MessageEvent and message is TextMessage, then echo text
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
        resp.text = "OK"

    else:
        resp.text = "404: This is not a webpage you are looking for."
        resp.status_code = api.status_codes.HTTP_404


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    options = arg_parser.parse_args()
    port = int(os.environ.get('PORT', 5000))
    api.run(address='0.0.0.0', port=port, debug=True)

