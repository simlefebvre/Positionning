import obj

if __name__ == "__main__":
    mod = obj.model(6)
    print("Vous êtes à la page 0, il y a 5 pages")
    Continue = True
    page = 0
    while Continue:
        
        entre = input("Entrez le numéro de la page que vous voulez visiter (Q pour quitter, M pour afficher le model): ")
        if entre == "Q":
            Continue = False
            continue
        elif entre == "M":
            print(mod)
        else:
            try:
                entre = int(entre)
            except ValueError:
                print("Vous n'avez pas entré un nombre")
                continue
            if entre < 0 or entre > 5:
                print("Vous n'avez pas entré un nombre entre 0 et 5")
                continue
            mod.addMovement(page,entre)
            print("Vous êtes à la page ",entre)
            page = entre