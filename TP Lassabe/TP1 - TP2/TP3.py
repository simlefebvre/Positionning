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

def convertRssiToHisto(sample: dict[str, float]) -> dict[int, float]:
    """
    Convertit un fingerprint en histogramme
    """

    histo = {}
    sum = 0
    for mac,rssi in sample.items():
        sum = sum + rssi
    
    if sum == 0:
        raise ValueError("Fingerprint vide")
    for mac in sample.keys():
        histo[mac] = sample[mac]/sum
    return histo

def probability(histo1: NormHisto, histo2: NormHisto) -> float :
    """
    Calcule la probabilité de match entre deux histogrammes
    en comparant les deux histogramme en prenant la somme des zonne commune
    """

    sum = 0
    for mac in histo1.histogram.keys():
        if mac in histo2.histogram.keys():
            sum = sum + min(histo1.histogram[mac],histo2.histogram[mac])
    
    return sum
