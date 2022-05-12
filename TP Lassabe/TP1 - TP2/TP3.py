import math
from TP1 import *
from TP2 import *

def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
    sum = 0
    for mac in sample1.keys():
        if mac not in sample2.keys():
            continue
        else:
            sum = sum + (sample1[mac] - sample2[mac])**2
    return math.sqrt(sum) 

def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
    bestFP = db.db.pop()
    bestDistance = rssi_distance(sample,bestFP.sample.toDict())

    for fp in db.db:
        if rssi_distance(sample,fp.sample.toDict()) < bestDistance:
            bestDistance = rssi_distance(sample,fp.sample.toDict())
            bestFP = fp
    return bestFP.position

class NormHisto:
    def __init__(self, histo: dict[int, float]):
        self.histogram = histo

"""
def convertRssiToHisto(sample: dict[str, float]) -> dict[int, float]:
    
    Convertit un fingerprint en histogramme


    histo = {}
    sum = 0
    for mac,rssi in sample.items():
        sum = sum + rssi
    
    if sum == 0:
        raise ValueError("Fingerprint vide")
    for mac in sample.keys():
        histo[mac] = sample[mac]/sum
    return histo
"""

def ParserHisto(fichier : str) -> list[tuple[SimpleLocation,dict[int, float]]]:
    L = []
    with open(fichier,"r") as data:
        for line in data:
            point = line.split(",")
            loc = SimpleLocation(float(point.pop(0)),float(point.pop(0)),float(point.pop(0)))
            point.pop(0)
            histo = {}
            count =0
            for index in range(1,len(point),2):
                if point[index] not in histo.keys():
                    histo[point[index]] = 1
                else:
                    histo[point[index]] = histo[point[index]] + 1
                count = count + 1
            
            #Normalisation de l'histogramme
            for dbm in histo.keys():
                histo[dbm] = histo[dbm]/count
            

            L.append((loc,histo))
    return L            

def fromFingerPrintToHisto(fp: Fingerprint) -> dict[str,NormHisto]:
    
    D = {}

    count = 0
    for sample in fp.sample.samples:
        histo = {}
        for dbm in sample.rssis:
            if dbm not in histo.keys():
                histo[dbm] = 1
            else:
                histo[dbm] = histo[dbm] + 1
            count = count + 1
        for dbm in histo.keys():
            histo[dbm] = histo[dbm]/count
        #L.append((sample.mac_address, NormHisto(histo)))
        D[sample.mac_address] = NormHisto(histo)
    return D

def fromDbToHisto(db: FingerprintDatabase) -> list[tuple[SimpleLocation,dict[str,NormHisto]]]:
    L = []
    for fp in db.db:
        L.append((fp.position,fromFingerPrintToHisto(fp)))
    return L

def probability(histo1: NormHisto, histo2: NormHisto) -> float :
    """
    Calcule la probabilité de match entre deux histogrammes
    en comparant les deux histogramme en prenant la somme des zonne commune
    """

    sum = 0
    for dbm in histo1.histogram.keys():
        if dbm in histo2.histogram.keys():
            sum = sum + min(histo1.histogram[dbm],histo2.histogram[dbm])
    return sum


def histogram_matching(db: FingerprintDatabase, sample: dict[str,NormHisto]) -> SimpleLocation:
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

#a = ParserHisto("test_data_not_filtered.csv")
#pass