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
# Edgelist

name = "contents_{}.pkl".format(date.today().strftime("%d-%m-%Y"))
metadata, data = client.files_download("/" + name)

data = pickle.loads(data.content)

pages = list(data["Page"].unique())

edgelist = pd.DataFrame(columns=["Source", "Target", "Weight"])

for page in pages:
    sub_data_network = data.loc[data["Page"] != page]
    for article in sub_data_network.itertuples():
        if page in article[4]:
            edgelist = edgelist.append(
                {"Source": article[2], "Target": page, "Weight": 0}, ignore_index=True
            )

table = pd.pivot_table(edgelist, index=["Source"], columns=["Target"], aggfunc="count")


for i in range(len(edgelist)):
    edgelist.loc[i, "Weight"] = table["Weight"].loc[
        edgelist.loc[i, "Source"], edgelist.loc[i, "Target"]
    ]

local_path = "/edgelist.pkl"
dropbox_path = "/edgelist.pkl"

edgelist.to_pickle(local_path)

client.files_upload(open(local_path, "rb").read(), dropbox_path)
print("[UPLOADED] to {}".format(dropbox_path))
