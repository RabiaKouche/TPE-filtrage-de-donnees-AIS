# fonction de filtrage
# Connexion a la base de données bd_navire
# Attention, il faut que l'utilisateur soit le propriétaire de la base de données
# ou possède des droits suffisant
import glob
import csv
import mmsi_navire
import zone
import time
import type_of_navire
import argparse

parser = argparse.ArgumentParser(
    description='Ce programme filtre les données ais en fonction du type de navire et sa zone géographique avec deux méthode differentes.')

parser.add_argument('ships_type', type=str, choices=type_of_navire.ships_type(), help='liste de type de navire')
parser.add_argument('-pp', '--points_poly', metavar='', type=str,
                    help='la liste des points avec le premier points c''est la latitude et la longitude, '
                         'Exemple : -pp="latitude,longitude x1,y1 x2,y2 x3,y3 ..."')
parser.add_argument('-w', '--width', metavar='', type=float, default=100, help='distance du rectangle')

args = parser.parse_args()


def filtre(ships_type, points_poly):
    tab = []
    points_poly = points_poly.split(' ')
    for i in points_poly:
        tab.append(i.split(','))

    points_poly = tab

    points_poly = [list(map(float, l)) for l in points_poly]

    table = mmsi_navire.list_mmsi(ships_type)

    # recupération des 4 coordonnées long et lat
    liste = zone.boundingBox(points_poly[0][0], points_poly[0][1], args.width)
    lat_min = liste[0]
    long_min = liste[1]
    lat_max = liste[2]
    long_max = liste[3]

    del points_poly[0]  # on peut supprimer le premier point car on en a pas besoin à partir de cette ligne

    # On liste l'ensemble des fichiers CSV présents dans le répertoire en supposant qu'ils sont au bon format
    tableau_ais = []

    for file in glob.glob("fichiers_csv/*.csv"):
        if file != "fichier_csv_filtre.csv":
            # print("Ajout de '{:45s}' à la liste des fichiers à traiter".format(file.replace(":", "/")))
            tableau_ais.append(file)

    file_name = "fichier_csv_filtre.csv"
    file = open(file_name, "w", newline="")
    writer = csv.writer(file, delimiter=";", lineterminator='\n'.strip(), quotechar='"')

    for file_ais in tableau_ais:
        # Ouverture de fichier  en mode lecture
        fp = open(file_ais, 'r', newline='')
        # Pour chaque ligne lu dans le fichier, on la découpe
        for ligne in fp:
            infos = ligne.split(';')
            # print(table[infos[3]]+", je garde")
            if (infos[1] == '1') or (infos[1] == '2') or (infos[1] == '3'):
                if infos[3] in table:  # si le mmsi du type de navire est dans ma table
                    long_a = float(infos[8].replace(",", ".") or 0.0)
                    lat_a = float(infos[9].replace(",", ".") or 0.0)
                    if len(points_poly) > 2:
                        if zone.point_interieur_du_polygon(lat_a, long_a, points_poly):
                            writer.writerow(infos)
                    else:
                        if (long_min <= long_a <= long_max) and (lat_min <= lat_a <= lat_max):
                            writer.writerow(infos)

        fp.close()


start_time = time.time()
if __name__ == '__main__':
    filtre(args.ships_type, args.points_poly)

# Affichage du temps d'exécution
print("Temps d'exécution : {:5.4f} minutes".format((time.time() - start_time) / 60))
