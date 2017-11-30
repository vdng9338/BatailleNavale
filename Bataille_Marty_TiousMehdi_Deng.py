import random

# Une classe Bateau qui simplifie le code de la partie.
class Bateau:
  def __init__(self, lig1, col1, lig2, col2):
    self._lig1 = lig1
    self._col1 = col1
    self._lig2 = lig2
    self._col2 = col2
    self._coule = False
    
  def getLigne1(self):
    return self._lig1
    
  def getColonne1(self):
    return self._col1
    
  def getLigne2(self):
    return self._lig2
    
  def getColonne2(self):
    return self._col2
    
    
    
    
    
    
  def estCoule(self):
    return self._coule
    
  def couler(self):
    self._coule = True

  def intersecteCase(self, lig, col):
    return (self.getLigne1() == lig and self.getColonne1() == col) or (self.getLigne2() == lig and self.getColonne2() == col)

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
    
  def estEnVue(self, lig, col):
    if self.intersecteCase(lig, col):
      return False
    else:
      return self.getLigne1() == lig or self.getLigne2() == lig or self.getColonne1() == col or self.getColonne2() == col
      
      
      
      
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
    
  def __str__(self):
    return "Le joueur " + self._nom + " a " + str(self._nbPoints) + " points"



def bateauInserableDansListe(liste, bateauAutre):
  if bateauAutre == None:
    return False
  for bateau in liste:
    if bateau.intersecte(bateauAutre):
      return False
  return True

def chercherBateauDansListe(liste, lig, col):
  for bateau in liste:
    if bateau.intersecteCase(lig, col):
      return bateau
  return None
    
def chercherBateauxEnVue(liste, lig, col):
  bateaux = []
  for bateau in liste:
    if bateau.estEnVue(lig, col):
      bateaux.append(bateau)
  return bateaux

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
  

def tri (joueurs):
  for i in range (len(joueurs)):
    imax = i
    for j in range (i, len(joueurs)):
      if joueurs[imax].getNbPoints()<joueurs[j].getNbPoints():
        imax = j
    if i != imax:
      joueurs[i], joueurs[imax] = joueurs[imax], joueurs[i]
      
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
