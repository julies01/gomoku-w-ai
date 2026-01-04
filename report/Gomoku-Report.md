# Rapport de projet Gomoku

## Présentation du jeu
Le Gomoku est un jeu de plateau abstrait d'origine chinoise qui se joue avec des pièces du jeu de Go (pièces noires et blanches). Le but du jeu est de placer ses pions de manière à former un alignement horizontal, vertical ou en diagonale de 5 pions. 

Le plateau est vide en début de partie. Tour à tour, les joueurs posent un de leurs pions sur une intersection libre. Une intersection est libre si elle ne contient pas déjà un pion. Dès qu’un joueur réalise une configuration gagnante, la partie s’arrête. Si les deux joueurs ont épuisé l’entierté de leurs pions et qu’aucun joueur n’a obtenu la configuration gagnante, la partie s’arrête sur un match nul.

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
Lors de la deuxième réunion, nous étions quatre membres du groupe. Nous avons tout d'abord joué tous ensemble au Gomoku pour que tout le monde soit bien au point du jeu, des règles, des stratégies pour gagner. Nous avons aussi partagé des idées quand à la manière de vérifier qu'un joueur avait posé la pièce manquante. Nous avons réfléchi à l'algorithme des plus proches voisins qui serait adopté pour une vérification plus optimisée au lieu de scanner chaque diagonale, chaque verticale, chaque horizontale du plateau. Nous avons décidé de procéder à la partie IA en faisant des recherches chacun de notre côté.


**3ème réunion (17/11/2025) :**
Avec les différents ponts et jours fériés en octobre + les vacances nous avons passé beaucoup de temps sans nous réunir. Pendant ce temps nous avons tous cherché des algorithmes, fait des recherches sur ce qui existe déjà et les bonnes pratiques. Chacun a présenté son travail pendant une dizaine de minutes. Nous avons présenter nos fonctions d'évaluation, nos algorithmes et leur fonctionnement en détail grâce à des schémas. Nous en sommes arrivés à la conclusion que l'algorithme Alpha-Beta avec élagage est l'algorithme qui convient le meiux à notre programme.

**4ème réunion (17/11/2025) :**
Réunion finale consacrée à l'organisation à avoir pendant les vacances pour respecter les échéances, et finir les derniers ajustement du code et la rédaction de ce rapport.



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
* **`depth`** : Profondeur de recherche actuelle (définie à `level` dans le code).
* **`alpha` & `beta`** : Bornes utilisées pour l'élagage.
* **`transposition_table`** : Dictionnaire utilisé pour la Mémorisation. Il stocke les configurations de plateau déjà analysées (signature, score, profondeur) pour éviter les recalculs inutiles. Pour cela, on mets le plateau sous la forme d'un tuple.
* **`relevant_moves`** : Liste générée dynamiquement à chaque étape (via `get_relevant_moves`) qui ne contient que les cases vides adjacentes à des pions existants. Cela réduit drastiquement le nombre de branche recherchées.

#### Description des machines à états finies (FSM)

Dans `Game.py`, le flux du programme est géré à l’aide d’une machine à états finie (FSM) implémentée au-dessus de **Tkinter**.  
Il ne s’agit pas d’une FSM explicite avec une pile personnalisée, mais d’une **gestion implicite des états**, reposant sur :
- la destruction et la création dynamique des widgets (`clear_window`),
- les callbacks Tkinter (`command=...`),
- la boucle d’événements principale (`mainloop`).

Chaque écran correspond à un **état logique**, et les transitions sont déclenchées par les interactions de l’utilisateur.

### États principaux de la FSM

1. **MENU**  
   État initial de l’application, affiché par la fonction `show_menu`.  
   Il présente les actions principales :
   - lancer une partie,
   - accéder aux options,
   - quitter le jeu.  

   Le passage vers un autre état s’effectue via des callbacks de boutons, par exemple :
   - `show_options`
   - `ask_rules_before_play`

2. **ASK_RULES**  
   État intermédiaire affiché avant le lancement du jeu.  
   Il demande à l’utilisateur s’il souhaite consulter les règles.  
   Selon la réponse :
   - transition vers **RULES**,
   - ou transition directe vers **PLAY**.

3. **RULES**  
   État d’affichage statique des règles du Gomoku.  
   Aucune logique de jeu n’est exécutée.  
   Cet état agit comme une **couche temporaire**, depuis laquelle l’utilisateur peut :
   - revenir au **MENU**,
   - ou lancer la partie (**PLAY**).

4. **OPTIONS**  
   L’état **OPTIONS** permet la configuration complète du jeu :
   - mode de jeu (PvAI, PvP, AIvAI),
   - niveau des IA,
   - taille du plateau,
   - nombre de manches (`Best of`).  

   Les modifications sont appliquées immédiatement via des callbacks, puis l’utilisateur peut revenir au **MENU**.

5. **PLAY**  
   L’état **PLAY** correspond à la phase de jeu active.  
   Il est initialisé par `show_game` et repose sur :
   - la création dynamique de frames Tkinter,
   - l’intégration du module `GomokuGUI`,
   - les callbacks `update_stones` et `update_scores`.  

   Le jeu reste dans cet état jusqu’à la fin d’une manche ou d’une série de manches.

6. **GAME OVER / END BEST OF**  
   Il ne s’agit pas d’un état graphique séparé, mais d’un **état logique** déclenché par `update_scores`.  
   Lorsque le nombre de victoires requis est atteint :
   - les scores sont réinitialisés,
   - une transition automatique vers **MENU** est effectuée.

### Gestion implicite des états et “stack” Tkinter

La gestion des états ne repose pas sur une pile explicite, mais sur le **modèle événementiel de Tkinter**, qui agit comme un **stack implicite d’écrans** :

