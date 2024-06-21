from modele.meteo import Meteo
import dao.mod_dao_connexion as dao_con

def create_table():
    cde_ddl = '''create table if not exists meteo(
            id integer primary key autoincrement,
            id_region integer, id_scrapping integer, condition text, pression real, temperature real,
            point_de_rosee real, humidite real, vent_direction text,  vent_velocite real, 
            visibilite real
            )
            '''
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ddl)
    dao_con.fermer_connexion(conn)
def inserer_meteo(m):
    # insertion dans la BD
    cde_ins = ('insert into meteo(id_region, id_scrapping, condition, pression, temperature, '
               'point_de_rosee, humidite, vent_direction,  vent_velocite, visibilite) '
               'values(?,?,?,?,?,?,?,?,?,?)')
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ins, [m.id_region, m.id_scrapping, m.condition, m.pression, m.temperature,
                              m.point_de_rosee, m.humidite, m.vent_direction,  m.vent_velocite,
                              m.visibilite])
    conn.commit()
    dao_con.fermer_connexion(conn)
    return curseur.lastrowid

def selectionner_meteo():
    # Selection de la table
    requete = ('select id, id_region, id_scrapping, condition, pression, temperature, '
               'point_de_rosee, humidite, vent_direction,  vent_velocite, visibilite from meteo')
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete)
    meteos = []
    # Parcours du curseur

    for rec in curseur:
        meteos.append(Meteo(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10]))
    dao_con.fermer_connexion(conn)
    return meteos