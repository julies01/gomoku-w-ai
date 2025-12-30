# Rapport de projet Gomoku

## Présentation du jeu
Le Gomoku est un jeu de plateau abstrait d'origine chinoise qui se joue avec des pièces du jeu de Go (pièces noires et blanches). Le but du jeu est de placer ses pions de manière à former un alignement horizontal, vertical ou en diagonale de 5 pions. 

Le plateau est vide en début de partie. Tour à tour, les joueurs posent un de leurs pions sur une intersection libre. Une intersection est libre si elle ne contient pas déjà un pion. Dès qu’un joueur réalise une configuration gagnante, la partie s’arrête. Si les deux joueurs ont épuisé l’entierté de leurs pions et qu’aucun joueur n’a obtenu la configuration gagante, la partie s’arrête sur un match nul.

## Énoncé du problème

Le Gomoku est un jeu m,n,k 

Qu'est ce qu'un jeu m,n,k ? 

Un jeu de société abstrait dans lequel deux joueurs placent à tour de rôle une pierre de leur couleur sur un plateau m x n. Le gagnant est le joueur qui parvient le premier à aligner k pierres de sa couleur, horizontalement, verticalement ou en diagonale.

Le Gomoku est : 
- un jeu à deux joueurs 
- un jeu à somme nulle : jeux dans lesquels la somme « algébrique » des gains des joueurs est constante. Ce que gagne un joueur est nécessairement perdu par l'autre. 
- un jeu à information complète et parfaite : chaque joueur dispose de connaissances exhaustives lorsqu'il prend des décisions. 
  Le joueur connaît : 
  • ses propres actions possibles ; 
  • les actions possibles des autres joueurs ; 
  • les gains résultant de ces actions ; 
  • les motivations des autres joueurs. <br><br>
  
  Information parfaite : mécanisme séquentiel dans lequel chaque joueur dispose d'informations détaillées sur toutes les actions effectuées avant de faire son propre choix. Ces jeux sont également appelés asynchrones ou alternés, car les joueurs prennent leurs décisions les uns après les autres, en disposant d'informations sur les coups de leurs adversaires.

Pour notre IA le but est de déterminer une séquence de coups gagnants pour atteindre une position finale, à l'aide d'algorithmes basés sur l'exploration d'un arbre de jeu.l’IA doit essayer de gagner en alignant ses pions mais doit aussi bloquer les potentielles actions du joueur adverse.


## Organisation et déroulement du projet
Nous avons décidé d'organiser des réunions régulièrement avec le groupe pour avancer le projet tout au long des douze semaines. 

**1ère réunion (06/10/2025) :** 
À ce moment là, nous n'étions que deux membres. Nous décidé d'implémenter d'abord le jeu sans IA. Nous avons réfléchi à quel paradigme de programmation utiliser et nous avons décidé d'utiliser la Programmation Orientée Objet. _Expliquer pourquoi on l'a utilisée_. Nous avons créé un onglet "Architecture of our project" sur le Wiki de notre dépôt Github. Dans celui-ci nous avons précisé les composants du programme : Joueur, Plateau, Case

_Photo, capture d'écran_ ?

**2ème réunion (19/10/2025) :**
Lors de la deuxième réunion, nous étions quatre membres du groupe. Nous avaons toout d'abord joué tous ensemble au Gomoku pour que tout le monde soit bien au point du jeu, des règles, des stratégies pour gagner. Nous avons aussi partagé des idées quand à la manière de vérifier qu'un joueur avait posé la pièce manquante. Nous avons réfléchi à l'algorithme des plus proches voisins qui serait adopté pour une vérification plus optimisée au lieu de scanner chaque diagonale, chaque verticale, chaque horizontale du plateau. Nous avons décidé de procéder à la partie IA en faisant des recherches chacun de notre côté.


**3ème réunion (17/11/2025) :**
Avec les différents ponts et jours fériés en octobre + les vacances nous avons passé beaucoup de temps sans nous réunir. Pendant ce temps nous avons tous cherché des algorithmes, fait des recherches sur ce qui existe déjà et les bonnes pratiques. Chacun a présenter son travail pendant une dizaine de minutes. Nous avons présenter nos fonctions d'évaluation, nos algorithmes et leur fonctionnement en détail grâce à des schémas. Nous en sommes arrivés à la conclusion que l'algorithme Alpha-Beta avec élagage est l'algorithme qui convient le meiux à notre programme.

