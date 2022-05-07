import math
from numpy import arange

class RSSISample:
    
    def __init__(self, mac_address: str, rssis: list[float]) -> None:
        """
        Initializes the RSSISample object.
        """
        self.mac_address = mac_address
        self.rssis = rssis
        self.rssi = 0.
    def setAverageRssi(self) -> None:
        """
        Calculates the average RSSI value of the given RSSI values.
        """
        sum = 0
        if len(self.rssis) == 0:
            raise Exception("No RSSI values")
        for sample in self.rssis:
            sum = sum+ sample
        self.rssi = 10 ** ((sum/len(self.rssis)) / 10.)
        return self
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the RSSISample object.
        """
        return "RSSISample(mac_address={}, rssis={}, rssi={})".format(self.mac_address, self.rssis, self.rssi)

    def __eq__(self, __o: object) -> bool:
        """
        Returns True if the given object is equal to the RSSISample object.
        """
        if not isinstance(__o, RSSISample):
            return False
        return self.mac_address == __o.mac_address and self.rssis == __o.rssis and self.rssi == __o.rssi

class FingerprintSample:
    def __init__(self, samples: list[RSSISample] ) -> None:
        self.samples = samples

    def getAlreadyHas(self, mac_address: str) -> RSSISample:
        """
        Returns the RSSISample object with the given mac address.
        @param mac_address: The mac address of the RSSISample object.
        @return: The RSSISample object with the given mac address.
        """
        for sample in self.samples:
            if sample.mac_address == mac_address:
                return sample
        return None
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the FingerprintSample object.
        @return: A string representation of the FingerprintSample object.
        """
        return "FingerprintSample: " + str(self.samples)

    def __eq__(self, object: object) -> bool:
        """
        Returns True if the given object is equal to the FingerprintSample object.
        @param object: The object to compare to.
        @return: True if the given object is equal to the FingerprintSample object.
        """
        if isinstance(object, FingerprintSample):
            return self.samples == object.samples
        return False

    def toDict(self):
        """
        Returns a dictionary representation of the FingerprintSample object.
        @return: A dictionary representation of the FingerprintSample object.
        """
        dic = {}
        for sample in self.samples:
            dic[sample.mac_address] = sample.rssis
        return dic



class SimpleLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return "x : " + str(self.x) +" y : " + str(self.y) + " z : " + str(self.z)

    def __eq__(self, other) -> bool:
        return other.x == self.x and other.y == self.y and other.z == self.z
    
class Fingerprint:
    def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
        self.position : SimpleLocation = position
        self.sample : FingerprintSample = sample
    
    def __repr__(self) -> str:
        return "Position : " + str(self.position) + " Sample : " + str(self.sample)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Fingerprint):
            return self.position == __o.position and self.sample == __o.sample
        

class FingerprintDatabase:
    def __init__(self) -> None:
        self.db : list[Fingerprint] = []
    def getAlreadyLocation(self,other : SimpleLocation) -> Fingerprint:
        """
        Returns the Fingerprint object with the given position.
        @param other: The position of the Fingerprint object.
        @return: The Fingerprint object with the given position.
        """
        for fp in self.db:
            if fp.position == other:
                return fp
        return None

    def __repr__(self):
        return str(self.db)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, FingerprintDatabase):
            return __o.db == self.db
        return False

class Parser:
    def __init__(self,path:str,fgdb:FingerprintDatabase) -> None:
        with open(path,"r") as data:
            for line in data:
                point = line.split(",")
                sl = SimpleLocation(float(point.pop(0)),float(point.pop(0)),float(point.pop(0)))
                fp = fgdb.getAlreadyLocation(sl)
                if fp == None:
                    fp = Fingerprint(sl,FingerprintSample([]))
                    fgdb.db.append(fp)
                point.pop(0)

                
                for index in range(0,len(point),2):
                    if fp.sample.getAlreadyHas(point[index]) == None:
                        fp.sample.samples.append(RSSISample(point[index],[float(point[index+1])]))
                    else:
                        fp.sample.getAlreadyHas(point[index]).rssis.append(float(point[index+1]))
                
    def compute(self,fgdb:FingerprintDatabase):
        for fp in fgdb.db:
            for rs in fp.sample.samples:
                rs.setAverageRssi()

class exportateur():
    def __init__(self,path : str,fgdb : FingerprintDatabase) -> None:
        with open(path,"w") as data:
            data.write("x,y,z,mac_address,rssi\n")
            for fp in fgdb.db:
                data.write(str(fp.position.x)+","+str(fp.position.y)+","+str(fp.position.z)+",")
                for rs in fp.sample.samples:
                    data.write(rs.mac_address+","+str(rs.rssi)+",")
                data.write("\n")

