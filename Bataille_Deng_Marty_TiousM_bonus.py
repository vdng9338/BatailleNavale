import random

# Une classe Bateau qui simplifie le code de la partie.
# Pour cette version bonus, un bateau peut faire une case (dans ce cas-là les
# deux coordonnées sont les mêmes) ou deux cases.
class Bateau:
  def __init__(self, lig1, col1, lig2, col2):
    self._lig1 = lig1
    self._col1 = col1
    self._lig2 = lig2
    self._col2 = col2
    self._coule = False
    
  # Accesseurs des coordonnées
  def getLigne1(self):
    return self._lig1
    
  def getColonne1(self):
    return self._col1
    
  def getLigne2(self):
    return self._lig2
    
  def getColonne2(self):
    return self._col2
    
    

  # Accesseurs et mutateurs pour le champ "coulé"
  def estCoule(self):
    return self._coule
    
  def couler(self):
    self._coule = True

  
  # Cette méthode renvoie True si la case donnée est une des cases de ce bateau, False sinon.
  def intersecteCase(self, lig, col):
    return (self.getLigne1() == lig and self.getColonne1() == col) or (self.getLigne2() == lig and self.getColonne2() == col)

  # Cette méthode renvoie True si ce bateau et le bateau passé en paramètre partagent au
  # moins une case en commun. Elle permet d'éviter de mettre deux bateaux au même endroit lors
  # de la génération aléatoire.
  # Le fait de ne pas avoir utilisé des listes de 2 pour la ligne et la colonne rend le code
  # un peu répétitif...
  def intersecte(self, autreBateau):
    if self.getLigne1() == autreBateau.getLigne1() and self.getColonne1() == autreBateau.getColonne1():
      return True
    elif self.getLigne1() == autreBateau.getLigne2() and self.getColonne1() == autreBateau.getColonne2():
      return True
    elif self.getLigne2() == autreBateau.getLigne1() and self.getColonne2() == autreBateau.getColonne1():
      return True
    elif self.getLigne2() == autreBateau.getLigne2() and self.getColonne2() == autreBateau.getColonne2():
      return True
    else:
      return False
    
  # Renvoie True si la case passée en paramètre n'est pas une des cases du bateau mais est à
  # la même colonne ou la même ligne qu'une des cases du bateau.
  def estEnVue(self, lig, col):
    if self.intersecteCase(lig, col):
      return False
    else:
      return self.getLigne1() == lig or self.getLigne2() == lig or self.getColonne1() == col or self.getColonne2() == col
      
      
      
# Une classe Joueur qui stocke le nom du joueur et son total de points.
class Joueur:
  def __init__(self, nom, nbPoints):
    self._nom = nom
    self._nbPoints = nbPoints
    
  def getNom(self):
    return self._nom
    
  def getNbPoints(self):
    return self._nbPoints
    
  def ajouterPoints(self, nbPointsAjout):
    self._nbPoints = self._nbPoints + nbPointsAjout
  
  # Affichage simplifié du joueur.
  def __str__(self):
    return "Le joueur " + self._nom + " a " + str(self._nbPoints) + " points"


# Retourne True si le bateau passé en paramètre n'est pas None et ne partage de case
# avec aucun autre bateau de la liste passée en paramètre, False sinon.
def bateauInserableDansListe(liste, bateauAutre):
  if bateauAutre == None:
    return False
  for bateau in liste:
    if bateau.intersecte(bateauAutre):
      return False
  return True

# Retourne _le_ bateau de la liste en paramètre présent à une certaine case passée en
# paramètre, None s'il n'y en a aucun.
def chercherBateauDansListe(liste, lig, col):
  for bateau in liste:
    if bateau.intersecteCase(lig, col):
      return bateau
  return None
    
# Retourne les bateaux de la liste en paramètre en vue pour la case en paramètre.
# N'inclut pas l'éventuel bateau dont une des cases est celle passée en paramètre.
def chercherBateauxEnVue(liste, lig, col):
  bateaux = []
  for bateau in liste:
    if bateau.estEnVue(lig, col):
      bateaux.append(bateau)
  return bateaux

