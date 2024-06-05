import sqlite3
from modele.region import Region
import dao.mod_dao_connexion as dao_con

def create_table():
    cde_ddl = '''create table if not exists region(
            id integer primary key autoincrement,
            nom text, id_region_parent integer, lien text, lien_meteo text
            )
            '''
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ddl)
    dao_con.fermer_connexion(conn)

def inserer_region(r):
    # insertion dans la BD
    cde_ins = 'insert into region(nom, id_region_parent, lien, lien_meteo) values(?,?,?,?)'
    conn =  dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ins, [r.nom, r.id_region_parent, r.lien, r.lien_meteo])
    conn.commit()
    dao_con.fermer_connexion(conn)
    return curseur.lastrowid

def selectionner_regions():
    # Selection de la table
    requete = 'select id, nom, id_region_parent, lien, lien_meteo from region'
    conn =  dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete)
    regions = []
    # Parcours du curseur

    for rec in curseur:
        regions.append(Region(rec[0], rec[1], rec[2], rec[3], rec[4]))
    dao_con.fermer_connexion(conn)
    return regions

def selectionner_regions_avec_lien_meteo():
    # Selection de la table
    requete = "select id, nom, id_region_parent, lien, lien_meteo from region where lien_meteo  != ''"
    conn =  dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete)
    regions = []
    # Parcours du curseur

    for rec in curseur:
        regions.append(Region(rec[0], rec[1], rec[2], rec[3], rec[4]))
    dao_con.fermer_connexion(conn)
    return regions

def selectionner_nom_region_par_id(id):
    # Selection de la table
    requete = 'select nom  from region where id = ?'
    conn =  dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete, [id])
    row = curseur.fetchone()
    dao_con.fermer_connexion(conn)
    return (row[0] if row != None else '')