class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation=SimpleLocation(0,0,0), p: float=20.0, a: float=5.0, f: float=2417000000):
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f

def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
    """
    Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
    and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
    :param distance: the distance between AP and device
    :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
    :return: one value for the FBCM index
    """
    Pr = rssi_values.rssi
    Pt = ap.output_power_dbm
    Gt = ap.antenna_dbi
    Gr = 2.1
    d = distance
    c = 299792458
    lambd = c / ap.output_frequency_hz
    return (Pt + Gr + Gt - Pr + 20*math.log10(lambd) - 20 * math.log10(4*math.pi)) / (10*math.log10(d))


AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55), 20.0, 5.0, 2417000000), \
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78), 20.0, 5.0,2417000000), \
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74), 20.0, 5.0, 2417000000), \
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80), 20.0, 5.0,2417000000), \
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04), 20.0, 5.0,2417000000)}

def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    """
    Function estimate_distance estimates the distance between an access point and a test point based on
    the test point rssi sample.
    :param rssi: average RSSI value for test point
    :param fbcm_index: index to use
    :param ap: access points parameters used in FBCM
    :return: the distance (meters)
    """
    Pr = rssi_avg
    Pt = ap.output_power_dbm
    Gt = ap.antenna_dbi
    Gr = 2.1
    i = fbcm_index
    c = 299792458
    lambd = c / ap.output_frequency_hz

    return math.pow(10, ((Pt + Gr + Gt - Pr + 20*math.log10(lambd) - 20 * math.log10(4*math.pi)) / (10*i)))

dist = lambda x ,y  : math.sqrt((x.x-y.x)**2 + (x.y-y.y)**2 + (x.z-y.z)**2)

def computeCost(distances: dict[str, float], ap_locations: dict[str, SimpleLocation],loc : SimpleLocation) -> float:
    """
    Function computeCost computes the cost of a location based on its distances towards at least 3 access points
    :param distances: the distances associated to the related AP MAC addresses as a string
    :param ap_locations: the access points locations, indexed by AP MAC address as strings
    :return: a cost
    """
    cout = 0
    for d in distances.keys():
        cout = cout + abs(dist(ap_locations[d],loc) - distances[d])
    return cout

def computeSpaceResearch(ap_locations : dict[str, SimpleLocation]) -> tuple[float,float,float,float,float,float]:
    """
    Function computeSpaceResearch computes the space research parameters based on the access points locations
    :param ap_locations: the access points locations, indexed by AP MAC address as strings
    :return: the space research parameters
    """
    x_min = min(ap_locations.values(), key=lambda x: x.x).x
    x_max = max(ap_locations.values(), key=lambda x: x.x).x
    y_min = min(ap_locations.values(), key=lambda x: x.y).y
    y_max = max(ap_locations.values(), key=lambda x: x.y).y
    z_min = min(ap_locations.values(), key=lambda x: x.z).z
    z_max = max(ap_locations.values(), key=lambda x: x.z).z
    return x_min,x_max,y_min,y_max,z_min,z_max

def multilateration(distances: dict[str, float], ap_locations: dict[str, SimpleLocation]) -> SimpleLocation:
    """
    Function multilateration computes a location based on its distances towards at least 3 access points
    :param distances: the distances associated to the related AP MAC addresses as a string
    :param ap_locations: the access points locations, indexed by AP MAC address as strings
    :return: a location
    """
    bestloc = SimpleLocation(0,0,0)
    bestCost = computeCost(distances,ap_locations,bestloc)
    x_min,x_max,y_min,y_max,z_min,z_max = computeSpaceResearch(ap_locations)
    for x in arange(x_min,x_max,0.1):
        for y in arange(y_min,y_max,0.1):
            for z in arange(z_min,z_max,0.1):
                loc = SimpleLocation(x,y,z)
                if computeCost(distances,ap_locations,loc) < bestCost:
                    bestCost = computeCost(distances,ap_locations,loc)
                    bestloc = loc
    return bestloc

def estimate_AP_index(db : FingerprintDatabase, ap_mac : str) -> float:
    """
    Function estimate_AP_index estimates the FBCM index for a given access point
    :param db: the fingerprint database
    :param ap_mac: the access point MAC address
    :return: the FBCM index
    """
    compt = 0
    sum = 0
    for fp in db.db:
        for sample in fp.sample.samples:
            if sample.mac_address == ap_mac:
                sum = sum + compute_FBCM_index(dist(fp.position,AP[ap_mac].location),sample,AP[ap_mac])
                compt = compt +1
    return sum/compt

def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
    sum = 0
    for mac in sample1.keys():
        if mac not in sample2.keys():
            return -1
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
