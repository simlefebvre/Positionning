import copy


class Coordone:
    def __init__(self, x : float, y : float ):
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)
    def __repr__(self) -> str:
        return self.__str__()


class Fingerprint:
    def __init__(self, coo : Coordone, fingerprint : dict[str, float]):
        self.coo = coo
        self.fingerprint = fingerprint
    
    def __str__(self):
        return "Fingerprint at " + str(self.coo) + " : " + str(self.fingerprint)
    
    def __repr__(self):
        return self.__str__()
    

def dist2Fingerprint(fp1 : Fingerprint, fp2 : Fingerprint) -> float:
    """
    Calcule la distance entre deux fingerprint dans l'espace des RSS
    """
    dist = 0
    for key in fp1.fingerprint.keys():
        if key in fp2.fingerprint.keys():
            dist += (fp1.fingerprint[key] - fp2.fingerprint[key])**2
        else:
            dist += (fp1.fingerprint[key] - (-100))**2
    
    for key in fp2.fingerprint.keys():
        if key not in fp1.fingerprint.keys():
            dist += (fp2.fingerprint[key] - (-100))**2

    return dist

def locateUsingScan(fp : Fingerprint, listFp : list[Fingerprint]) -> Coordone:
    """
    Trouve la position d'un fingerprint dans 
    la liste de fingerprint en utilisant le scan de toute les positions
    """
    minDist = 100
    minCoordone = Coordone(0,0)
    for fp2 in listFp:
        dist = dist2Fingerprint(fp, fp2)
        if dist < minDist:
            minDist = dist
            minCoordone = fp2.coo
    return minCoordone

def locateUsingWeightedBarycentre(fp : Fingerprint, listFp : list[Fingerprint]) -> Coordone:
    """
    Trouve la position d'un fingerprint dans 
    la liste de fingerprint en utilisant le barycentre pondéré
    """
    #Trie de la liste des fingerprint par ordre croissant de distance
    listFp.sort(key=lambda x: dist2Fingerprint(fp, x))
    #Calcule et stoque de la distance des K plus proche fingerprint
    K = 3
    distK = {}
    for i in range(K):
        FP = listFp.pop(0)
        distK[FP] = dist2Fingerprint(fp, FP)

    #Calcule le barycentre pondéré
    barycentre = Coordone(0,0)
    for FP in distK.keys():
        barycentre.x += FP.coo.x * distK[FP]
        barycentre.y += FP.coo.y * distK[FP]
    barycentre.x /= sum(distK.values())
    barycentre.y /= sum(distK.values())

    #Retourne le barycentre pondéré
    return barycentre

def computeMetric(fp : Fingerprint,mb : Fingerprint) -> float:
    """
    Calcule la métrique du fingerprint
    """
    sum = 0
    for i in fp.fingerprint.keys():
        sum = sum + abs(fp.fingerprint[i] - mb.fingerprint[i])
    return sum

    

def locateUsingMetric(fp : Fingerprint, listFp : list[Fingerprint]) -> Coordone:
    #Calcul des metriques
    listMetric = {}
    for fp2 in listFp:
        listMetric[fp2] = computeMetric(fp, fp2)
    
    #Trie de la liste des fingerprint par ordre croissant de distance
    listFp.sort(key=lambda x: listMetric[x])

    #Calcule et stoque les K plus proche fingerprint
    K = 4
    Lfp = []
    for i in range(K):
        Lfp.append(listFp.pop(0))
    
    #Calcule les alpha
    alpha = {}

    #Calcul de alpha 1 
    #ATTENTION ICI LE PAPIER DE VERONICA N'EST PAS BON
    sum = 1
    for i in range(1,K):
        sum = sum + (listMetric[Lfp[0]]/listMetric[Lfp[i]])
    alpha[Lfp[0]] = 1/sum

    #Calcul des autres alpha
    for i in range(1,K):
        alpha[Lfp[i]] = (listMetric[Lfp[0]]/listMetric[Lfp[i]]) * alpha[Lfp[0]]
    
    #Calcule des coordonées
    x = 0
    y = 0
    for i in range(K):
        x += alpha[Lfp[i]] * Lfp[i].coo.x
        y += alpha[Lfp[i]] * Lfp[i].coo.y
    return Coordone(x,y)

if __name__ == '__main__':
    cells = []

    cells.append(Fingerprint(Coordone(2,2), {'A':-38, 'B':-27, 'C':-54, 'D':-13}))
    cells.append(Fingerprint(Coordone(6,2), {'A':-34, 'B':-27, 'C':-38, 'D':-41}))
    cells.append(Fingerprint(Coordone(10,2), {'A':-17, 'B':-50, 'C':-44, 'D':-33}))
    cells.append(Fingerprint(Coordone(2,6), {'A':-74, 'B':-62, 'C':-48, 'D':-33}))
    cells.append(Fingerprint(Coordone(6,6), {'A':-64, 'B':-48, 'C':-72, 'D':-35}))
    cells.append(Fingerprint(Coordone(10,6), {'A':-27, 'B':-28, 'C':-32, 'D':-45}))
    cells.append(Fingerprint(Coordone(2,10), {'A':-13, 'B':-28, 'C':-12, 'D':-40}))
    cells.append(Fingerprint(Coordone(6,10), {'A':-45, 'B':-37, 'C':-20, 'D':-15}))
    cells.append(Fingerprint(Coordone(10,10), {'A':-30, 'B':-20, 'C':-60, 'D':-40}))

    Mobile = Fingerprint(None, {'A':-26, 'B':-42, 'C':-13, 'D':-46})

    print(locateUsingMetric(Mobile, copy.deepcopy(cells)))
