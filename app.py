'''
    test flask framework
    by yan-bin-lin
'''

from flask import Flask
import os
from flask import request
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

@app.route('/')
def website_test():
    return '<p>This is a flask test</p>'

@app.route('/callback', methods=['POST'])
#first step
def callback():
    #get json input
    decode = request.get_json()
    
    if decode['events'][0]['type'] == "message":
        #start line_bot_api
        channel_token = "w5LR/GWzxSwwVP910AG4AOaDBv0Ys7bEW2yJM9qYdyBfHhgnh1mRJlXKLOpncI/f5iEJLb38bLWriV9AoZ72p45BODmeil/Ux7iWSbYqgcFx9E1uLwf1kCWk6luXUQUH0ZN5WxhRITHYZjx5balb0AdB04t89/1O/w1cDnyilFU="
        line_bot_api = LineBotApi(channel_token)
        #get reply token
        reply_token = decode['events'][0]["replyToken"]
        #get message
        text = decode['events'][0]['message']['text']
        #example message:"lb. news 1"
        tlist = text.split(' ')
        if len(tlist) >= 2:
            judge = tlist[0] #lb.
            method = tlist[1] #news
            if len(tlist) == 3:
                control = tlist[2] #1        
                if judge == "lb.":
                    if method == "eddy":
                        line_bot_api.reply_message(reply_token, TextSendMessage(text='Eddy Green!'))
                    else:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text = 'Invalid instruction: ' + method ))           
    return "<p>hello world</p>"



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)