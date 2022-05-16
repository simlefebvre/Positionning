import math

import numpy
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

class GaussModel:
    def __init__(self, avg: float, stddev: float):
        self.average_rssi = avg
        self.standard_deviation = stddev

normal = lambda x,sample : (1/(math.sqrt(2*math.pi)*sample.standard_deviation))*math.exp(- (1/2) * ((x - sample.average_rssi)/sample.standard_deviation)**2)

def histogram_from_gauss(sample: GaussModel) -> NormHisto:
    L = [i for i in range(math.floor(sample.average_rssi)-10,math.floor(sample.average_rssi)+10)]
    histo = {}
    for dbm in L:
        histo[dbm] = normal(dbm,sample)
    return NormHisto(histo)

def fromFingerprintToGauss(sample: Fingerprint) -> dict[str,GaussModel]:
    D = {}
    for samp in sample.sample.samples:
       D[samp.mac_address] = GaussModel(numpy.mean(samp.rssis),numpy.std(samp.rssis))
    return D

def fromDbToGauss(db: FingerprintDatabase) -> list[tuple[SimpleLocation,dict[str,GaussModel]]]:
    L = []
    for fp in db.db:
        L.append((fp.position,fromFingerprintToGauss(fp)))
    return L

def probability_gauss(gauss1: GaussModel, gauss2: GaussModel) -> float :
    hist1 = histogram_from_gauss(gauss1)
    hist2 = histogram_from_gauss(gauss2)
    return probability(hist1,hist2)

def gauss_matching(db: FingerprintDatabase, sample: dict[str,GaussModel]) -> SimpleLocation:
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

#a = ParserHisto("test_data_not_filtered.csv")
#pass