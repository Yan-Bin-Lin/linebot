#coding=utf-8
'''
Created on 2017/12/10/
@author: danny
mission data
'''

import requests
import re
from bs4 import BeautifulSoup
#from flask import Blueprint

#ms = Blueprint('mission',__name__) #regisster

#@mission.route('/')
def mission(inlist):
    
    if len(inlist) == 2:
        inlist.append('')
    
    if len(inlist) == 3:
        
        #牌位  #挑戰
        if inlist[0] == 'rk' or inlist[0] == 'clg':
            out = show_race(inlist[0],inlist[1],inlist[2]).encode('utf-8')
                     
        #降臨  #轉生
        elif inlist[0] == 'jl' or inlist[0] == 'js':
            out = show_jls(inlist[0],inlist[1],inlist[2]).encode('utf-8')
                    
        else:
            out = '指令ms, 查無參數: '.encode('utf-8') + inlist[0].encode('utf-8')
        
        if len(out) >= 2000:
            out = '指令ms, 資料字數過多,不要在搜尋用字串後面加任何字'.encode('utf-8')
    
        elif len(out) == 0:
            out = '指令ms, 查無資料'.encode('utf-8')
            
        return out 
    
    else:
        return '指令ms, 錯誤格式'.encode('utf-8')

def show_race(race,key,detai):
    
    #rk
    if race == 'rk':
        url = "https://shoumetsu.gamerch.com/%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88" 
        start = 1
        
    #clg
    else:
        url = 'https://shoumetsu.gamerch.com/%E3%83%81%E3%83%A3%E3%83%AC%E3%83%B3%E3%82%B8%E3%83%A3%E3%83%BC'
        start = 0
        
    #filter
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')  
    filt = soup.find('section', id = 'js_async_main_column_text')    
    soup = BeautifulSoup(str(filt), 'html.parser')
    filt = soup.find_all('a', title = re.compile('\D'))       
    
    end = len(filt)
    out = ''
    result = [['1','2']]
    #find assigned data
    if key == '':
        #show all
        for i in range(start,end):
            out_text = filt[i].get('title')
            out += out_text[out_text.find('】') + 1:out_text.find('-') - 1] + '\n\n'
    else:
        #show seaarch
        #max: 5
        max = 0
        for i in range(start,end):
            if (filt[i].get('title')).find(key) != -1:
                text_title = filt[i].get('title')
                text_title = text_title[text_title.find('】') + 1:text_title.find('-') - 1]
                text_href = filt[i].get('href')
                inside = [text_title, text_href]
                result.append(inside)
                out += text_title + '\n' + text_href + '\n\n'
                max += 1
                if(max >= 5):
                    break  
                
        if len(result) == 2:
            out += show_data(result[1][1],detai)     
            
        
    print(out)
    return out

def show_jls(jls,key,detail):
    
    #jl
    if jls == 'jl':
        start = 6
        end = 15
    
    #js
    else:
        start = 15
        end = 18
    
    #filter 
    url = "https://shoumetsu.gamerch.com/"           
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    filt = list()
    ms_id = 'js_oc_box_m'
    for i in range(start,end):
        tmp = soup.find_all('div',id = ms_id + str(i))
        filt += tmp
    
    soup =  BeautifulSoup(str(filt),'html.parser')
    filt = soup.find_all('a')
    out = ''
    if key == '':
        for text in filt:
            text_title = text.get_text()
            out += text_title[0:text_title.find('(')] + '\n\n'
    
    else:
        count = 0
        result = [['1','2']]   
        for text in filt:
            text_title = text.get_text()
            if text_title.find(key) != -1:
                text_href = text.get('href')
                inside = [text_title, text_href]
                result.append(inside)
                out += text_title[0:text_title.find('(')] + '\n' + text_href + '\n\n'
                count += 1
                if(count >= 5):
                    break
            
        if len(result) == 2:
            out += show_data(result[1][1],detail)
    
    print(out)
    return out        

def show_data(url,detail):
    
    html = requests.get(url).text   
    soup = BeautifulSoup(html,"html5lib")
    #filter
    filt = soup.find_all('div',id = 'js_oc_box_0')
    soup =  BeautifulSoup(str(filt),'html.parser')
    filt = soup.find_all('tr')    
    
    out_text = ''
    #pint out
    for data in filt:
        #  print()
        line = BeautifulSoup(str(data),'html.parser')
        text = line.find_all('td')
        out = ''
        if len(text) == 4:
            if detail == '':
                continue
            if (text[0].get_text())[0] == 'N':
                continue
            if text[1].get_text() == '':
                out = 'NO.{:<3}{}\n'.format(text[0].get_text(),text[2].get_text())
            else:
                out = 'No.{:<3}CD:{:<3}\nATK:{}\n'.format(text[0].get_text(),text[1].get_text(),text[3].get_text())
        else:
            for x in text:
                out = out + x.get_text() + ' '
            if out[0] == 'H':
                out += '\n----------\n'
            elif out[0] == 'B':
                out = '----------\n' + out
            else:
                if detail == '':
                    continue
        out_text += out + '\n'
    return out_text
