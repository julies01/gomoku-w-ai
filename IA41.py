import re
import sys
import random
import datetime

class Joueur:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
        self.pierres = 60 
        self.date_creation = datetime.datetime.now()  # timestemp de creation
    
    # Methode pour formater l'affichage
    def __str__(self):
        return f"{self.nom} ({self.couleur})"

class Case:
    def __init__(self, coordonnees):
        self.coordonnees = coordonnees  # tuple (x, y)
        self.etat = "inoccupee"  # "noir", "blanc", "inoccupee"
        
    # Verifie si la case est libre
    def est_libre(self):
        return self.etat == "inoccupee"

class Plateau:
    def __init__(self, taille=15):
        self.taille = taille
        self.cases = {}
        self.initialiser_plateau()
        
    def initialiser_plateau(self):
        for i in range(self.taille):
            for j in range(self.taille):
                self.cases[(i, j)] = Case((i, j))
    
    def afficher_plateau(self):
        print("\n  ", end="")
        for i in range(self.taille):
            print(f"{i:2}", end="")
        print()
        
        for i in range(self.taille):
            print(f"{i:2}", end="")
            for j in range(self.taille):
                case = self.cases[(i, j)]
                if case.etat == "noir":
                    print(" ●", end="")
                elif case.etat == "blanc":
                    print(" ○", end="")
                else:
                    print(" +", end="")
            print()
        print()

class ControleurJeu:
    def __init__(self, taille_plateau=15):
        self.plateau = Plateau(taille_plateau)
        self.joueurs = []
        self.joueur_actuel_index = 0
        self.configurer_joueurs()
    
    def configurer_joueurs(self):
        # Configure les joueurs au debut
        print("Configuration du Jeu de Gomoku")
        nom1 = input("Entrez le nom du joueur 1: ")
        nom2 = input("Entrez le nom du joueur 2: ")
        
        # Assignation des couleurs
        if random.random() > 0.5:
            self.joueurs.append(Joueur(nom1, "noir"))
            self.joueurs.append(Joueur(nom2, "blanc"))
        else:
            self.joueurs.append(Joueur(nom1, "blanc"))
            self.joueurs.append(Joueur(nom2, "noir"))
        
        print(f"\n{self.joueurs[0].nom} utilise les pierres {self.joueurs[0].couleur} ●")
        print(f"{self.joueurs[1].nom} utilise les pierres {self.joueurs[1].couleur} ○\n")
    
    def obtenir_joueur_actuel(self):
        return self.joueurs[self.joueur_actuel_index]
    
    def changer_joueur(self):
        self.joueur_actuel_index = 1 - self.joueur_actuel_index
    
    def valider_coordonnees(self, entree_utilisateur):
        pattern = r'^\((\d+),(\d+)\)$'
        correspondance = re.match(pattern, entree_utilisateur)
        
        if not correspondance:
            return None, "Erreur: Format invalide, utilisez (x,y)"
        
        try:
            x = int(correspondance.group(1))
            y = int(correspondance.group(2))
        except ValueError:
            return None, "Erreur: Les coordonnées doit être numeriques"
        
        if x < 0 or x >= self.plateau.taille or y < 0 or y >= self.plateau.taille:
            return None, f"Erreur: Coordonnées hors de limites (0-{self.plateau.taille-1})"
        
        return (x, y), None
    
    def case_est_occupee(self, coordonnees):
        return not self.plateau.cases[coordonnees].est_libre()
    
    def placer_pierre(self, coordonnees, couleur):
        case = self.plateau.cases[coordonnees]
        case.etat = couleur
    
    def verifier_victoire(self, coordonnees, couleur):
        x, y = coordonnees
        directions = [
            (1, 0),   # horizontal
            (0, 1),   # vertical  
            (1, 1),   # diagonal /
            (1, -1)   # diagonal \
        ]
        
        for dx, dy in directions:
            compteur = 1  # commence avec la pierre placee
            
            # Verification dans une direction
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if (nx, ny) in self.plateau.cases and self.plateau.cases[(nx, ny)].etat == couleur:
                    compteur += 1
                else:
                    break
            
            # Verification dans la direction oppose
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if (nx, ny) in self.plateau.cases and self.plateau.cases[(nx, ny)].etat == couleur:
                    compteur += 1
                else:
                    break
            
            ### Condition de victoire
            if compteur >= 5:
                return True
        
        return False
    
    def verifier_egalite(self):
        return all(joueur.pierres == 0 for joueur in self.joueurs)
    
    def abandonner_partie(self):
        joueur_actuel = self.obtenir_joueur_actuel()
        print(f"{joueur_actuel.nom} abandonne la partie!")
        self.changer_joueur()
        gagnant = self.obtenir_joueur_actuel()
        print(f"Vainqueur: {gagnant.nom}!")
        return "partie_terminee"
    
    def tour_joueur(self):
        joueur_actuel = self.obtenir_joueur_actuel()
        
        print(f"\n=== Tour de {joueur_actuel.nom} ({joueur_actuel.couleur}) ===")
        print(f"Pierres restantes: {joueur_actuel.pierres}")
        
        while True:
            entree = input("Coordonnées (x,y), 'quitter', 'abandonner': ").strip()
            
            if entree.lower() == 'quitter':
                print("Au revoir!")
                sys.exit()
            elif entree.lower() == 'abandonner':
                return self.abandonner_partie()
            
            coordonnees, erreur = self.valider_coordonnees(entree)
            if erreur:
                print(erreur)
                continue
            
            if self.case_est_occupee(coordonnees):
                print("Case occupee - choisissez une autre position")
                continue
            
            # Placement de la pierre
            self.placer_pierre(coordonnees, joueur_actuel.couleur)
            joueur_actuel.pierres -= 1
            
            # Affichage mise a jour
            self.plateau.afficher_plateau()
            
            ### Verification des conditions de fin
            if self.verifier_victoire(coordonnees, joueur_actuel.couleur):
                print(f"Felicitations! {joueur_actuel.nom} gagne!")
                return "partie_terminee"
            
            if self.verifier_egalite():
                print("Egalite! Plus de pierres disponible")
                return "partie_terminee"
            
            # Passage au joueur suivant
            self.changer_joueur()
            return "continuer"
    
    def demarrer_jeu(self):
        print("Jeu de Gomoku")
        print("Commandes disponible:")
        print("  (x,y) - placer une pierre")
        print("  abandonner - capituler")
        print("  quitter - quitter le jeu")
        
        self.plateau.afficher_plateau()
        
        while True:
            resultat = self.tour_joueur()
            
            if resultat == "partie_terminee":
                print("Merci d'avoir joue!")
                break

### Entree du programme
if __name__ == "__main__":
    # Configuration de la taille du plateau
    while True:
        try:
            taille = int(input("Taille du plateau (15 ou 19, defaut 15): ") or "15")
            if taille not in [15, 19]:
                print("Choix: 15 ou 19")
                continue
            break
        except ValueError:
            print("Veuillez entrer un nombre valide")
    
    jeu = ControleurJeu(taille)
    jeu.demarrer_jeu()