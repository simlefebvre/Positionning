import math

import numpy
from TP1 import *
from TP2 import *

def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
    """
    Calcul la distance entre deux samples dans l'espace des RSSI
    :param sample1: un sample
    :param sample2: un sample
    :return: la distance entre les deux samples    
    """
    sum = 0
    for mac in sample1.keys():#pour chaque adresse MAC
        if mac not in sample2.keys():#si elle n'est pas dans le sample2 on passe
            continue
        else:#sinon on calcule la distance
            sum = sum + (sample1[mac] - sample2[mac])**2
    return math.sqrt(sum) 

def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
    """
    Utilisation du simple matching pour estimer une position : on récupére et retourne la position la plus proche
    :param db: la base de données
    :param sample: le sample à estimer
    :return: la position la plus proche dans la base de donée
    """
    bestFP = db.db.pop()
    bestDistance = rssi_distance(sample,bestFP.sample.toDict())

    for fp in db.db:
        if rssi_distance(sample,fp.sample.toDict()) < bestDistance:
            bestDistance = rssi_distance(sample,fp.sample.toDict())
            bestFP = fp
    return bestFP.position

class NormHisto:
    """
    Objet représetnant un sample sous la forme d'un histogramme normalisé
    """
    def __init__(self, histo: dict[int, float]):
        self.histogram = histo

def ParserHisto(fichier : str) -> list[tuple[SimpleLocation,dict[int, float]]]:
    """
    Fonction permettant de parser un fichier de prise de mesure de RSSI en une liste d'histograme normalisé
    """
    L = []
    with open(fichier,"r") as data:
        for line in data:#pour chaque ligne du fichier
            point = line.split(",")
            loc = SimpleLocation(float(point.pop(0)),float(point.pop(0)),float(point.pop(0))) #on récupère la position
            point.pop(0)
            histo = {}
            count =0
            for index in range(1,len(point),2):#pour chaque couple d'adresse MAC et RSSI
                if point[index] not in histo.keys():#si l'adresse MAC n'est pas dans le dictionnaire
                    histo[point[index]] = 1 #on l'ajoute avec une valeur de 1
                else:
                    histo[point[index]] = histo[point[index]] + 1 #sinon on ajoute 1 a la valeur déjà présente
                count = count + 1
            
            #Normalisation de l'histogramme
            for dbm in histo.keys():
                histo[dbm] = histo[dbm]/count
            

            L.append((loc,histo))
    return L            

def fromFingerPrintToHisto(fp: Fingerprint) -> dict[str,NormHisto]:
    """
    Fonction permettant la transformation d'un fingerprint en histogramme normalisé
    :param fp: le fingerprint à transformer
    :return: l'histogramme normalisé
    """
    D = {}

    count = 0
    for sample in fp.sample.samples: #pour chaque sample
        histo = {}
        for dbm in sample.rssis: #pour chaque RSSI
            if dbm not in histo.keys():#si l'adresse MAC n'est pas dans le dictionnaire
                histo[dbm] = 1#on l'ajoute avec une valeur de 1
            else:
                histo[dbm] = histo[dbm] + 1#sinon on ajoute 1 a la valeur déjà présente
            count = count + 1

        #Normalisation de l'histogramme
        for dbm in histo.keys():
            histo[dbm] = histo[dbm]/count
        
        D[sample.mac_address] = NormHisto(histo)
    return D

def fromDbToHisto(db: FingerprintDatabase) -> list[tuple[SimpleLocation,dict[str,NormHisto]]]:
    """
    Fonction permettant la transformation d'une base de donnée en histogramme normalisé
    :param db: la base de donnée
    :return: la base de donnée transformée en histogramme normalisé
    """
    L = []
    for fp in db.db:
        L.append((fp.position,fromFingerPrintToHisto(fp)))
    return L

