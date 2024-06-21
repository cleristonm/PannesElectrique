from modele.scrapping import Scrapping
import dao.mod_dao_connexion as dao_con
import datetime


def create_table():
    cde_ddl = '''create table if not exists scrapping(
            id integer primary key autoincrement,
            date_heure_debut text, date_heure_fin text
            )
            '''
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ddl)
    dao_con.fermer_connexion(conn)

def inserer_scrapping():
    # insertion dans la BD
    cde_ins = ('insert into scrapping(date_heure_debut) '
               'values(?)')
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ins, [datetime.datetime.now()])
    conn.commit()
    dao_con.fermer_connexion(conn)
    return curseur.lastrowid

def maj_scrapping(id):
    # insertion dans la BD
    cde_ins = ('update scrapping set date_heure_fin = ? where id = ?')
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ins, [datetime.datetime.now(), id])
    conn.commit()
    dao_con.fermer_connexion(conn)

def selectionner_scrapping():
    # Selection de la table
    requete = 'select  id, date_heure_debut, date_heure_fin from scrapping'
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete)
    scrappings = []
    # Parcours du curseur

    for rec in curseur:
        scrappings.append(Scrapping(rec[0], rec[1], rec[2]))
    dao_con.fermer_connexion(conn)
    return scrappings

