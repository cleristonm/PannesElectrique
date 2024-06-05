class Region:
    def __init__(self, id, nom, id_region_parent, lien, lien_meteo ):
        self.id = id
        self.nom = nom
        self.id_region_parent = id_region_parent
        self.lien = lien
        self.lien_meteo = lien_meteo

    def __str__(self):
        lien_text =  f'\nLien {self.lien}' if self.lien else '';
        lien_meteo_text = f'\nLien meteo {self.lien_meteo}' if self.lien_meteo else ''
        return f'Region id {self.id}: {self.nom}{lien_text}{lien_meteo_text}'
class Region_old:
    def __init__(self, region, lien, interruption, clients_prive, clients_total, id_region_parent, id=None ):
        self.region = region
        self.lien = lien
        self.interruption = interruption
        self.clients_prive = clients_prive
        self.clients_total = clients_total
        self.id_region_parent = id_region_parent
        self.id = id

    def __str__(self):
        return f'Region id {self.id}: {self.region} ({self.id_region_parent}) - Interruption {self.interruption} - Clients {self.clients_prive}/{self.clients_total} - Lien {self.lien}'