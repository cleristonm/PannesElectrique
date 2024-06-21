import sqlite3
def get_connexion():
    conn = sqlite3.connect('bdebPannesElectriques.dbf')
    return conn

def fermer_connexion(con):
    con.close()