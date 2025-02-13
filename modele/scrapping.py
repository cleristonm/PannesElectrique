class Scrapping:
    def __init__(self, id, date_heure_debut, date_heure_fin ):
        self.id = id
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin

    def __str__(self):
        return f'Scrapping id {self.id}: {self.date_heure_debut} - {self.date_heure_fin}'