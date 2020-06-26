import datetime
import json
import os
import dotenv
import string
import requests
import dropbox

from bs4 import BeautifulSoup
import bs4
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import re
import arrow
import sqlalchemy


dotenv.load_dotenv()

# Alap függvények


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


def get_soups(page_links, sleep_time=3):
    soups = []
    for page_link in page_links:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        soups.append(soup)
        time.sleep(sleep_time)
    return soups


# Mandiner
home = "mandiner.hu"
day = date.today().strftime("%Y%m%d")

page = requests.get("https://" + home + "/")
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if day in item.get("href"):
            l.append(item.get("href"))
links = list(set(l))

mandiner_links = []
for link in links:
    if "https://" not in link:
        if "#comments" not in link:
            mandiner_links.append("https://mandiner.hu" + link)

soups = get_soups(mandiner_links)

mandiner_out = pd.DataFrame(list(zip(mandiner_links, soups)), columns=["Link", "Soup"])
mandiner_out["Page"] = "Mandiner"


# 444
home = "444.hu"
day = date.today().strftime("%Y/%m/%d/")
negy_links = get_links(home, day)
soups = get_soups(negy_links)

negy_out = pd.DataFrame(list(zip(negy_links, soups)), columns=["Link", "Soup"])
negy_out["Page"] = "444"


# HVg
home = "hvg.hu"
day = date.today().strftime("%Y%m%d")

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
    if "https://" not in link:
        if "/360/" not in link:
            hvg_links.append("https://hvg.hu" + link)


soups = get_soups(hvg_links)

hvg_out = pd.DataFrame(list(zip(hvg_links, soups)), columns=["Link", "Soup"])
hvg_out["Page"] = "HVG"


# Origo
home = "www.origo.hu/index.html"
day = date.today().strftime("%Y%m%d")

page = requests.get("https://" + home, allow_redirects=False)
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if day in item.get("href"):
            if "origo.hu" in item.get("href"):
                l.append(item.get("href"))
origo_links = list(set(l))

soups = get_soups(origo_links)


origo_out = pd.DataFrame(list(zip(origo_links, soups)), columns=["Link", "Soup"])
origo_out["Page"] = "Origo"


# 24.hu
home = "24.hu"
day = date.today().strftime("%Y/%m/%d/")
# day = "2020/06/17"
links = get_links(home, day)

huszon_links = []
for link in links:
    if "https://24.hu/" in link:
        huszon_links.append(link)

soups = get_soups(huszon_links)

huszon_out = pd.DataFrame(list(zip(huszon_links, soups)), columns=["Link", "Soup"])
huszon_out["Page"] = "24.hu"


# Ripost
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

ripost_out = pd.DataFrame(list(zip(ripost_links, soups)), columns=["Link", "Soup"])
ripost_out["Page"] = "Ripost"


# 888.hu
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

soups = get_soups(nyolc_links)

nyolc_out = pd.DataFrame(list(zip(nyolc_links, soups)), columns=["Link", "Soup"])
nyolc_out["Page"] = "888"


# VG
page = requests.get("https://vg.hu/")
soup = BeautifulSoup(page.content, "html.parser")
l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "vg.hu" in item.get("href"):
            l.append(item.get("href"))
links = list(set(l))
vg_links = []
for link in links:
    try:
        a = int(link[-8:-1])
        vg_links.append(link)
    except:
        pass

soups = get_soups(vg_links)

vg_out = pd.DataFrame(list(zip(vg_links, soups)), columns=["Link", "Soup"])
vg_out["Page"] = "Világgazdaság"


# Figyelő

page = requests.get("https://figyelo.hu/")
soup = BeautifulSoup(page.content, "html.parser")

l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "figyelo.hu" in item.get("href"):
            if "hetilap" not in item.get("href"):
                l.append(item.get("href"))
links = list(set(l))

figyelo_links = []
for link in links:
    try:
        a = int(link[-7:-1])
        figyelo_links.append(link)
    except:
        pass

soups = get_soups(figyelo_links)

figyelo_out = pd.DataFrame(list(zip(figyelo_links, soups)), columns=["Link", "Soup"])
figyelo_out["Page"] = "Figyelő"


# Alfahír
page = requests.get("https://alfahir.hu/")
soup = BeautifulSoup(page.content, "html.parser")

day = date.today().strftime("%Y/%m/%d/")

l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if day in item.get("href"):
            l.append(item.get("href"))
links = list(set(l))

alfahir_links = []
for link in links:
    if "https://" not in link:
        alfahir_links.append("https://alfahir.hu" + link)

soups = get_soups(alfahir_links)

alfahir_out = pd.DataFrame(list(zip(alfahir_links, soups)), columns=["Link", "Soup"])
alfahir_out["Page"] = "Alfahír"


# Napi.hu
page = requests.get("https://napi.hu/")
soup = BeautifulSoup(page.content, "html.parser")

l = []
for item in soup.find_all("a"):
    if type(item.get("href")) == str:
        if "napi.hu" in item.get("href"):
            if "www.facebook.com" not in item.get("href"):
                l.append(item.get("href"))
links = list(set(l))


napi_links = []
for link in links:
    try:
        a = int(link[-11:-5])
        napi_links.append(link)
    except:
        pass

soups = get_soups(napi_links)

napi_out = pd.DataFrame(list(zip(napi_links, soups)), columns=["Link", "Soup"])
napi_out["Page"] = "Napi.hu"


# Index
home = "index.hu"
day = date.today().strftime("%%2F%Y%%2F%m%%2F%d")
links = get_links(home, day)

index_links = []
for i in range(len(links)):
    if "mindekozben" not in links[i]:
        index_links.append(links[i])

soups = get_soups(index_links)

index_out = pd.DataFrame(list(zip(index_links, soups)), columns=["Link", "Soup"])
index_out["Page"] = "Index"


new_posts = pd.concat(
    [
        negy_out,
        hvg_out,
        origo_out,
        huszon_out,
        ripost_out,
        nyolc_out,
        mandiner_out,
        figyelo_out,
        vg_out,
        napi_out,
        alfahir_out,
        index_out,
    ]
)
new_posts["Date"] = date.today()

new_posts["Soup"] = new_posts["Soup"].apply(str)

local_path = "/links_soups.pkl"
dropbox_path = "/links_soups_{}.pkl".format(date.today().strftime("%d-%m-%Y"))

new_posts.to_pickle(local_path)

dropbox_access_token = os.environ["DROPBOX_TOKEN"]

client = dropbox.Dropbox(dropbox_access_token)
print("[SUCCESS] dropbox account linked")

client.files_upload(open(local_path, "rb").read(), dropbox_path)
print("[UPLOADED] to {}".format(dropbox_path))
