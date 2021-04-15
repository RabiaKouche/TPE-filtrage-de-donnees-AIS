import psycopg2 as psycopg2


def connection():
    connexionBD = psycopg2.connect(
        host="localhost",  # Nom du serveur où se trouve la base de données
        database="bd_navire",  # Nom de la base de données contenant déjà la structure
        user="dev",  # Nom de l'utilisateur
        password="13041996"  # Mot de passe de l'utilisateur
    )
    return connexionBD
