import requests
from bs4 import BeautifulSoup
import lxml

def obtenir_soup(url):
  req = requests.get(url, verify=False)
  return BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
