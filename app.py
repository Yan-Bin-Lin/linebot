#coding=utf-8
'''
    test flask framework
    by yan-bin-lin
'''

import os
from linebot.models import TextSendMessage
from linebot import LineBotApi
from flask import Flask, request, Blueprint, url_for
from blueprint_pf.pf import PF,count_Chain
from help.helper import helper,help_all

app = Flask(__name__)
app.register_blueprint(PF, url_prefix='/pf')
app.register_blueprint(helper, url_prefix='/help')

@app.route('/')
def website_test():
    return '<p>This is a flask test</p>'

@app.route('/callback', methods=['POST'])
#first step
def callback():   
   
    #get json input
    decode = request.get_json()
    #start line_bot_api
    channel_token = "w5LR/GWzxSwwVP910AG4AOaDBv0Ys7bEW2yJM9qYdyBfHhgnh1mRJlXKLOpncI/f5iEJLb38bLWriV9AoZ72p45BODmeil/Ux7iWSbYqgcFx9E1uLwf1kCWk6luXUQUH0ZN5WxhRITHYZjx5balb0AdB04t89/1O/w1cDnyilFU="
    line_bot_api = LineBotApi(channel_token)
  
        #get reply token
    reply_token = decode['events'][0]["replyToken"]
        #get message
    text = decode['events'][0]['message']['text']
    
    if(text.upper().find("EDDY") != -1):
        line_bot_api.reply_message(reply_token, TextSendMessage(text='Eddy Green!'))
    #example message:"lb. news 1"
    tlist = text.split(' ')
    if len(tlist) >= 2:
        
        judge = tlist[0] #lb.
        method = tlist[1] #news ,control = tlis[2]       
        if judge == "lb.":
            
            if method == "help":
                if len(tlist) == 2:
                    tlist.append('')
                out_text = help_all(tlist[2])
                
            #pf method
            elif method == "pf":     
                out_text = count_Chain(tlist[2:])           
            
            else:
                out_text = u'無效指令: '.encode('utf-8') + method.encode('utf_8')
            
            line_bot_api.reply_message(reply_token, TextSendMessage(text = out_text.decode('utf-8')))           
    
    return "<p>hello world</p>"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)