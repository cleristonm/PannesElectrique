from modele.panne import Panne
import dao.mod_dao_connexion as dao_con

def create_table():
    cde_ddl = '''create table if not exists panne(
            id integer primary key autoincrement,
            id_region integer, id_scrapping integer, interruption integer, clients_prive integer, clients_total integer
            )
            '''
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ddl)
    dao_con.fermer_connexion(conn)



def inserer_panne(r):
    # insertion dans la BD
    cde_ins = ('insert into panne(id_region, id_scrapping, interruption, clients_prive, clients_total) '
               'values(?,?,?,?,?)')
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(cde_ins, [r.id_region, r.id_scrapping, r.interruption,
                              r.clients_prive, r.clients_total])
    conn.commit()
    dao_con.fermer_connexion(conn)
    return curseur.lastrowid

def selectionner_pannes():
    # Selection de la table
    requete = 'select id, id_region, id_scrapping, interruption, clients_prive, clients_total from panne'
    conn = dao_con.get_connexion()
    curseur = conn.cursor()
    curseur.execute(requete)
    pannes = []
    # Parcours du curseur

    for rec in curseur:
        pannes.append(Panne(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))
    dao_con.fermer_connexion(conn)
    return pannes

