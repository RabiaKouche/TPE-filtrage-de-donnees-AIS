# fonction de filtration
# Connexion a la base de données bd_navire
# Attention, il faut que l'utilisateur soit le propriétaire de la base de données
# ou possède des droits suffisant
import glob
import csv
import mmsi_navire
import zone
import argparse
import time
import type_of_navire

parser = argparse.ArgumentParser(
    description='Ce programme filtre les données ais en fonction du type de navire et sa zone.')
parser.add_argument('latitude', type=float, help='latitude en degré')
parser.add_argument('longitude', type=float, help='longitude en degré')
parser.add_argument('width', type=float, help='latitude en degré')
parser.add_argument('ships_type', type=str, choices=type_of_navire.ships_type(), help='liste de type de navire')

args = parser.parse_args()


def filtre(latitude, longitude, width, ships_type):
    table = mmsi_navire.list_mmsi(ships_type)

    # recupération des 4 coordonnées long et lat
    liste = zone.boundingBox(latitude, longitude, width)
    lat_min = liste[0]
    long_min = liste[1]
    lat_max = liste[2]
    long_max = liste[3]

    # On liste l'ensemble des fichiers CSV présents dans le répertoire en supposant qu'ils sont au bon format
    tableau_ais = []

    for file in glob.glob("fichiers_csv/*.csv"):
        if file != "fichier_csv_filtre.csv":
            # print("Ajout de '{:45s}' à la liste des fichiers à traiter".format(file.replace(":", "/")))
            tableau_ais.append(file)

    file_name = "fichier_csv_filtre.csv"
    file = open(file_name, "w", newline="")
    for file_ais in tableau_ais:
        # Ouverture de fichier  en mode lecture
        fp = open(file_ais, 'r', newline='')
        # next(fp)
        # Pour chaque ligne lu dans le fichier, on la découpe
        for ligne in fp:
            # lignes = fp.readlines()
            infos = ligne.split(';')
            # print(table[infos[3]]+", je garde")
            if (infos[1] == '1') or (infos[1] == '2') or (infos[1] == '3'):
                # print(table)
                if infos[3] in table:  # si le mmsi du type de navire est dans ma table
                    long_a = float(infos[8].replace(",", ".") or 0.0)
                    lat_a = float(infos[9].replace(",", ".") or 0.0)
                    if (long_min <= long_a <= long_max) and (lat_min <= lat_a <= lat_max):
                        # writer = csv.writer(file, delimiter=';', quotechar=' ')
                        writer = csv.writer(file, delimiter=";", lineterminator='\n'.strip(), quotechar='"')
                        writer.writerow(infos)

        fp.close()


start_time = time.time()
if __name__ == '__main__':
    filtre(args.latitude, args.longitude, args.width, args.ships_type)

# Affichage du temps d'exécution
print("Temps d'exécution : {:5.4f} minutes".format((time.time() - start_time) / 60))
