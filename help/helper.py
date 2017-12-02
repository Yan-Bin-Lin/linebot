#coding=utf-8
'''
Created on 2017/12/1
@author: danny
instruction of linebot
'''
from flask import Blueprint

helper = Blueprint('helper',__name__) #regisster

@helper.route('/')
def help_all(instr):
   
    if instr:
        if instr == 'pf':
            return help_pf()
        
        else:
            out = u'指令help, 查無參數: '.encode('utf_8') + instr.encode('utf-8')
            return out
    else:
        return help_instruct()
    

def help_instruct():

    with helper.open_resource('instruction.txt') as file:
        out = file.read()
    return out
    
def help_pf():
    with helper.open_resource("PF.txt") as file:
        out = file.read()     
    return out      