# Affichage basique de la grille, avec éventuellement un coup.
# Par défaut cette fonction n'est jamais appelée.
# Légende :
# . : rien                B : bateau
# X : bateau coulé        ! : coup (remplace le bateau le cas échéant)
def afficherGrille(bateaux, tailleGrille, ligneCoup=None, colonneCoup=None):
  for ligne in range(tailleGrille):
    for colonne in range(tailleGrille):
      bateau = chercherBateauDansListe(bateaux, ligne, colonne)
      if ligneCoup == ligne and colonneCoup == colonne:
        print("!", end="")
      elif bateau == None:
        print(".", end="")
      elif bateau.estCoule():
        print("X", end="")
      else:
        print("B", end="")
    print()
  print()

# Procédure qui effectue une partie aléatoire avec nbBateaux bateaux et une grille
# carée de tailleGrille x tailleGrille. Renvoie le nombre de points total.
# Risque de boucler indéfiniment dans les deux cas suivants :
# 1 - On a une grille 1x1 (impossible de réaliser trois coups).
# 2 - La grille des bateaux est complètement remplie, mais tous les bateaux n'ont
#     pas encore été générés. (Dans le cas où il reste très peu de cases libres
#     la génération aléatoire peut prendre assez longtemps, le temps de retomber
#     sur une case libre.)
# A détecter.
def partieAleatoire(nbBateaux, tailleGrille):
  # Liste des bateaux
  bateaux = []
  for iBateau in range(nbBateaux):
    bateau = None
    # Tant que le bateau sélectionné est en conflit avec un autre, on crée un bateau au hasard
    while not bateauInserableDansListe(bateaux, bateau):
      # Coordonnées aléatoires
      haut = random.randint(0, tailleGrille-1)
      gauche = random.randint(0, tailleGrille-1)
      # Un nombre entre 1 et 3. Si ce nombre est 1, alors le bateau aura 2
      # cases, sinon il n'en aura qu'une. Donc un peu moins d'un tiers de
      # bateaux à 2 cases.
      etendre = random.randint(1, 3) <= 1
      if etendre:
        direction = random.randint(1,2)
        if direction == 1: # DROITE : seulement s'il y a de la place
          if gauche < tailleGrille-1:
            bateau = Bateau(haut, gauche, haut, gauche+1)
          else:
            bateau = Bateau(haut, gauche, haut, gauche)
        elif direction == 2: # BAS : seulement s'il y a de la place
          if haut < tailleGrille-1:
            bateau = Bateau(haut, gauche, haut+1, gauche)
          else:
            bateau = Bateau(haut, gauche, haut, gauche)
      else:
        bateau = Bateau(haut, gauche, haut, gauche)
    bateaux.append(bateau)
  
  
  # Liste d'essais déjà effectués
  essais = []
  points = 0
  for iEssai in range(3):
    # Coup aléatoire (on ne tape pas une case plus d'une fois)
    case = None
    while case == None or case in essais:
        case = [random.randint(0,tailleGrille-1), random.randint(0,tailleGrille-1)]
    essais.append(case)
    bateauMemeCase = chercherBateauDansListe(bateaux, case[0], case[1])
    bateauxEnVue = chercherBateauxEnVue(bateaux, case[0], case[1])
    if bateauMemeCase != None and not bateauMemeCase.estCoule(): # Si on a coulé un bateau...
      bateauMemeCase.couler()
      points = points + 8
    for bateau in bateauxEnVue:
      if not bateau.estCoule():
        points = points + 1
  
  return points
  
