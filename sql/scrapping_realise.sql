select r.nom, p.interruption, p.clients_prive, p.clients_total, s.date_heure_debut, s.date_heure_fin from panne p
INNER JOIN REGION r on r.id = p.id_region
INNER JOIN scrapping s on s.id = p.id_scrapping
order by date_heure_debut