import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

load_dotenv()

CHANNEL_ACCESS_TOKEN=os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET=os.environ["CHANNEL_SECRET"]

OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
openai.api_key=OPENAI_API_KEY

assistant_setting = [
            {"role": "system", "content": "you're 20, UChicago student, and user's friend. you reply short sentences include abbreviation like OMG and lol, don't use difficult words. Because user's an uni student in Japan and not good as English."}
            ]
messages_log=[]

def management_message_log_length(message_log):
    message_log_conversation_length=len(message_log)-1
    if(message_log_conversation_length>10):
        messages_log.pop(0)
    else:
        None

def response_message_by_chatGPT(user_message):
    messages_log.append({"role": "user", "content": user_message})
    management_message_log_length(messages_log)
    # API呼び出し
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=assistant_setting+messages_log
        )
    except (openai.error.RateLimitError, openai.error.InvalidRequestError) as error:
        return {"type":"error","message":error.user_message}

    # 応答の取得 / 表示 / messagesへの追加
    response_message = completion["choices"][0]["message"]["content"]
    print("OpenAIの応答です： " + response_message)
    messages_log.append({"role": "assistant", "content": response_message})
    management_message_log_length(messages_log)
    token=completion["usage"]["completion_tokens"]
    return {"type":"response","message":response_message,"token":token}

    # token数の取得と表示
    #tokens = completion["usage"]["total_tokens"]
    #print("今回のToken数： " + str(tokens))

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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
    response_data=response_message_by_chatGPT(event.message.text)
    if(response_data["type"]=="response"):
        if(response_data["token"]>20):
            message_split=response_data["message"].split("!")
            for i in range(len(message_split)-1):
                    message_split[i]+="!"
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=message) for message in message_split])
        else:    
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response_data["message"]))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextMessage("Sorry, I can't reply now."),TextSendMessage("error:"+response_data["message"])])


if __name__ == "__main__":
    app.run(debug=True)
