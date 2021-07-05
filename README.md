# immobilier

L'objectif est de réaliser un dashboard sur Tableau qui permet de faire un état des lieu du marché immobilier Parisien en 2020, selon les différents arrondissements et quartiers.

3 fichiers en input : 
 - full-2020.csv : DVF - contient toutes les mutations/transactions (fichier très lourd donc non deposé sur Github)
   Lien : https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres-geolocalisees/
 - laposte_hexasmal.csv : contient les correspondances entre les code_INSEE des communes et le nom des communes
   Lien : https://www.data.gouv.fr/en/datasets/base-officielle-des-codes-postaux/#
 - cadastre-75-sections.json : contient les sections cadastrales, ainsi que les coordonnées GPS qui les delimitent, du département 75
   Lien : https://cadastre.data.gouv.fr/datasets/cadastre-etalab

Script Python Immobilier.py :
Permet de transformer le fichier full-2020.csv pour créer une source de données propre qui servera d'input pour Tableau Public

Script Python Cadastre.py :
Permet le géocodage des sections cadastrales qui permettra une hierarchie géographique plus fine dans Tableau Public

Visualisation sur Tableau Public : https://public.tableau.com/app/profile/maxime.simon/viz/ImmobilierParis/Tableaudebord1
Disponible également via le fichier Immobilier Paris.twbx
