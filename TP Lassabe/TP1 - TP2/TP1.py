from math import log10

class RSSISample:
    """
    Objet représentant une prise de mesure de RSSI avec pour valeur l'adresse mac qui est associée à l'AP et la liste des RSSI mesurés.
    """
    
    def __init__(self, mac_address: str, rssis: list[float]) -> None:
        """
        Initialise un objet RSSISample avec l'adresse mac de l'AP et la liste des RSSI mesurés.
        """
        self.mac_address = mac_address
        self.rssis = rssis
        self.rssi = 0.
    
    def setAverageRssi(self) -> None:
        """
        Calcule la moyenne des RSSI mesurés.
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
        Retournes une représentation textuelle de l'objet RSSISample.
        """
        return "RSSISample(mac_address={}, rssis={}, rssi={})".format(self.mac_address, self.rssis, self.rssi)

    def __eq__(self, __o: object) -> bool:
        """
        Retourne True si l'objet __o est égal à l'objet RSSISample.
        """
        if not isinstance(__o, RSSISample):
            return False
        return self.mac_address == __o.mac_address and self.rssis == __o.rssis and self.rssi == __o.rssi

class FingerprintSample:
    """
    Objet représentant un fingerprint avec la liste des samples.
    """
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
    """
    Objet représentant une position dans l'espace.
    """
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return "x : " + str(self.x) +" y : " + str(self.y) + " z : " + str(self.z)

    def __eq__(self, other) -> bool:
        return other.x == self.x and other.y == self.y and other.z == self.z
    
class Fingerprint:
    """
    Objet représentant un fingerprint avec la liste des samples et les coordonées.
    """
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
    """
    Objet permetant de parser le fichier donné en entrée dans une base de donnée donnée en paramètre.
    """
    def __init__(self,path:str,fgdb:FingerprintDatabase) -> None:
        with open(path,"r") as data: #Ouverture du fichier
            for line in data: #Pour chaque ligne du fichier
                point = line.split(",") #On sépare les différents éléments
                sl = SimpleLocation(float(point.pop(0)),float(point.pop(0)),float(point.pop(0))) #On récupère les coordonées
                fp = fgdb.getAlreadyLocation(sl) #On récupère le fingerprint correspondant au coordonées s'il existe
                if fp == None: #Si il n'existe pas on le crée
                    fp = Fingerprint(sl,FingerprintSample([]))
                    fgdb.db.append(fp)
                point.pop(0)#On supprime le mac address

                
                for index in range(0,len(point),2):#Pour chaque valeur de RSSI
                    if fp.sample.getAlreadyHas(point[index]) == None: #Si le sample avec le mac address n'existe pas on le crée
                        fp.sample.samples.append(RSSISample(point[index],[float(point[index+1])]))
                    else:#Sinon on ajoute la valeur au sample
                        fp.sample.getAlreadyHas(point[index]).rssis.append(float(point[index+1]))
                
    def compute(self,fgdb:FingerprintDatabase):
        """
        Compute the avarage RSSI of each fingerprint in the database.
        """
        for fp in fgdb.db:
            for rs in fp.sample.samples:
                rs.setAverageRssi()

class exportateur:
    """
    Objet permetant d'exporter la base de donnée en format csv.
    """
    def __init__(self,path : str,fgdb : FingerprintDatabase) -> None:
        """
        Réalise l'export du la base de donnée passée en paramètre.
        """
        with open(path,"w") as data:
            data.write("x,y,z,mac_address,rssi\n") #On écrit les entêtes
            for fp in fgdb.db:#Pour chaque fingerprint
                data.write(str(fp.position.x)+","+str(fp.position.y)+","+str(fp.position.z)+",")#On écrit les coordonées
                fp.sample.samples.sort(key=lambda x: x.mac_address)#On trie les samples par mac address
                for rs in fp.sample.samples:#Pour chaque sample
                    data.write(rs.mac_address+","+str(rs.rssi)+",")#On écrit le mac address et le rssi 
                data.write("\n")
