#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dropbox
import pandas as pd
import pickle

import datetime
import json
import os
import dotenv
import string
import requests

from bs4 import BeautifulSoup
import bs4
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import re

dropbox_access_token = os.environ["DROPBOX_TOKEN"]  # Enter your own access token
client = dropbox.Dropbox(dropbox_access_token)

response = client.files_list_folder("")

files = []
for file in response.entries:
    files.append(file.name)

df = pd.DataFrame(columns=["Link", "Soup", "Page", "Date", "Content"])
for name in files:
    metadata, data = client.files_download("/" + name)
    df = df.append(pickle.loads(data.content))
df = df.drop_duplicates(subset="Link").reset_index(drop=True)

# Mandiner


def get_Mandiner(df):
    page = "Mandiner"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("articletext"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# 444
def get_444(df):
    page = "444"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = BeautifulSoup(soup).find_all("article")[0].find_all("p")
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# hvg
def get_HVG(df):
    page = "HVG"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("article-menu_main"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# origo
def get_Origo(df):
    page = "Origo"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = BeautifulSoup(soup).find_all("p")
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# 24.hu
def get_24(df):
    page = "24.hu"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("o-post__body o-postCnt post-body"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# ripost
def get_Ripost(df):
    page = "Ripost"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("content-holder"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# 888
def get_888(df):
    page = "888"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("maincontent8"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# vg
def get_VG(df):
    page = "Világgazdaság"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("entry-content clearfix"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# figyelő
def get_Figyelő(df):
    page = "Figyelő"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("entry-content clearfix"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents)


# alfahír
def get_Alfahír(df):
    page = "Alfahír"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("article-content"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents[1:])


# napihu
def get_Napi(df):
    page = "Napi.hu"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup).find("div", class_=re.compile("article")).find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents[3:])


# index
def get_Index(df):
    page = "Index"
    soups = df.loc[df["Page"] == page]["Soup"].dropna()
    for i, soup in enumerate(soups):
        linkcontents = []
        soup = (
            BeautifulSoup(soup)
            .find("div", class_=re.compile("cikk-torzs"))
            .find_all("p")
        )
        for n in range(len(soup)):
            if soup != "":
                linkcontents.append(soup[n].text)
        df.loc[soups.index[i], "Content"] = " ".join(linkcontents[1:])


get_444(df)
get_Origo(df)
get_HVG(df)
get_24(df)
get_Ripost(df)
get_888(df)
get_Mandiner(df)
get_Figyelő(df)
get_VG(df)
get_Napi(df)
get_Alfahír(df)
get_Index(df)

df = df.drop(columns="Soup")

local_path = "/contents.pkl"
dropbox_path = "/contents_{}.pkl".format(date.today().strftime("%d-%m-%Y"))

df.to_pickle(local_path)

client = dropbox.Dropbox(dropbox_access_token)
print("[SUCCESS] dropbox account linked")

client.files_upload(open(local_path, "rb").read(), dropbox_path)
print("[UPLOADED] to {}".format(dropbox_path))
