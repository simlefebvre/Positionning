import obj

#Test if nothing is return when no Location corespond in FingerPrintSampleDatabase
def test_NewLocationFingerPrintSampleDatabase():
    fpsd = obj.FingerprintDatabase()
    assert fpsd.getAlreadyLocation("1") == None

#Test if the FIngerprint is return when it's location is present in FingerPrintSampleDatabase
def test_AlreadyPresentLocationFingerPrintSampleDatabase():
    fpsd = obj.FingerprintDatabase()
    fpsd.db.append(obj.Fingerprint(obj.SimpleLocation(0,0,0),obj.FingerprintSample([obj.RSSISample("0",[3.])])))
    assert fpsd.getAlreadyLocation(obj.SimpleLocation(0,0,0)) == obj.Fingerprint(obj.SimpleLocation(0,0,0),obj.FingerprintSample([obj.RSSISample("0",[3.])]))