#!/usr/bin/env python
# coding: utf-8

# In[65]:


import datetime
import json
import os
import dotenv
import string
import requests
import bs4

import selenium
import requests

from selenium import webdriver
import time

import pandas as pd
import numpy as np
from datetime import datetime
import re
import arrow

import sqlalchemy


dotenv.load_dotenv()



constring = os.environ["VL_CONSTRING"]
