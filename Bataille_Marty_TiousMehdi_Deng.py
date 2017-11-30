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
## A commenter : assez long...
def partieAleatoire(nbBateaux, tailleGrille):
  bateaux = []
  for iBateau in range(nbBateaux):
    bateau = None
    while not bateauInserableDansListe(bateaux, bateau):
      haut = random.randint(0, tailleGrille-1)
      gauche = random.randint(0, tailleGrille-1)
      etendre = random.randint(1, 3) <= 1
      bateau = None
      if etendre:
        direction = random.randint(1,2) == 1
        if direction == 1: # DROITE
          if gauche < tailleGrille-1:
            bateau = Bateau(haut, gauche, haut, gauche+1)
          else:
            bateau = Bateau(haut, gauche, haut, gauche)
        elif direction == 2: # BAS
          if haut < tailleGrille-1:
            bateau = Bateau(haut, gauche, haut+1, gauche)
          else:
            bateau = Bateau(haut, gauche, haut, gauche)
      else:
        bateau = Bateau(haut, gauche, haut, gauche)
    bateaux.append(bateau)
  
                      
  afficherGrille(bateaux, tailleGrille)
  essais = []
  points = 0
  for iEssai in range(3):
    case = [random.randint(0,tailleGrille-1), random.randint(0,tailleGrille-1)]
    while case in essais:
      case = [random.randint(0,4), random.randint(0,4)]
    essais.append(case)
    bateauMemeCase = chercherBateauDansListe(bateaux, case[0], case[1])
    bateauxEnVue = chercherBateauxEnVue(bateaux, case[0], case[1])
    if bateauMemeCase != None and not bateauMemeCase.estCoule():
      bateauMemeCase.couler()
      points = points + 8
    for bateau in bateauxEnVue:
      if not bateau.estCoule():
        points = points + 1
    afficherGrille(bateaux, tailleGrille, case[0], case[1])
  print("Résultat : %d points" % points)
  return points
  

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

# La fonction principale.
def main():
  # Entrée de paramètres (pas de blindage de la lecture !)
  nbBateaux = int(input("Nombre de bateaux : "))
  tailleGrille = int(input("Taille de la grille : "))
  
  noms = ["M", "N", "Alexandre Petit-Jaillet"]
  joueurs = []
  for nom in noms:
    joueurs.append(Joueur(nom, 0))
  for iPartie in range(5):
    for joueur in joueurs:
      points = partieAleatoire(nbBateaux, tailleGrille)
      joueur.ajouterPoints(points)
  tri(joueurs)
  somme = 0
  for joueur in joueurs:
    somme = somme + joueur.getNbPoints()
  moyenne = somme / len(joueurs)
  for joueur in joueurs:
    print(joueur)
  print("Moyenne :", moyenne)
  
  
main()
# ATTENTION : J'ai changé le nombre de parties et de joueurs pour le test.
# Il faut les remettre à respectivement 100 et 15!