- chaque transition détruit l’état courant via `clear_window`,
- un nouvel état est ensuite créé et affiché,
- les callbacks conservent le contexte logique (variables de la classe `Game`).


## Description détaillée d'une ou plusieurs situations traitées par notre programme

## Situation 1 : Gestion d'un cas d'urgence

**Problème :** si l'adversaire a aligné 4 pions avec une case vide au bout, et que l'ia ne le bloque pas, elle perd au prochain tour. Cela signifie qu'il est essentiel que l'ia place son pion a cet endroit. Inversement, si l'ia a aligné 4 pions et que c'est a son tour de jouer, elle n'a pas a calculer plusieurs coup a l'avance pour rien.



C'est pourquoi avant le lancement de l'algorithme alpha-beta on verifie le plateau actuel en lançant `find_immediate_threat` avec sa propre couleur, afin de vérifier si une potentiel victoire est possible.

La fonction `find_immediate_threat` fonctionne ainsi :
* Elle récupère les coups potentiellements gagnant (les cases vides adjacentes)
* Elle simule la pose d'un pion sur chaque case candidates
* Elle appelle `check_win_move` qui regarde si cela crée un alignement de 5.

Apres cela, on vérifie `find_immediate_threat` avec la couleur adverse.

Dans le cas ou une condition de victoire ou de défaite et trouvée, on ne lance pas l'algorithme alpha-beta et on retourne les coordonnées du coup gagnant ou permettant d'éviter la défaite.


## Situation 2 : Optimisation de la recherche

Dans le cas ou aucune menace n'est détectée, l'ia doit choisir efficacement le meilleur placement pour avoir le plus de chance de victoire.

**Problème :** Il y a un trop grand nombre de possibilité (environ 200 cases vides). Calculer tout les scénarios serait beacoup trop long, et en augmentant la profondeur cela augmente exponentiellement.

1. C'est pourquoi le programme fait une pré selection des movements intéressant. L'ia utilise la fonction `get_relevant_move` pour ne prendre en compte que les movement adjacents à des pions déjà existants. Cela permet d'ignorer la majeure partie du plateau remplie de cases vide.
2. Ensuite l'ia descend dans l'arbre des possibilités : si l'ia joue a un certain endroit, alors le joueur a beaucoup de chance de jouer ici, etc...
3. Elle utilise l'élagage afin de diminuer le nombre de branche a explorer, par exemple, si l'ia trouve une branche qui lui donne a la fin 100 points, et que dans une autre branche elle voit que l'adversaire peut réduire le score à 50, il n'y a pas grand intérêt a continuer de chercher dans cette branche.
4. Avant de calculer, on vérifie si la configuration du plateau a déjà été calculée auparavant pour avoir un gain de temps.


## Résultat obtenus sur notre programme sur ces situations

* **Fonctionnalité** : Les modes PvAI, PvP et AIvAI sont fonctionnels.
* **Intelligence** :
    * **Level 1** : Réponse rapide, reconnaissance des alignements simples.
    * **Level 3** : Recherche plus profonde, défense solide contre les attaques complexes et exploitation des erreurs adverses.
* **Efficacité** : Grâce à l'optimisation combinée de l'élagage Alpha-Bêta, de la recherche locale (Window Search) et de la Table de Transposition, le temps de réponse reste convenable, même avec une profondeur de 3. L'IA est capable de detecter les menaces immédiates instantanément grâce à sa fonction dédiée.

## Difficultés rencontrées

1.  **Mapping des coordonnées**
    * L'implémentation initiale posait les pions au centre des cases. Après vérification des règles, nous avons corrigé pour viser les intersections.
    * **Solution** : Modification de `GomokuGUI` avec une variable `margin` et ajustement de la formule : `col = int(round((event.x - margin) / spacing))`.

2.  **Équilibrage des poids (Heuristique)**
    * Difficulté à déterminer le ratio attaque/défense. Faut-il bloquer un "quatre" adverse ou construire son "trois" ?
    * **Solution** : Hiérarchie stricte par ordres de grandeur : **Mon 5 > Son 5 (Défense) > Mon 4 > Son 4**.

3. **Gestion de l'espace de recherche**
   * Nous avons tenté de maintenir des tableau d'adjacence (`aroundtables`) mis à jour en temps réel. Cependant cette approche s'est révélée trop complexe lors de la recursion.
   * Nous avons donc opté pour une génération dynamique des coups (`get_relevant_moves), qui semble finalement assez performante.

## Améliorations possibles

1.  **Fonction Annuler (Undo)**
    * Implémentable via une pile `history` dans la classe `Board` (push à chaque coup, pop pour annuler).

2.  **Table de transposition**
    * Actuellement la clé de notre table de transposition est un tuple complet du plateau. En utilisant le hachage zobrist, il serait possible de calculer la clé unique du plateau plus rapidement ce qui permettrait un gain de temps conséquent.

3.  **Algorithme VCF (Victory by Continuous Fours)**
    * Ajouter un module de recherche spécialisé pour trouver les chemins de victoire par "quatre" consécutifs, plus efficace que Minimax en fin de partie.

## Perspectives d'ouverture possible du sujet traité

* **Machine Learning** : Remplacer la fonction d'évaluation heuristique par un Réseau de Neurones Convolutif (CNN) entraîné, pour une intuition de jeu plus naturelle.
* **Jeu en réseau** : Utilisation des `sockets` Python pour permettre le jeu à distance (LAN/Internet).
  
## Annexe 
au moins deux prédicats que vous jugez essentiels, avec explication des termes requis pour chaque prédicat ?? adaptation pour python ?