def partiejouer(nbBateauxpartie ,tailleGrillepartie):
  # Liste des bateaux
  
  print("""Ici, vous jouez une partie contre l'ordinateur avec les règles suivante:
 - vous ne placez pas de bateaux, vous tenter simplement d'en couler 6.
 - vous entrer les coordonnées à frapper que vous ne pourrez pas frapper à nouveau plus tard.
 - vous avez une limite de 10 coups à tirer, soyez stratégique .
 """)
  
  bateaux = []
  for iBateau in range(nbBateauxpartie):
    bateau = None
    while not bateauInserableDansListe(bateaux, bateau):
      # Coordonnées des batau 
      haut = random.randint(1, tailleGrillepartie) ## Les bateaux sopnt placés aléatoirement dans la grille
      gauche = random.randint(1, tailleGrillepartie) 
      bateau = Bateau(haut, gauche, haut, gauche)
    bateaux.append(bateau)
  
  essaisjoueur = []
  pointsjoueur = 0
  for iEssai in range(10):
    # Coup (on ne tape pas une case plus d'une fois)
    casefrappe = None
    while casefrappe == None or casefrappe in essaisjoueur:
        if casefrappe != None:
          print("Vous avez déjà frappé cette case auparavant.")
        verif_entree_gauche = 1 ## Attention à l'indentation...
        while verif_entree_gauche == 1: # Tant que le nombre entré est invalide
          try:
            casefrappegauche = input("Quelle case voulez vous frapper ?  \n abcisse (de 1 à "+str( tailleGrillepartie)+") : ")
            int(casefrappegauche)
            verif_entree_gauche = 0
          except:
            print("/!\ Veuillez entrer un nombre entier.")
        casefrappegauche = int(casefrappegauche)
        
        verif_entree_haut = 1
        while verif_entree_haut == 1:
          casefrappehaut = input(" ordonnée (de 1 à "+str(tailleGrillepartie)+") : ")
          try:
            int(casefrappehaut)
            verif_entree_haut = 0
          except:
            print("/!\ Veuillez entrer un nombre entier.")
          casefrappehaut = int(casefrappehaut)
        casefrappe = (casefrappehaut, casefrappegauche)
    essaisjoueur.append(casefrappe)
    bateauMemeCase = chercherBateauDansListe(bateaux, casefrappe[0], casefrappe[1])
    bateauxEnVue = chercherBateauxEnVue(bateaux, casefrappe[0], casefrappe[1])
    if bateauMemeCase != None and not bateauMemeCase.estCoule(): # Si on a coulé un bateau...
      bateauMemeCase.couler()
      pointsjoueur += 8
      print("Vous avez coulé un bateau !")
    nbBateauxEnVue = 0
    for bateau in bateauxEnVue:
      if not bateau.estCoule():
        pointsjoueur += 1
        nbBateauxEnVue += 1
    print("Il y a", nbBateauxEnVue, "bateau(x) en vue.\n")
    
  print("Vous avez gagné", pointsjoueur, "points.")
  return pointsjoueur
  
# Procédure qui trie le tableau de joueurs passé en paramètre par score
# décroissant. Algorithme : tri sélection.
def tri (joueurs):
  for i in range (len(joueurs)):
    imax = i
    for j in range (i, len(joueurs)):
      if joueurs[imax].getNbPoints()<joueurs[j].getNbPoints():
        imax = j
    if i != imax:
      joueurs[i], joueurs[imax] = joueurs[imax], joueurs[i]

# La fonction de parties aléatoires.
## On peut ajouter un peu de blindage. (nombres négatifs ?)
def progPartiesAleatoires():
  # Entrée des paramètres.
  verifbateau = 1
  while verifbateau==1: # Tant que le nombre entré est invalide
    try:
      nbBateaux = input("Nombre de bateaux : ")
      int(nbBateaux)
      verifbateau = 0
    except:
      print("/!\ Veuillez entrer un nombre entier.")
  nbBateaux = int(nbBateaux)
  verifgrille = 1
  while verifgrille == 1:
    tailleGrille = input("Taille de la grille : ")
    try:
      int(tailleGrille)
      verifgrille = 0
    except:
      print("/!\ Veuillez entrer un nombre entier.")
  tailleGrille = int(tailleGrille)
  
  # On a décidé de nommer les joueurs ainsi :
  noms = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
  joueurs = []
  for nom in noms:
    joueurs.append(Joueur(nom, 0))
  # 100 parties par joueur
  for iPartie in range(100):
    for joueur in joueurs:
      points = partieAleatoire(nbBateaux, tailleGrille)
      joueur.ajouterPoints(points)
  
  tri(joueurs)
  somme = 0
  for joueur in joueurs:
    somme = somme + joueur.getNbPoints()
  moyenne = somme / len(joueurs)
  for joueur in joueurs:
    print(joueur) # Affiche le nombre de points du joueur
  print("Moyenne :", moyenne)
  


#INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M 
#INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M 
#INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M #INTERFACE H-M 

boucle = True

while boucle == True:
  choixmenu = input("""\n \n Menu principal 
1. Partie automatique
2. Jouer une partie
3. Quitter\n""")

  if choixmenu == "1":
    progPartiesAleatoires()
    
  elif choixmenu == "2":
    partiejouer(6, 10)             #fonction à créer en bonus (partie jouée par le joueur qui choisira les coordonnées à frapper)
    
  elif choixmenu == "3":
    boucle = False
  else:
    print(" /!\ Veuillez entrer l'une des commandes proposées. ")