def probability(histo1: NormHisto, histo2: NormHisto) -> float :
    """
    Calcule la probabilité de match entre deux histogrammes
    en comparant les deux histogramme en prenant la somme des zones communes
    :param histo1: un histogramme normalisé
    :param histo2: un histogramme normalisé
    :return: la probabilité de match entre les deux histogrammes
    """

    sum = 0
    for dbm in histo1.histogram.keys():
        if dbm in histo2.histogram.keys():
            sum = sum + min(histo1.histogram[dbm],histo2.histogram[dbm])
    return sum

def histogram_matching(db: FingerprintDatabase, sample: dict[str,NormHisto]) -> SimpleLocation:
    """
    Utilisation du matching entre histogramme pour estimer une position
    :param db: la base de données
    :param sample: le sample à estimer
    :return: la position la plus proche dans la base de donée
    """

    histDb = fromDbToHisto(db)
    bestScore = None
    bestLoc = None
    for loc,FpHist in histDb:
        score = 0
        for mac in FpHist.keys():
            hist = FpHist[mac]
            if mac in sample.keys():
                score = score + probability(sample[mac],hist)
        if bestScore == None or score > bestScore:
            bestScore = score
            bestLoc = loc
    return bestLoc        

class GaussModel:
    """
    Objet représentant un modèle de Gauss
    """
    def __init__(self, avg: float, stddev: float):
        self.average_rssi = avg
        self.standard_deviation = stddev


normal = lambda x,sample : (1/(math.sqrt(2*math.pi)*sample.standard_deviation))*math.exp(- (1/2) * ((x - sample.average_rssi)/sample.standard_deviation)**2)

def histogram_from_gauss(sample: GaussModel) -> NormHisto:
    """
    Fontion permettant de transformer un modèle de Gauss en histogramme normalisé
    :param sample: le modèle de Gauss
    :return: l'histogramme normalisé
    """
    L = [i for i in range(math.floor(sample.average_rssi)-10,math.floor(sample.average_rssi)+10)]
    histo = {}
    for dbm in L:
        histo[dbm] = normal(dbm,sample)
    return NormHisto(histo)

def fromFingerprintToGauss(sample: Fingerprint) -> dict[str,GaussModel]:
    """
    Fonction permettant la transformation d'un fingerprint en modèle de Gauss
    :param sample: le fingerprint à transformer
    :return: le modèle de Gauss
    """
    D = {}
    for samp in sample.sample.samples:
       D[samp.mac_address] = GaussModel(numpy.mean(samp.rssis),numpy.std(samp.rssis))
    return D

def fromDbToGauss(db: FingerprintDatabase) -> list[tuple[SimpleLocation,dict[str,GaussModel]]]:
    """
    Fonction permettant la transformation d'une base de donnée en modèle de Gauss
    :param db: la base de donnée
    :return: la base de donnée transformée en modèle de Gauss
    """
    L = []
    for fp in db.db:
        L.append((fp.position,fromFingerprintToGauss(fp)))
    return L

def probability_gauss(gauss1: GaussModel, gauss2: GaussModel) -> float :
    """
    Calcule la probabilité de match entre deux modèles de Gauss en comparant la probabilité de match entre leur deux histogrammes
    :param gauss1: un modèle de Gauss
    :param gauss2: un modèle de Gauss
    :return: la probabilité de match entre les deux modèles de Gauss
    """
    hist1 = histogram_from_gauss(gauss1)
    hist2 = histogram_from_gauss(gauss2)
    return probability(hist1,hist2)

def gauss_matching(db: FingerprintDatabase, sample: dict[str,GaussModel]) -> SimpleLocation:
    """
    Utilisation du matching entre modèle de Gauss pour estimer une position
    :param db: la base de données
    :param sample: le sample à estimer
    :return: la position estimée
    """
    gaussDb = fromDbToGauss(db)
    bestScore = None
    bestLoc = None
    for loc,FpGauss in gaussDb:
        score = 0
        for mac in FpGauss.keys():
            gauss = FpGauss[mac]
            if mac in sample.keys():
                score = score + probability_gauss(sample[mac],gauss)
        if bestScore == None or score > bestScore:
            bestScore = score
            bestLoc = loc
    return bestLoc