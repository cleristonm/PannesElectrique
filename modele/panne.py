class Panne:
    def __init__(self, id, id_region, id_scrapping, interruption, clients_prive, clients_total ):
        self.id = id
        self.id_region = id_region
        self.id_scrapping = id_scrapping
        self.interruption = interruption
        self.clients_prive = clients_prive
        self.clients_total = clients_total


    def __str__(self):
        return f'Panne id {self.id}: Region {self.id_region} - Interruption {self.interruption} - Clients {self.clients_prive}/{self.clients_total}'