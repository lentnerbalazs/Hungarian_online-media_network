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


# In[61]:


import networkx as nx
import pyvis

from pyvis.network import Network


# In[2]:


dotenv.load_dotenv()


# In[ ]:


constring = os.environ["VL_CONSTRING"]


# In[ ]:





# In[5]:


data=pd.read_sql_table("VL_articles_main_v1", con=constring)


# In[8]:


data.head()


# In[10]:


Pages=list(data['Page'].unique())


# In[121]:


edgelist=pd.DataFrame(columns=['Source', 'Target', 'Weight'])


# In[125]:


for page in Pages:
    sub_data_network=data[data['Page']!=page]
    for article in sub_data_network.itertuples():
        if page in article[2]:
            edgelist=edgelist.append({'Source': article[3], 'Target':page, 'Weight':0},ignore_index=True)


# In[127]:


table = pd.pivot_table(edgelist, index=['Source'],
                    columns=['Target'], aggfunc='count')


for i in range(len(edgelist)):
    edgelist.loc[i, 'Weight']=table['Weight'].loc[edgelist.loc[i, 'Source'],edgelist.loc[i, 'Target']]


# In[ ]:


###Figyelj a replace-append-re 


# In[136]:


edgelist.to_sql(name="VL_edgelist_main_v1", con=constring, if_exists="replace", index=False)


# In[ ]:





# In[66]:


height="800px"
width="100%"
name="VL_AAA_final"


# In[133]:


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

#citation_net.show("citation_net_" + name + ".html")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




