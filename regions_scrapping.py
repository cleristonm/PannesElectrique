from modele.region import Region
from request.mod_request import obtenir_soup
import dao.mod_dao_regions as dao
import time
from datetime import timedelta
import urllib3
def obtenir_regions(link_parent, id_region_parent):
    soup = obtenir_soup(link_parent)

    tbl = soup.findChildren('tbody')[0]
    rows = tbl.findChildren(['th', 'tr'])
    for row in rows:
        cells = row.findChildren('td')
        if cells:
            tag_a = cells[0].findChildren('a')
            tag_span = cells[0].findChildren('span')
            region_nom = ''
            lien = ''
            if tag_a:
                lien = tag_a[0]['href']
                region_nom = tag_a[0].string
            elif tag_span:
                region_nom = cells[0].findChildren('span')[0].get_text()
                lien = ''

            if tag_a or tag_span:
                region = Region(None, region_nom, id_region_parent, lien, '')
                id = dao.inserer_region(region)
                region.id = id
                print(f'Region ajouté {region}')
                if lien:
                    obtenir_regions(region.lien, region.id)


def scraping():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    start_time = time.time()
    dao.create_table()
    region_quebec_province = Region(None, 'Quebec Provence', None,
                                    'https://pannes.hydroquebec.com/pannes/bilan-interruptions-service/#bis', '')
    id_region_quebec_province = dao.inserer_region(region_quebec_province)
    obtenir_regions(region_quebec_province.lien, id_region_quebec_province)
    td = timedelta(seconds=(time.time() - start_time))
    print("Temps d'éxécution : ", td)

def lister_regions():
    regions = dao.selectionner_regions()
    for r in regions:
        print('=' * 50)
        print(r)
        nom_region_parent = dao.selectionner_nom_region_par_id(r.id_region_parent)
        if nom_region_parent:
            print(f'Region Parent: {r.id_region_parent}-{nom_region_parent}')


if __name__ == "__main__":
    options = ['1 - Importer toutes les régions', '2 Afficher toutes les régions de la base de données']
    opt=input("Sélectionner l'option 1 ou 2: ")
    if opt == '1':
        scraping()
    elif opt == '2':
        lister_regions()

