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
    
  # Cette méthode renverra toujours False si le bateau est coulé, de manière à
  # éviter d'attribuer des points à quelqu'un qui coule un bateau coulé.
  # Est-ce judicieux ??
  def estMemeCase(self, lig, col):
    if self.estCoule():
      return False
    else:
      return self.getLigne() == lig and self.getColonne() == col
  
  # Cette méthode renverra toujours False si le bateau est coulé, de manière à
  # éviter d'attribuer des points à quelqu'un qui coule un bateau coulé.
  # Est-ce judicieux ??
  # D'ailleurs, cette méthode renverra False si la case donnée en paramètre est
  # la même que celle du bateau. Au cas où la partie est mal codée...
  def estEnVue(self, lig, col):
    if self.estCoule:
      return False
    elif self.estMemeCase(lig, col):
      return False
    else:
      return self.getLigne() == lig or self.getColonne() == col

def main():
  pass
  
main()
