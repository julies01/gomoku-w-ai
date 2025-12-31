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

## Analyse du problème
identification de sous-problèmes avec illustrations si possible <br>
méthode(s) de résolution de ces sous-problèmes avec illustrations de cas d'étude
## Méthode proposée
listing du programme commenté <br>
des améliorations envisageables de la méthode <br>
Description des variables d'états (informations) utilisées dans un état pour l'algorithme A* ou MinMax <br>
Description des machines à états finies implémentées <br>
Description de la hiérarchie de machines à états finies <br>
Attention : plusieurs représentations possibles des mêmes connaissances peuvent être utilisées dans un même programme en fonction des traitements associés




# Description détaillée d'une ou plusieurs situations traitées par notre programme

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

## Difficultés rencontrées
## Améliorations possibles
## Perspectives d'ouverture possible du sujet traité
## Annexe 
au moins deux prédicats que vous jugez essentiels, avec explication des termes requis pour chaque prédicat ?? adaptation pour python ?
