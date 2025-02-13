from dataclasses import dataclass
@dataclass
class Meteo:
    id: int
    id_region: int
    id_scrapping: int
    condition: str
    pression: float
    temperature: float
    point_de_rosee:float
    humidite: float
    vent_direction: str
    vent_velocite: float
    visibilite: float