from math import log10

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
            sum = sum+ 10 ** (sample / 10.)
        self.rssi = 10*log10((sum/len(self.rssis)))
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
            dic[sample.mac_address] = sample.rssi
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

class exportateur:
    def __init__(self,path : str,fgdb : FingerprintDatabase) -> None:
        
        with open(path,"w") as data:
            data.write("x,y,z,mac_address,rssi\n")
            for fp in fgdb.db:
                data.write(str(fp.position.x)+","+str(fp.position.y)+","+str(fp.position.z)+",")
                fp.sample.samples.sort(key=lambda x: x.mac_address)
                for rs in fp.sample.samples:
                    data.write(rs.mac_address+","+str(rs.rssi)+",")
                data.write("\n")
