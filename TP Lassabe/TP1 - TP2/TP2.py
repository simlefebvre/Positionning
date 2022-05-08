from TP1 import *
import math
from numpy import arange

class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation=SimpleLocation(0,0,0), p: float=20.0, a: float=5.0, f: float=2417000000):
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f

AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55), 20.0, 5.0, 2417000000), \
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78), 20.0, 5.0,2417000000), \
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74), 20.0, 5.0, 2417000000), \
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80), 20.0, 5.0,2417000000), \
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04), 20.0, 5.0,2417000000)}


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
    return (Pt + Gr + Gt - Pr + 20*math.log10(lambd/(4*math.pi))) / (10*math.log10(d))

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

dist = lambda x ,y  : math.sqrt(math.pow((x.x-y.x),2) + math.pow((x.y-y.y),2) + math.pow((x.z-y.z),2))

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
    x_min = 2.0
    x_max = 9.0
    y_min = 1.0
    y_max = 21.5
    z_min = 1.2
    z_max = 4.2
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
