#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import json
import os
import dotenv
import string
import requests
import bs4

from bs4 import BeautifulSoup
import bs4
import selenium
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from datetime import datetime
import re
import arrow
import sqlalchemy


# In[ ]:


dotenv.load_dotenv()


# In[ ]:





# In[ ]:


constring = os.environ["VL_CONSTRING"]


# In[ ]:




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


out= pd.DataFrame(list(zip(pagelinks_final,contents)), 
               columns =['Link', 'Content'])
out['Page']="444.hu"
out.to_sql(name="probalol", con=constring, if_exists="replace", index=False)


# In[ ]:


page = requests.get("https://index.hu/")
soup = BeautifulSoup(page.content, "html.parser")
l = []

for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "2F2020%2F06%2F17" in item.get("href"):
            if "2Findex.hu" in item.get("href"):
                l.append(item.get("href"))
links = list(set(l))

index_links = []
for i in range(len(links)):
    if "mindekozben" not in links[i]:
        index_links.append(links[i])

soups = []
for pagelink in index_links:
    page = requests.get(pagelink)
    soup = BeautifulSoup(page.content, "html.parser")
    soups.append(soup)
    time.sleep(1)

contents = []
for i in range(len(soups)):
    linkcontents = []
    for n in range(
        len(soups[i].find("div", class_=re.compile("cikk-torzs")).find_all("p"))
    ):
        if (soups[i].find("div", class_=re.compile("cikk-torzs")).find_all("p")) != "":
            linkcontents.append(
                soups[i]
                .find("div", class_=re.compile("cikk-torzs"))
                .find_all("p")[n]
                .text
            )
    contents.append("".join(linkcontents[1:]))

out= pd.DataFrame(list(zip(index_links,contents)), 
                   columns =['Link', 'Content'])

out.to_sql(name="index_proba_konyorgom", con=constring, if_exists="replace", index=False)

