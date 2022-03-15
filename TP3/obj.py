class RSSISample:
    def __init__(self, mac_address: str, rssi: list[float]) -> None:
        self.mac_address = mac_address
        self.rssi = rssi

    def get_average_rssi(self) -> float:
        sum = 0
        for sample in self.rssi:
            sum = sum+ sample
        return 10 ** ((sum/len(self.rssi)) / 10.)
   

class FingerprintSample:
    def __init__(self, samples: list[RSSISample] ) -> None:
        self.samples = samples

class SimpleLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return "x : " + str(self.x) +" y : " + str(self.y) + " z : " + str(self.z)

class Fingerprint:
    def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
        self.position = position
        self.sample = sample

class FingerprintDatabase:
    def __init__(self) -> None:
        self.db = []

class Parser:
    def __init__(self,path:str) -> None:
        with open(path,"r") as data:
            for line in data:
                point = line.split(",")
                sl = SimpleLocation(float(point.pop(0)),float(point.pop(0)),float(point.pop(0)))
                orientation = point.pop(0)
                l=[]
                for i in range(len(point)//2):
                    l.append(RSSISample(point.pop(0),point.pop(0)))
                pass