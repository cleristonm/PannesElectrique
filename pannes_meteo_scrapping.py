from modele.panne import Panne
from modele.meteo import Meteo
from soup.mod_soup import obtenir_soup
import dao.mod_dao_regions as dao_region
import dao.mod_dao_pannes as dao_pannes
import dao.mod_dao_meteo as dao_meteo
import dao.mod_dao_scrapping as dao_scrapping
import urllib3
import requests

def get_clients_prives_eletricite(text):
    text = text.replace(" ", "")

    client_decoupes = text.split("clientssansélectricitésur")

    if len(client_decoupes) <= 1:
        client_decoupes = text.split("clientsansélectricitésur")

    if len(client_decoupes) <= 1:
        return [0, 0]

    return client_decoupes

def inserer_donnes_pannes(region, id_scrapping):
    soup = obtenir_soup(region.lien)
    clients = soup.select('#recap > span:nth-child(1)')[0].get_text()
    [clients_prive, clients_total] = get_clients_prives_eletricite(clients)
    interruption = soup.select('#recap > span:nth-child(3)')[0].get_text().split(" ")[0]
    panne = Panne(None, region.id, id_scrapping, interruption, clients_prive, clients_total)
    dao_pannes.inserer_panne(panne)

def inserer_donnes_meteo(region, id_scrapping):
    reponse = requests.get(region.lien_meteo).json()[0]['observation']
    condition = reponse['condition']
    pression = reponse['pressure']['metric']
    temperature = reponse['temperature']['metricUnrounded']
    point_de_rosee = reponse['dewpoint']['metricUnrounded']
    humidite  =reponse['humidity']
    vent_direction = reponse['windDirection']
    vent_velocite  = reponse['windSpeed']['metric']
    visibilite = reponse['visibility']['metric']

    meteo = Meteo(None, region.id, id_scrapping, condition, pression, temperature,
                  point_de_rosee, humidite, vent_direction, vent_velocite, visibilite)
    dao_meteo.inserer_meteo(meteo)

def scraping():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    dao_pannes.create_table()
    dao_scrapping.create_table()
    dao_meteo.create_table()
    id_scrapping = dao_scrapping.inserer_scrapping()
    regions = dao_region.selectionner_regions_avec_lien_meteo()
    for region in regions:
        inserer_donnes_pannes(region, id_scrapping)
        inserer_donnes_meteo(region, id_scrapping)
    dao_scrapping.maj_scrapping(id_scrapping)

if __name__ == "__main__":
    scraping()
