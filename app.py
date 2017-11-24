'''
    test flask framework
    by yan-bin-lin
'''
from flask import Flask
import json
from flask import request
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

@app.route('/')
def website_test():
    return '<p>This is a flask test</p>'

@app.route('/callback', methods=['POST'])
def callback():
    decode = request.get_json()
    channel_token = "w5LR/GWzxSwwVP910AG4AOaDBv0Ys7bEW2yJM9qYdyBfHhgnh1mRJlXKLOpncI/f5iEJLb38bLWriV9AoZ72p45BODmeil/Ux7iWSbYqgcFx9E1uLwf1kCWk6luXUQUH0ZN5WxhRITHYZjx5balb0AdB04t89/1O/w1cDnyilFU="
    reply_token = decode['events'][0]["replyToken"]
    print(reply_token)
    line_bot_api = LineBotApi(channel_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text='Eddy Green !'))
    return "<p>hello world</p>"
    
'''    
    file = request.get_json()
    decode = json.load(file)
    line_type = decode['events'][0]['type']
    text = decode['events'][0]['message']['text']
    judge = text[0:8]
    strlen = len(text)
    if judge == "linebot:":
        control = text[9:strlen]
        return "<p>" + control + "</p>"
    return ""
'''



if __name__ == '__main__':
    app.run(debug = True)