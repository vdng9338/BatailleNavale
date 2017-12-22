import random

# Une classe Bateau qui simplifie le code de la partie.
# Pour la version de base, une seule case.
class Bateau:
  def __init__(self, lig, col):
    self._lig = lig
    self._col = col
    self._coule = False
    
  def getLigne(self):
    return self._lig
    
  def getColonne(self):
    return self._col
    
  def estCoule(self):
    return self._coule
    
  def couler(self):
    self._coule = True

  # Retourne si le bateau est à la case décrite.
  def estMemeCase(self, lig, col):
    return self.getLigne() == lig and self.getColonne() == col

  # Retourne si le bateau est considéré en vue depuis la case décrite, c'est-à-dire soit à la même
  # colonne soit à la même ligne (mais pas les deux).
  def estEnVue(self, lig, col):
    if self.estMemeCase(lig, col):
      return False
    else:
      return self.getLigne() == lig or self.getColonne() == col
      
      
      
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
  
  # Méthode pour un affichage simplifié.
  def __str__(self):
    return "Le joueur " + self._nom + " a " + str(self._nbPoints) + " points."



# Cherche étant donné une liste de bateaux et une case le bateau éventuel qui est à la case donnée en paramètre.
# Inclut les bateaux coulés !
def chercherBateauDansListe(liste, lig, col):
  for bateau in liste:
    if bateau.estMemeCase(lig, col):
      return bateau
  return None

# Cherche, étant donné une liste de bateaux et une case, les éventuels bateaux en vue depuis la case donnée.
# Inclut les bateaux coulés !
def chercherBateauxEnVue(liste, lig, col):
  bateaux = []
  for bateau in liste:
    if bateau.estEnVue(lig, col):
      bateaux.append(bateau)
  return bateaux

# Affichage de la grille avec éventuellement le coup porté : ! pour le coup, . pour rien du tout, X pour un bateau
# coulé, B pour un bateau encore en vie.
def afficherGrille(bateaux, ligneCoup=None, colonneCoup=None):
  for ligne in range(5):
    for colonne in range(5):
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

# Cette fonction exécute une partie aléatoire (3 essais) et renvoie le nombre de points obtenus.
def partieAleatoire():
  # Génération des bateaux
  bateaux = []
  for iBateau in range(2):       
    bateau = Bateau(None, None)
    while chercherBateauDansListe(bateaux, bateau.getLigne(), bateau.getColonne()) != None:
      bateau = Bateau(random.randint(0,4), random.randint(0,4))
    bateaux.append(bateau)
  #afficherGrille(bateaux)
  
  # La partie à proprement parler
  essais = []
  points = 0
  for iEssai in range(3):
    # Détermination de la case à toucher
    case = [None, None]
    while case in essais:
      case = [random.randint(0,4), random.randint(0,4)]
    essais.append(case)
    # Récupération des bateaux en vue et à la même case
    bateauMemeCase = chercherBateauDansListe(bateaux, case[0], case[1])
    bateauxEnVue = chercherBateauxEnVue(bateaux, case[0], case[1])
    # Coulage de l'éventuel bateau coulé
    if bateauMemeCase != None and not bateauMemeCase.estCoule():
      bateauMemeCase.couler()
      points = points + 8
    # Ajout des points pour chaque bateau en vue
    for bateau in bateauxEnVue:
      if not bateau.estCoule():
        points = points + 1
    #afficherGrille(bateaux, case[0], case[1])
  #print("Résultat : %d points" % points)
  return points
  

# Trie la liste de joueurs donnée par score décroissant. Tri sélection.
def tri (joueurs):
  for i in range (len(joueurs)):
    imax = i
    for j in range (i, len(joueurs)):
      if joueurs[imax].getNbPoints()<joueurs[j].getNbPoints():
        imax = j
    if i != imax:
      joueurs[i], joueurs[imax] = joueurs[imax], joueurs[i]
      
def main():
  noms = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Alexandre Petit-Jaillet"]
  # Création du tableau des joueurs
  joueurs = []
  for nom in noms:
    joueurs.append(Joueur(nom, 0))
  # 100 parties par joueur
  for iPartie in range(100):
    for joueur in joueurs:
      points = partieAleatoire()
      joueur.ajouterPoints(points)
  # Tri des joueurs
  tri(joueurs)
  # Calcul de la moyenne
  somme = 0
  for joueur in joueurs:
    somme = somme + joueur.getNbPoints()
  moyenne = somme / len(joueurs)
  # Affichage
  for joueur in joueurs:
    print(joueur)
  print("Moyenne :", moyenne)
  
  
main()