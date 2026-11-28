import time


def menu_init(initialize_game, clear, game_running=False):
    while True:
        clear()
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
            choix = int(input("Entrez l'option choisie : "))
        except ValueError:
            print("\nVeuillez entrer un chiffre valide (1 à 4).")
            time.sleep(1)
            continue

        if choix == 1:
            clear()
            return initialize_game()
        elif choix == 2:
            print("\nA dev")
            time.sleep(1)
        elif choix == 3:
            print("\nEquipe 67 : Félix Pastor et David Stefan Raducan")
            input("\nAppuyez sur Entrée pour revenir au menu...")
        elif choix == 4:
            clear()
            exit()
        else:
            print("\nOption invalide : choisissez entre 1 et 4.")
            time.sleep(1)


def menu_in_game(game_running, clear):
    while game_running:
        print("\nMenu des options :")
        options = [
            "1 : Construire/Détruire un bâtiment",
            "2 : Récolter une ressource",
            "3 : Informations",
            "4 : Terminer le tour",
            "5 : Sauvgarder et quitter",
            "6 : Quitter le jeu le jeu sans enregistrer",
        ]
        for option in options:
            print(option)

        try:
            choix = int(input("Entrez l'option choisie : "))
        except ValueError:
            print("\nVeuillez entrer un chiffre valide (1 à 6).")
            time.sleep(1)
            continue
                

        if choix == 1:
            print("\nA dev")
            time.sleep(1)
        elif choix == 2:
            print("\nA dev")
            time.sleep(1)
        elif choix == 3:
            print("\nA dev")
            time.sleep(1)
        elif choix == 4:
            print(f"\n vous passez au prochaine tour (tour [a modif])")
            time.sleep(1)
        elif choix == 5:
            clear()
            exit()
        elif choix == 6:
            clear()
            exit()
        else:
            print("\nOption invalide : choisissez entre 1 et 6.")
            time.sleep(1)
        break