**4ème réunion (17/11/2025) :**




## Formalisation du problème

Pour que l'ordinateur puisse résoudre le problème du Gomoku, nous avons traduit les règles du jeu en un modèle mathématique et une représentation d'espace d'états :

1.  **Espace d'états (State Space)**
    * Le plateau est représenté par une matrice 2D de $15 \times 15$ (correspondant à `Board.grid` dans le code).
    * L'ensemble des états pour chaque coordonnée $(r, c)$ est $\{ \text{None}, \text{Black}, \text{White} \}$.
    * L'état initial est un plateau entièrement vide.

2.  **Actions**
    * Le joueur $P$, à son tour, peut placer un pion sur n'importe quelle position $(r, c)$ satisfaisant la condition `board.grid[r][c].state == None`.

3.  **Modèle de transition (Transition Model)**
    * $Result(S, a)$ : Exécuter l'action $a$ (poser un pion) dans l'état actuel $S$ entraîne la mise à jour de l'état de cette position à la couleur du joueur actuel, et le contrôle passe à l'adversaire (correspondant au code `Board.place_stone` et `switch_player`).

4.  **Test terminal (Terminal Test)**
    * **Victoire** : 5 pions de la même couleur alignés consécutivement sur n'importe quelle ligne, colonne ou diagonale (code `check_win`).
    * **Match nul** : Le plateau est plein et personne n'a gagné.

5.  **Fonction d'utilité (Utility Function)**
    * Pour l'IA (joueur Max), la victoire attribue un score très élevé (ex: $+10,000,000$).
    * Pour l'adversaire (joueur Min), la victoire attribue un score très bas (ex: $-10,000,000$).
    * Les états non terminaux sont évalués via la fonction heuristique `evaluate_board`.

## Analyse du problème

### Identification de sous-problèmes
Nous avons identifié plusieurs sous-problèmes clés :

1.  **Explosion combinatoire de l'espace de recherche**
    * **Analyse** : Le facteur de branchement (Branching Factor) du Gomoku est énorme, avec 225 choix au premier coup. Une recherche exhaustive est impossible.
    * **Solution** : Utilisation de l'élagage Alpha-Bêta et restriction heuristique de la zone de recherche.

2.  **Évaluation statique des positions**
    * **Analyse** : Avec une profondeur de recherche limitée, l'IA doit juger de la qualité d'une position immédiate.
    * **Solution** : Conception d'une fonction d'évaluation identifiant les motifs comme "Quatre vivant", "Trois vivant" et leur attribuant des poids.

3.  **Correspondance Interface Graphique / Coordonnées Logiques**
    * **Analyse** : Le clic en pixels $(x, y)$ sur l'écran doit être converti précisément en indice de matrice $(row, col)$, tout en respectant la règle des intersections.

### Méthode proposée

#### Listing du programme commenté
Nous avons adopté la Programmation Orientée Objet (POO). Le système est constitué des classes suivantes :
* **`Board`** : Gère la structure de données `grid`, l'historique des coups et la vérification de victoire.
* **`Cell`** : Objet représentant une intersection unique sur le plateau.
* **`AI`** : L'agent intelligent central.
    * Contient `evaluate_board` : Système de notation basé sur les alignements de pions.
    * Contient `get_best_move` : Arbre de décision basé sur l'algorithme Minimax avec élagage Alpha-Bêta.
* **`GomokuGUI`** : Implémenté avec `tkinter`, gère le rendu de la grille, les événements souris et l'ordonnancement de l'IA.

#### Description des variables d'états
Dans l'algorithme de l'IA, les variables d'état clés suivantes sont utilisées :
* **`depth`** : Profondeur de recherche actuelle (définie à `2 * level` dans le code).
* **`alpha` & `beta`** : Bornes utilisées pour l'élagage.
* **`white_around` / `black_around`** (Optimisation majeure) :
    * Ce sont deux tableaux auxiliaires de $15 \times 15$ maintenus dans la classe `AI`.
    * **Rôle** : Enregistrer quelles cases vides ont des pions adjacents. Lors de la génération des coups candidats, l'IA ne considère que ces "zones actives", réduisant le facteur de branchement de 225 à environ 20-30.

