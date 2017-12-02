#coding=utf-8
'''
Created on 2017/12/1
@author: danny
blueprint test
count Chain
'''

from flask import Blueprint
import math

PF = Blueprint('PF',__name__) #regisster

@PF.route('/')
def count_Chain(mlist):
# 1 1 2 3 4 : 5
# 3 . 1 2 3 . 4 + 4 + 1 : 5
    try:
        tmp = mlist.index('.')             #if . exist,there are more than one fire 
        numOfFire = int(mlist[tmp - 1])    #amount of fire
        mlist = mlist[tmp + 1:]             
        index_base = mlist.index('.')       #index .
        Separated = mlist.index(':')        #index :
    except:
        try:
            Separated = mlist.index(':')        #else, only one fire
            numOfFire = 1
            index_base = Separated              #index :
        except: return -1
    try:
        index_atk = index_base

        if numOfFire <= 0:              #no fire
            raise
        if numOfFire > 1:
            index_atk = mlist.index('+')#index +
    
        deff = 0
        for i in range(Separated + 1, len(mlist)): #count hp + def ,  5
            deff += int(mlist[i])
    
        atk = 1.0    
        for i in range(index_base):     #count base , 1 2 3
            atk *= float(mlist[i])
    
        total = 0
        for i in range(numOfFire):      #count fire , 4 + 4 + 1
            damage = 1
            for j in range(index_base + 1, index_atk, 1):   #mulity , 4 and 4 and 1
                damage *= int(mlist[j])
            total += damage                                     #add, 4 + 4 + 1
            index_base = index_atk
            if '+' in mlist[index_atk + 1:]:                    #index of next + or :
                index_atk = mlist[index_atk + 1:].index('+')
            elif ':' in mlist[index_atk + 1:]:
                index_atk = mlist[index_atk + 1:].index(':')
            index_atk = index_atk + index_base + 1
        # (chain * 2 * 0.01 + 1) * base_atack >= hp + def
        chain = (deff / (total * atk) - 1) / 2 / 0.01       
        if chain < 0: chain = 0
        chain = math.ceil(chain)
        out = str(chain).encode('utf-8') + u' C可殺'.encode('utf-8')
        return out

    except:
        return u'指令pf, 錯誤格式: '.encode('utf-8') + ''.join(mlist).encode('utf-8')