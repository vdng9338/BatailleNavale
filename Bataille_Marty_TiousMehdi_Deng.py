import random

# Une classe Bateau qui simplifie le code de la partie.
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

  def estMemeCase(self, lig, col):
    return self.getLigne() == lig and self.getColonne() == col

  def estEnVue(self, lig, col):
    if self.estMemeCase(lig, col):
      return False
    else:
      return self.getLigne() == lig or self.getColonne() == col

def chercherBateauDansListe(liste, lig, col):
    for bateau in liste:
        if bateau.estMemeCase(lig, col):
            return bateau
    return None
    
def chercherBateauxEnVue(liste, lig, col):
    bateaux = []
    for bateau in liste:
        if bateau.estEnVue(lig, col):
            bateaux.append(bateau)
    return bateaux

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

def partieAleatoire():
    bateaux = []
    for iBateau in range(2):
        bateau = Bateau(random.randint(0,4), random.randint(0,4))
        while chercherBateauDansListe(bateaux, bateau.getLigne(), bateau.getColonne()) != None:
            bateau = Bateau(random.randint(0,4), random.randint(0,4))
        bateaux.append(bateau)
    afficherGrille(bateaux)
    essais = []
    points = 0
    for iEssai in range(3):
        case = [random.randint(0,4), random.randint(0,4)]
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
        afficherGrille(bateaux, case[0], case[1])
    print("Résultat : %d points" % points)

def main():
  partieAleatoire()
  
main()
