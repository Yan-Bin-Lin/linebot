#coding=utf-8
'''
Created on 2018�~3��22��
find card
@author: danny
'''

import requests
import re
from bs4 import BeautifulSoup

#go to the website
class webin():
    def __init__(self, url_end):
        url = "https://shoumetsu.gamerch.com/"
        self.url_end = url_end
        html = requests.get(url + url_end).text
        self.soup = BeautifulSoup(html, 'html.parser')

#return picture URL
def find_card(url_end):
    #go to card website
    target = webin(url_end)
    #picture url
    return target.soup.find('div', id = 'ui_wikidb_main_img_wrap').find('a').get('href')

#get input data
def get_data(input):
    return input[input.find('.') + 1:]

#get input head
def get_head(input):
    return input[:input.find('.')]


#id str format and find correct url 
def search_id(nostr):
    global url_end
    #find id
    no = get_data(nostr)
    #id format
    id = '{:0>3d}'.format(int(no))
    #find url
    digit = int(no) % 50
    no = int(int(no) / 50)
    if digit == 0: no -= 1
    print('no = ' + str(no))
    url_end = '{:0>3d}'.format(int(no * 50) + 1) + '-' 
    return id

#find by id
def find_id(id_str):
    global url_end
    #search id
    search = search_id(id_str)
    print('search = ' + str(search))
    print(url_end)
    #go to the website   
    card = webin(url_end)
    #find the card
    all = card.soup.find_all('table', width="800")
    card.soup = BeautifulSoup(str(all), 'html.parser')
    all = card.soup.find_all('tr')
    for list in all:
        line = BeautifulSoup(str(list), 'html.parser')
        number = line.find('td')
        number = BeautifulSoup(str(number), 'html.parser') 
        #the correct card
        if number.get_text() == search:
            url_end = line.find('a').get('href')
            return find_card(url_end)
            break       
    #data not found
    return '查無資料'


#dict for chinese input chage to japanese 
order = {'r' : 0, 'e' : 1, 't' : 2}
attritube = {
    'r' : {'1' : '1', '2' : '2', '3' : '3', '4' : '4', '5' : '5', '6' : '6'},
    'e' : {'火' : '火', '水' : '水', '木' : '木', '光' : '光', '暗' : '闇'},
    't' : {'超越' :'超越', '神秘' :'アングラ', '藝術' : 'アート', '平衡' : 'バランス', '體力' : '体力', '治癒' : '癒し'}
            }

#return the url of first step website
def attrubute_first(first):
    #get input tag
    head = get_head(first)
    #get input data
    search = get_data(first)
    #check if the input is correct format
    try:
        #change chinese tj japanese
        search = attritube[head][search]
    #wrong format
    except:
        return ''
    #the first website
    first = webin(url_end = '')
    #get the attribute box
    id = 'js_oc_box_m' + str(order[head] + 2)
    all = first.soup.find('div',id = id).find_all('a')
    for list in all:
        text = list.get_text()
        #get the first shilter to the website
        if text.find(search) != -1:
            url_end = list.get('href')
            url_end = url_end[30:]
            break    
    return url_end

#find the cards by another attrubute
def attrubute_second(url_end, instruct):
    #organize instruxt
    search = []
    ins = [1,2]
    for i in range(len(instruct)):
        ins[0] = get_head(instruct[i])
        ins[1] = get_data(instruct[i])
        search.append(ins.copy())
    #go to the website
    web = webin(url_end)    
    #the card table
    all = web.soup.find_all('table', id = re.compile('ui_wikidb_table_'))
    out_str = []
    for list in all:
        #table raw
        table = list.find_all('tr')
        for data in table:
            #table line
            detail = data.find_all('td')
            #no card data, continue
            if len(detail) == 0:
                continue
            #find if the card data coincide the input attribute
            card = True
            for i in range(len(search)):
                key = search[i][0]
                value = attritube[key][search[i][1]]
                #card data don't coincide the input attribute
                if detail[order[key] + 3].get_text().find(value) == -1:
                    card = False
                    break
            #if card data coincide the input attribute, get this card data
            if card != False:    
                txt = detail[0].get_text() + ' '
                for i in range(2, len(detail)):
                    txt = txt + detail[i].get_text() + ' ' 
                out_str.append(txt + '\n')
         
    #return card data
    out = ''
    for txt in out_str:
        out = out + txt
    #max size string of line_bot is 2000 character 
    return out[:1995]    
        
#find card by card attrubute        
def find_attrubute(instruct):
    #get the first step website of search
    url_end = attrubute_first(instruct[0])
    #check if there is correct format
    if url_end == '': 
        #data not found'
        return '格式錯誤!!'
    #the instruct is done, delete it
    del instruct[0]
    #the cards coincide to input
    out = attrubute_second(url_end, instruct)
    #return output
    return out


#in the tag page, compare for the name
def tag_container(name,url_end):
    #go to the website
    card = webin(url_end)
    #get all card href in the tag page
    data = card.soup.find('div', class_ = 'ui_unique_tag_list')
    data = data.find('ul')
    data = data.find_all('li', recursive = False)
    #get the name and href of card
    cards = []
    for all in data:
        search = all.find('a').get('href')
        #compare if the href is the name of correct card
        if search.find(name) != -1:
            print('tag_container: ' + search)
            #the correct
            cards.append(search[1:])
    #return all card coincide input
    return cards

#find all card in draw
def tag_draw(tag):
    #the draw website url
    url_end = 'tag/list/ガチャ排出一覧'
    #all draw 
    tags = tag_container(tag, url_end)
    out_text = ''
    for cards in tags:
        out_text += attrubute_second(cards, [])
    #return card gatch data
    return out_text

#find by name in tag
def tag_all(tag,name):
    url_end = 'tag'
    next = True
    total = 0
    while next == True:
        #go to tag website
        tags = webin(url_end)
        
        #find tag
        html = tags.soup.find('div', id = "ui_tag_all_container").find_all('li')
        for list in html:
            search = BeautifulSoup(str(list), 'html.parser')
            
            #get the correct tag
            target = search.get_text()
            if target.find(tag) != -1:
                url_end = search.find('a').get('href')
                #search by name
                result = tag_container(name, url_end)
                #check if there is card coincide to the input
                total = len(result)
                #not found, find another tag
                if total == 0:
                    continue
                #get the card, leave tags search
                else:
                    next = False 
                    break
        
        #check if there is correct card in this page
        if next == False:
            break
        #go to next page            
        html = tags.soup.find('div', class_ = 'ui_pagination js_pagination').find_all('a')
        for list in html:
            #check if there is next page
            if list.get_text().find('次へ ') != -1:
                url_end = list.get('href')
            else:
                next = False
                
    #only one correct data
    if total == 1:
        #return card
        return find_card(result[0])
    #many cards coincide to the input
    elif total > 1:
        #make the list to string
        out = ''
        for card in result:
            out = out + card + '\n' 
        #return string
        return out
    #data not found
    else:
        return '查無資料'            

#find card by tag          
def find_tag(tag,name):
    #get tag
    tag = get_data(tag)
    print('tag = ' + tag + ' name = ' + name)
    if name == 'draw':
        return tag_draw(tag)
    else:
        return tag_all(tag,name)     
    
#@card.route('/')
def search_card(inlist):
    #id method
    if inlist[0].find('no') != -1:
        return find_id(inlist[0])
    #tag method
    elif inlist[0].find('tag') != -1:
        #check input format
        if len(inlist) < 2:
            inlist.append('')
        return find_tag(inlist[0],inlist[1])

    #attribute method
    else:
        return find_attrubute(inlist)