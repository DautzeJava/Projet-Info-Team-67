import time


def menu_init():
    while True:
        print("\nMenu des options :")
        options = [
            "1 : Commencer une partie",
            "2 : Charger la dernière partie",
            "3 : Crédits",
            "4 : Quitter le jeu",
        ]
        for option in options:
            print(option)

        try:
            compris = int(input("Entrez l'option choisie : "))
        except ValueError:
            print("\nVeuillez entrer un chiffre valide (1 à 4).")
            time.sleep(1.2)
            continue

        if compris in (1, 2, 3, 4):
            return compris

        print("\nOption invalide : choisissez entre 1 et 4.")
        time.sleep(1)