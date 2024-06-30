from dataclasses import dataclass
@dataclass
class ScrappingQueue:
    def __init__(self, region, pannes_ajoutee, meteo_ajoutee, tentative  ):
        self.region = region
        self.pannes_ajoutee = pannes_ajoutee
        self.meteo_ajoutee = meteo_ajoutee
        self.tentative = tentative

