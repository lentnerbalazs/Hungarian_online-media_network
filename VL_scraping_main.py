#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from datetime import date
import re
import arrow
import sqlalchemy


# In[2]:


dotenv.load_dotenv()


# In[ ]:


constring = os.environ["VL_CONSTRING"]


# In[4]:


#Alap függvények


# In[5]:


def get_links(home_string, day_string):
    page = requests.get("https://" + home + "/", allow_redirects=False)
    soup = BeautifulSoup(page.content, "html.parser")
    l = []
    for item in soup.find_all("a"):
        if type(item.get("href")) == str:
            if day_string in item.get("href"):
                if home_string in item.get("href"):
                    l.append(item.get("href"))
    links = list(set(l))
    return links


# In[6]:


def get_soups(page_links):
    soups = []
    for page_link in page_links:
        page = requests.get(page_link, allow_redirects=False)
        soup = BeautifulSoup(page.content, "html.parser")
        soups.append(soup)
        time.sleep(5)
    return soups


# In[7]:


#Oldalak: 


# In[8]:


#Index
home = "index.hu"
day = date.today().strftime("%%2F%Y%%2F%m%%2F%d")
links = get_links(home, day)

index_links = []
for i in range(len(links)):
    if "mindekozben" not in links[i]:
        index_links.append(links[i])

soups = get_soups(index_links)

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
    contents.append(" ".join(linkcontents[1:]))

index_out = pd.DataFrame(list(zip(index_links, contents)), columns=["Link", "Content"])
index_out['Page']="Index"


# In[ ]:


#444
home = "444.hu"
day = date.today().strftime("%Y/%m/%d/")
negy_links = get_links(home, day)
soups = get_soups(negy_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    for n in range(len(soups[i].find_all("article")[0].find_all("p"))):
        if (soups[i].find_all("article")[0].find_all("p")[n].text) != "":
            linkcontents.append(soups[i].find_all("article")[0].find_all("p")[n].text)
    contents.append(" ".join(linkcontents))

negy_out = pd.DataFrame(list(zip(negy_links, contents)), columns=["Link", "Content"])
negy_out['Page']="444"


# In[9]:


#HVG
home = "hvg.hu"
day = date.today().strftime("%Y%m%d")
# day = '20200617'

page = requests.get("https://" + home + "/")
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if day in item.get("href"):
            l.append(item.get("href"))
links = list(set(l))
hvg_links = []
for link in links:
    if "360/" not in link:
        if "https://" not in link:
            hvg_links.append("https://hvg.hu" + link)

soups = get_soups(hvg_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    soup = soups[i].find("div", class_=re.compile("article-menu_main")).find_all("p")
    for n in range(len(soup)):
        if (soup) != "":
            linkcontents.append(soup[n].text)
    contents.append(" ".join(linkcontents))

hvg_out = pd.DataFrame(list(zip(hvg_links, contents)), columns=["Link", "Content"])
hvg_out['Page']="HVG"


# In[ ]:


#Origo
home = "origo.hu"
day = date.today().strftime("%Y%m%d")
# day = "20200617"
origo_links = get_links(home, day)

soups = get_soups(origo_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    soup = soups[i].find_all("p")
    for n in range(1, (len(soup))):
        if (soup) != "":
            linkcontents.append(soup[n].text)
    contents.append(" ".join(linkcontents))

origo_out = pd.DataFrame(list(zip(origo_links, contents)), columns=["Link", "Content"])
origo_out['Page']="Origo"


# In[ ]:


#24.hu
home = "24.hu"
day = date.today().strftime("%Y/%m/%d/")
# day = "2020/06/17"
huszon_links = get_links(home, day)

soups = get_soups(huszon_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    soup = (
        soups[i]
        .find("div", class_=re.compile("o-post__body o-postCnt post-body"))
        .find_all("p")
    )
    for n in range(1, (len(soup))):
        if (soup) != "":
            linkcontents.append(soup[n].text)
    contents.append(" ".join(linkcontents))

huszon_out = pd.DataFrame(
    list(zip(huszon_links, contents)), columns=["Link", "Content"]
)
huszon_out['Page']="24.hu"


# In[ ]:


#Ripost
page = requests.get("https://ripost.hu/")
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "ripost.hu" in item.get("href"):
            l.append(item.get("href"))
links = list(set(l))
ripost_links = []
for link in links:
    try:
        a = int(link[-8:-1])
        ripost_links.append(link)
    except:
        pass

soups = get_soups(ripost_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    soup = soups[i].find("div", class_=re.compile("content-holder")).find_all("p")
    for n in range(1, (len(soup))):
        if (soup) != "":
            linkcontents.append(soup[n].text)
    contents.append(" ".join(linkcontents))

ripost_out = pd.DataFrame(
    list(zip(ripost_links, contents)), columns=["Link", "Content"]
)
ripost_out['Page']="Ripost"


# In[ ]:


#888.hu
page = requests.get("https://888.hu/")
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "888.hu" in item.get("href"):
            l.append(item.get("href"))

links = list(set(l))

nyolc_links = []
for link in links:
    try:
        a = int(link[-8:-1])
        nyolc_links.append(link)
    except:
        pass

# ezt csekkolni kell minden nap mi az új és csak azokat beletenni!

soups = get_soups(nyolc_links)

contents = []
for i in range(len(soups)):
    linkcontents = []
    soup = soups[i].find("div", class_=re.compile("maincontent8")).find_all("p")
    for n in range(1, (len(soup))):
        if (soup) != "":
            linkcontents.append(soup[n].text)
    contents.append(" ".join(linkcontents))

nyolc_out = pd.DataFrame(list(zip(nyolc_links, contents)), columns=["Link", "Content"])
nyolc_out['Page']="888"


# In[ ]:


new_posts=pd.concat([index_out,negy_out,hvg_out,origo_out,huszon_out,ripost_out,nyolc_out])


# In[ ]:


out.to_sql(name="VL_articles_main_v1", con=constring, if_exists="append", index=False)


# In[ ]:


pd.read_sql_table("VL_articles_main_v1", con=constring)


# In[ ]:


main=pd.read_sql_table("VL_articles_main_v1", con=constring)


# In[ ]:


main=main.drop_duplicates(subset='Link', keep="last")


# In[ ]:


main..to_sql(name="VL_articles_main_v1", con=constring, if_exists="replace", index=False)

