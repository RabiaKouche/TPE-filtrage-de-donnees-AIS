# connexion à la base de données navire
import connexionBD


def list_mmsi(ships_type):
    cBD = connexionBD.connection()
    curseur = cBD.cursor()

    if not curseur:
        print("connexion echouée ... ")

    curseur.execute("SELECT mmsi FROM navire where type_of_navire ='" + ships_type + "'")

    result = curseur.fetchone()
    table = []
    while result:
        if result[0] != '':
            table.append(result[0])

        result = curseur.fetchone()

    # Fermeture de la connexion
    cBD.close()
    return table
