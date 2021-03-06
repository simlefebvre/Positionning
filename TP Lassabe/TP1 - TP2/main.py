from TP1 import *
from TP2 import *
from TP3 import *

fpdb = FingerprintDatabase()

def TP1():
    global fpdb
    pars = Parser("data.csv",fpdb)
    pars.compute(fpdb)
    exportateur("export.csv",fpdb)

def TP2():
    global fpdb
    APIndex = {}
    #Calcul des index de calibration de friis
    for mac in AP.keys():
        index = estimate_AP_index(fpdb,mac)
        APIndex[mac] = index

    MobileSamples = []
    
    testT = []
    #Calcul a partir des index, la distance entre le mobile et les différents AP
    #Lecture du fichier de données
    with open("test_data.csv") as test:
        
        for line in test:
            testT.append(line[:line.find(",0,")])
            line = line[line.find(",0,")+3:]
            data = line.split(",")
            RSSISamples = []
            for i in range(0,len(data),2):
                mac = data[i]
                rssi = float(data[i+1])
                RssiSample = RSSISample(mac,[rssi])
                RssiSample.setAverageRssi()
                RSSISamples.append(RssiSample)
            MobileSamples.append(FingerprintSample(RSSISamples))
                
    for MobileSample,st in zip(MobileSamples,testT):
        APDist = {}
        for mac in AP.keys():
            for sample in MobileSample.samples:
                if sample.mac_address == mac:
                    dist = estimate_distance(sample.rssi,APIndex[mac],AP[mac])
                    APDist[mac] = dist


        APLoc  = {}
        for mac in AP.keys():
            APLoc[mac] = AP[mac].location

        mobileLoc = multilateration(APDist,APLoc)
        print(st)
        print(mobileLoc)

def TP3_histo():
    fdb = FingerprintDatabase()
    a = Parser("test_data_not_filtered.csv",fdb)
    #fpdbhisto = fromDbToHisto(fpdb)

    i=0
    for fp in fdb.db:
        print(i)
        i = i+1
        print("position exact",fp.position)
        histo = fromFingerPrintToHisto(fp)
        mobileLoc = histogram_matching(fpdb,histo)
        print("position estimé",mobileLoc,"\n")

def TP3_gauss():
    fdb = FingerprintDatabase()
    a = Parser("test_data_not_filtered.csv",fdb)
    #fpdbhisto = fromDbToHisto(fpdb)

    i=0
    for fp in fdb.db:
        print(i)
        i = i+1
        print("position exact",fp.position)
        gauss = fromFingerprintToGauss(fp)
        mobileLoc = gauss_matching(fpdb,gauss)
        print("position estimé",mobileLoc,"\n")

if __name__ == "__main__":
    TP1()
    #TP2()
    #TP3_histo()
    TP3_gauss()
    
    pass