#### Description des machines à états finies (FSM)
Dans `Game.py`, une machine à états de haut niveau gère le flux du programme :
1.  **MENU** : Menu principal, attente du choix de mode.
2.  **OPTIONS** : Configuration (`AI Level`, `Board Size`).
3.  **PLAY** : Boucle de jeu (`wait_for_click` -> `update_board` -> `check_win` -> `switch_player`).
4.  **GAME_OVER** : Affichage du vainqueur et retour au menu.

## Description détaillée d'une ou plusieurs situations traitées par notre programme

**Scénario : L'IA défend contre un "Trois Vivant"**

* **Situation** : L'IA joue les Noirs (2ème joueur). Les Blancs ont formé un "trois vivant" au centre (trois pions consécutifs, extrémités vides). Sans blocage, les Blancs formeront un "quatre vivant" au prochain coup et gagneront.
* **Traitement** :
    1.  Appel de la fonction `get_best_move`.
    2.  Le programme consulte `white_around` et identifie les extrémités du "trois" comme candidats prioritaires.
    3.  **Simulation** :
        * Si l'IA simule un coup ailleurs, la récursion descend au niveau suivant (tour des Blancs).
        * Les Blancs détectent une victoire imminente (4 puis 5 pions). `evaluate_board` retourne un score très bas (défaite).
        * L'algorithme Alpha-Bêta coupe ces branches.
    4.  **Défense** :
        * L'IA simule un coup à une extrémité du "trois" (blocage).
        * Au niveau suivant, l'offensive blanche est brisée. Le score, bien que passif, est nettement supérieur à une défaite.
* **Résultat** : L'IA choisit le blocage.

## Résultat obtenus sur notre programme sur ces situations

* **Fonctionnalité** : Les modes PvAI, PvP et AIvAI sont fonctionnels.
* **Intelligence** :
    * **Level 1** : Réponse rapide, reconnaissance des alignements simples.
    * **Level 3** : Recherche plus profonde, défense solide contre les attaques complexes et exploitation des erreurs adverses.
* **Efficacité** : Grâce à l'optimisation des tables `around`, le temps de réponse initial est très rapide (<0.5s). Sur un plateau encombré avec une profondeur élevée, le temps monte à 1-2s, ce qui reste acceptable.

## Difficultés rencontrées

1.  **Mapping des coordonnées**
    * L'implémentation initiale posait les pions au centre des cases. Après vérification des règles, nous avons corrigé pour viser les intersections.
    * **Solution** : Modification de `GomokuGUI` avec une variable `margin` et ajustement de la formule : `col = int(round((event.x - margin) / spacing))`.

2.  **Équilibrage des poids (Heuristique)**
    * Difficulté à déterminer le ratio attaque/défense. Faut-il bloquer un "quatre" adverse ou construire son "trois" ?
    * **Solution** : Hiérarchie stricte par ordres de grandeur : **Mon 5 > Son 5 (Défense) > Mon 4 > Son 4**.

## Améliorations possibles

1.  **Fonction Annuler (Undo)**
    * Implémentable via une pile `history` dans la classe `Board` (push à chaque coup, pop pour annuler).

2.  **Table de transposition**
    * Utilisation du Hachage Zobrist pour mettre en cache les configurations de plateau déjà calculées et éviter le recalcul.

3.  **Algorithme VCF (Victory by Continuous Fours)**
    * Ajouter un module de recherche spécialisé pour trouver les chemins de victoire par "quatre" consécutifs, plus efficace que Minimax en fin de partie.

## Perspectives d'ouverture possible du sujet traité

* **Machine Learning** : Remplacer la fonction d'évaluation heuristique par un Réseau de Neurones Convolutif (CNN) entraîné, pour une intuition de jeu plus naturelle.
* **Jeu en réseau** : Utilisation des `sockets` Python pour permettre le jeu à distance (LAN/Internet).
  
## Annexe 
au moins deux prédicats que vous jugez essentiels, avec explication des termes requis pour chaque prédicat ?? adaptation pour python ?
