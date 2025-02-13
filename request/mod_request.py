import requests
from bs4 import BeautifulSoup
import time
import logging
from fake_useragent import UserAgent

def obtenir_req(url):
  max_retry = 6
  logger = logging.getLogger()
  headers = {"User-Agent": UserAgent().random}

  for retry in range(max_retry):
    try:
      req = requests.get(url, verify=False, headers=headers)
      if (req.status_code != 200):
        logger.error(f'Tentative {retry}')
        logger.error(f'ERREUR au obtenir les donnees du lien {url}. Status code {req.status_code}')
        time.sleep(30)
        continue
      return req
    except Exception as e:
      logger.error(f'Tentative {retry}')
      logger.error(f'ERREUR au obtenir les donnees du lien {url}')
      logger.error(e)
      time.sleep(30)
      pass
  return None

def obtenir_soup(url):
  req = obtenir_req(url)
  return BeautifulSoup(req.content.decode('utf-8'), 'html.parser')


def obtenir_meteo(url):
  req = obtenir_req(url)
  return req.json()[0]['observation']