import connexionBD


def ships_type():
    cBD = connexionBD.connection()
    curseur = cBD.cursor()

    if curseur:
        print("connexion réussie ... ")
    else:
        print("connexion echouée ... ")

    curseur.execute("SELECT type_of_navire FROM navire GROUP BY type_of_navire")

    result = curseur.fetchone()
    choices = []
    while result:
        if result[0] != '':
            choices.append(result[0])
            choices.append('----')

        result = curseur.fetchone()
    # Fermeture de la connexion
    cBD.close()
    return choices
