import time

from modele.panne import Panne
from modele.meteo import Meteo
from modele.scrapping_queue import ScrappingQueue
from request.mod_request import obtenir_soup, obtenir_meteo
import dao.mod_dao_regions as dao_region
import dao.mod_dao_pannes as dao_pannes
import dao.mod_dao_meteo as dao_meteo
import dao.mod_dao_scrapping as dao_scrapping
import urllib3
import logging
import traceback
def get_clients_prives_eletricite(text):
    text = text.replace(" ", "")

    client_decoupes = text.split("clientssansélectricitésur")

    if len(client_decoupes) <= 1:
        client_decoupes = text.split("clientsansélectricitésur")

    if len(client_decoupes) <= 1:
        return [0, 0]

    return client_decoupes

def inserer_donnes_pannes(region, id_scrapping):
    logger = logging.getLogger()
    try:
        soup = obtenir_soup(region.lien)
        clients = soup.select('#recap > span:nth-child(1)')[0].get_text()
        [clients_prive, clients_total] = get_clients_prives_eletricite(clients)
        interruption = soup.select('#recap > span:nth-child(3)')[0].get_text().split(" ")[0]
        panne = Panne(None, region.id, id_scrapping, interruption, clients_prive, clients_total)
        id_ajoute = dao_pannes.inserer_panne(panne)
        logger.info(f'Donnees de pannes lié a {region.nom} ont ete ajouté a la BD. Panne id {id_ajoute}')
        return True
    except Exception as e:
        logger.error(f'ERREUR au moment d\'ajouté le donnes de pannes lié à {region.nom}')
        logger.error(e)
        logger.error(traceback.format_exc())
    return False


def inserer_donnes_meteo(region, id_scrapping):
    logger = logging.getLogger()
    try:
        reponse = obtenir_meteo(region.lien_meteo)
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
        id_ajoute = dao_meteo.inserer_meteo(meteo)
        logger.info(f'Donnees de la meteo lié a {region.nom} ont ete ajouté a la BD. Meteo id {id_ajoute}')
        return True
    except Exception as e:
        logger.error(f'ERREUR au moment d\'ajouté le donnes de meteo lié à {region.nom}')
        logger.error(e)
        logger.error(traceback.format_exc())
    return False

def cree_scrapping_queue(regions):
    queue = []
    for region in regions:
        queue.append( ScrappingQueue(region, False, False, 1) )
    return queue
def scrapping():
    max_tentative = 4
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    logger = logging.getLogger()
    dao_pannes.create_table()
    dao_scrapping.create_table()
    dao_meteo.create_table()
    id_scrapping = dao_scrapping.inserer_scrapping()
    logger.info('='*100)
    logger.info(f'Starting Web scrapping id {id_scrapping}')
    regions = dao_region.selectionner_regions_avec_lien_meteo()

    scrapping_queue = cree_scrapping_queue(regions)
    while len(scrapping_queue) > 0:
        element_queue = scrapping_queue.pop(0)
        region = element_queue.region
        logger.info(f'Web scrapping region {region.nom} - Tentative {element_queue.tentative}')
        # S'il ne s'agit pas de la première tentative, il faut attendre 30 secondes.
        if (element_queue.tentative > 1):
            time.sleep(30)

        if (element_queue.pannes_ajoutee == False):
            element_queue.pannes_ajoutee = inserer_donnes_pannes(region, id_scrapping)
        if (element_queue.meteo_ajoutee == False):
            element_queue.meteo_ajoutee = inserer_donnes_meteo(region, id_scrapping)

        # S'il n'a pas été possible d'obtenir les informations de la Panne ou de Meteo,
        # et que le nombre maximum de  tentatives n'a pas été atteint, ajouter à nouveau
        # la région à la file d'attente.
        if ((element_queue.pannes_ajoutee == False or element_queue.meteo_ajoutee == False) and
            (element_queue.tentative <= max_tentative)):
            element_queue.tentative = element_queue.tentative + 1
            scrapping_queue.append(element_queue)

    dao_scrapping.maj_scrapping(id_scrapping)

if __name__ == "__main__":
    logging.basicConfig(filename="std.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logging.getLogger() .setLevel(logging.DEBUG)

    scrapping()
