import sys
import os
import requests
from bs4 import BeautifulSoup as bs

#local libraries
from .constants import Constants as Cts

class WebUtils:
    def __init__(self):
        self.cts = Cts()

    def get_content(self, ar_url)
