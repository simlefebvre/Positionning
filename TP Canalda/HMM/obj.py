class model:
    def __init__(self, nb_states):
        self.totauxParCible = []
        self.totauxParSource = []
        self.totaux = []

        for i in range(nb_states):
            self.totauxParCible.append(0)
            self.totauxParSource.append(0)
            self.totaux.append([])
            for j in range(nb_states):
                self.totaux[i].append(0)
    
    def addMovement(self, source,cible):
        if source < len(self.totaux) and cible < len(self.totaux) and source >= 0 and cible >= 0:
            self.totaux[source][cible] += 1
            self.totauxParCible[cible] += 1
            self.totauxParSource[source] += 1
    
    def getValue(self, source, cible):
        """Retourne un tubple comprenant : 
            le nombre de mouvement entre deux états, 
            la probabilité d'arrivé dans l'état cible en partant de l'état source
            la probabilité de partir de l'état source quand on arrive dans l'état cible
        """
        if source < len(self.totaux) and cible < len(self.totaux) and source >= 0 and cible >= 0:
            if self.totauxParCible[cible] != 0 and self.totauxParSource[source] != 0:
                return (self.totaux[source][cible], self.totaux[source][cible]/self.totauxParSource[source], self.totaux[source][cible]/self.totauxParCible[cible])
            return (0,0,0)
        return None
    
    def __repr__(self) -> str: 
        s = " |           0           |           1           |           2           |           3           |           4           |           5           |\n"
        for i in range(len(self.totaux)):
            s = s + f"{i}|"
            for j in range(len(self.totaux[i])):
                nboc, par,pparti= self.getValue(i,j)
                s = s + f"nb={nboc};Pav={par:.2f};Pdep={pparti:.2f}|"
            s = s + "\n"
        return s