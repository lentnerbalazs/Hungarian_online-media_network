#!/usr/bin/env python
# coding: utf-8

# In[60]:


import datetime
import json
import os
import dotenv
import string
import requests
from bs4 import BeautifulSoup

import gspread

import bs4

import selenium

from oauth2client.service_account import ServiceAccountCredentials


import requests
from bs4 import BeautifulSoup

from selenium import webdriver
import time

import pandas as pd
import numpy as np
from datetime import datetime
import re
import arrow


# In[8]:


gc = gspread.service_account(filename='C:/Users/thinkpad/Desktop/progprojekt/creds.json')


# In[15]:


spread_id = "1nHO_Ch5GGxxlzj-3X3j8kGbsJX-A3De2vGaSrf5L-5o"

d = json.load(open("creds.json"))

#d["private_key"] = os.environ["GSPREAD_PRIVATE_KEY"]

scope = ["https://spreadsheets.google.com/feeds"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(d, scope)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key(spread_id).sheet1


# In[62]:


if __name__ == "__main__":
    ### oldal amit használok 444.hu
    page = requests.get('https://444.hu/')
    ### leves, parsolás, html szövegként
    soup = BeautifulSoup(page.content, 'html.parser')
    ## a főoldalon nincsenek különböző hirblokkok, elég csak a központi blokkra  létrehozni egy listát amiben be vannak ágyazva a linkek a cikkekhez
    weblinks_all = soup.find_all('div', class_=re.compile('row'))
    ###Kiszedi az összes linket és berakja egy listába
    pagelinks=[]
    for weblinks in weblinks_all:
        for item in weblinks.find_all('a'):
            pagelinks.append(item.get('href'))
    pagelinks=list(set(pagelinks))
    ###létrehozok egy listát az elmúlt 4 npról megfelelő formátumban, hogy ki tudjam szűrni a releváns linkekeket
    delay=[]
    for i in range(4):
        delay.append(arrow.now().shift(days=-i).format('YYYY/MM/DD'))
    #létrehozom a végleges link listát, amiben csak azok szerepelnek, amik a 444-re vezetnek,  amikben dátum van, ezek a rendes cikkek és nem a comment szekcióra vezetnek át
    pagelinks_final=[]
    for n in range(len(delay)):
        for i in range(len(pagelinks)):
            if (delay[n] in pagelinks[i])==True and pagelinks[i][-9:]!='#comments' and pagelinks[i][:14]=='https://444.hu':
                pagelinks_final.append(pagelinks[i])

    # létrehozok egy lista az összes cikkről ami van a  főoldalonvan és leszedem a tartalmukat
    soups=[]
    for pagelink in pagelinks_final:
        page=requests.get(pagelink)
        soup=BeautifulSoup(page.content, 'html.parser')
        soups.append(soup)
    ## Csinálok egy listákból álló listát, aminek a hossza megegyezik a cikkek számával, minden cikkhez tartozik egy lista,
    #ami tördelt részletekben tartalmmazza a cikkek szövegét, innentől kezdve megvan minden cikk szövege egy helyen
    contents=[]
    for i in range(len(soups)):
        linkcontents=[]
        for n in range(len(soups[i].find_all('article')[0].find_all('p'))):
            if (soups[i].find_all('article')[0].find_all('p')[n].text)!='':
                linkcontents.append(soups[i].find_all('article')[0].find_all('p')[n].text)
        contents.append(linkcontents)


    dictionary = dict(zip(keys, values))

    out=[]
    for i in range(len(pagelinks_final)):
        dic={"link":str(pagelinks_final[i]), "content":str(contents[i])}
        out.append(dic)

    record = out[0]
    col_headers = list(record.keys())
    end_letter = string.ascii_uppercase[len(col_headers) - 1]
    end_of_sheet = sheet.row_count
    end_of_sheet=1
    rows = [list(d.values()) for d in out]
    sheet.add_rows(len(rows))
    sheet_range_name = f"A{end_of_sheet + 1}:{end_letter}{len(rows)+end_of_sheet}"
    sheet.update(sheet_range_name, rows)

