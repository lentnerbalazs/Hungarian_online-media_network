#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import networkx as nx
import pyvis
from pyvis.network import Network

import dotenv
import string
import requests
import bs4


from bs4 import BeautifulSoup
import bs4
import time
import numpy as np
from datetime import datetime
from datetime import date
import re
import arrow
import sqlalchemy
from collections import Counter

import glob
import string
import json
import os
import subprocess
import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components import Div, H3, H1, Link, P
import plotly.express as px

import dropbox
import pickle


# In[ ]:


dotenv.load_dotenv()


# In[2]:


dropbox_access_token = os.environ["DROPBOX_TOKEN"]
client = dropbox.Dropbox(dropbox_access_token)

# In[4]:
data_name = "contents.pkl"

metadata, data = client.files_download("/" + data_name)

data= pickle.loads(data.content)

# In[5]:
edge_name = "edgelist.pkl"

metadata, edge_data = client.files_download("/" + edge_name)

edgelist = pickle.loads(edge_data.content)


# In[6]:


height="800px"
width="100%"
name="VL_AAA_final"


# In[7]:


citation_net = Network(
    height=height,
    width=width,
    bgcolor="FFFFFF",
    font_color="black",
    directed=True,
    notebook=False,
)
citation_net.barnes_hut()
sources = edgelist["Source"]
targets = edgelist["Target"]
weights = edgelist["Weight"]
#size = 2*df["closeness centrality"]
#color = df["color"]

edge_data = zip(sources, targets,weights) #, weights, size, color
for e in edge_data:
    src = str(e[0])
    dst = str(e[1])
    w = e[2]
    #s = e[3]
    #c = e[4]
    citation_net.add_node(src, src, title=src) #, size=s, color=c
    citation_net.add_node(dst, dst, title=dst) #, size=s, color=c
    citation_net.add_edge(src, dst,value=w) #, value=w
    #neighbor_map = citation_net.get_adj_list()

#for node in citation_net.nodes:
#    node["title"] += info_dic[node["title"]]
#    node["value"] = len(neighbor_map[node["id"]])

citation_net.set_options(
    """
var options = {
  "nodes": {
    "borderWidth": 2,
    "color": {
      "highlight": {
        "background": "rgba(217,255,50,1)"
      }
    },
    "font": {
      "size": 50,
      "face": "tahoma"
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}
"""
)

citation_net.show("citation_net_" + name + ".html")


# In[ ]:





# In[8]:


def clean_text(article):
    clean1 = re.sub(r'['+string.punctuation + '’—”'+']', "", article.lower())
    return re.sub(r'\W+', ' ', clean1)

data['tokenized'] = data['Content'].map(lambda x: clean_text(x))

data.head()

data['num_wds'] = data['tokenized'].apply(lambda x: len(x.split()))
data['num_wds'].mean()

data[data['tokenized']==""]

data = data[data['num_wds']>0]

data=data.reset_index(drop=True)


data['uniq_wds'] = data['tokenized'].str.split().apply(lambda x: len(set(x)))


# In[ ]:


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Média hálózat"

app.scripts.config.serve_locally = True

# correl plot
fig1=px.histogram(data, x='Page', y='Page', histfunc='count',  color='Page')
fig1.update_layout(title_text="Cikkek száma az adatbázisban",
    xaxis_title="Hírportál",
    yaxis_title="Cikkek száma",
    xaxis={'categoryorder':'category ascending'},
    xaxis_type='category')

fig2=go.Figure(data=[
    go.Histogram(histfunc="avg", y=data['num_wds'], x=data['Page'], name="átlagos szószám"),
    go.Histogram(histfunc="avg", y=data['uniq_wds'], x=data['Page'], name="átlagos egyedi szószám")
])
fig2.update_layout(title_text="Átlagos szószám hírportálonként",
    xaxis_title="Hírportál",
    yaxis_title="Szavak száma hírportálonként",
    xaxis_type='category')


markdown_text = """
Ez a projekt egy kurzuszáró munka a Rajk Szakkollégium Alkalmazott Adatközpontú Algoritmustervezés kurzusára. 
A projekt lényege, hogy [Github Actions](https://github.com/lentnerbalazs/Vig_Lentner) segítségével naponta kétszer letöltjük 12 magyar hírportál főoldalán található 
cikkeket, majd a szövegekből kinyerjük az oldalak egymásra mutató hivatkozásait. A hivatkozásokból hálózatot építünk 
a cikkek szövegeiből pedig egyszerű leíró statisztikákat készítünk hírportál szerinti bontásban. A megjelenítés Dash 
felületen egy Heroku applikáción keresztül történik.
"""


# layout
app.layout = html.Div(
    children=[
        H1(
            children=" Hivatkozási hálózat ",
            style={
                "color": "black",
                "backgroundColor": "ffffff",
                "text-align": "center",
            },
        ),
        html.Div(
            children=[
                html.P(
                    children=[
                        H3(children="Miről szól a projekt?"),
                        html.Element(dcc.Markdown(children=markdown_text),),
                    ],
                    className="six columns",
                ),
                html.Div(
                    html.Iframe(
                        srcDoc=open("citation_net_VL_AAA_final.html").read(),
                        style={"height": "100%", "width": "100%"},
                    ),
                    style={"height": "400px"},
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                 children=[dcc.Graph(id="correl-graph", figure=fig1),],
                    className="six columns",
                ),
                html.Div(
                 children=[dcc.Graph(id="correl-graph2", figure=fig2),],
                    className="six columns",
                ),
            ],
            className="row",
        ),
    ]
)


server = app.server

if __name__ == "__main__":

    app.run_server(debug=False)


# In[ ]:




