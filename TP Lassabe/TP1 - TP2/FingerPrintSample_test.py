import obj

#Test if nothing is return when no mac address corespond in FingerPrintSample
def test_NewMacAdressFingerPrintSample():
    fps = obj.FingerprintSample([obj.RSSISample("0",[3.])])
    assert fps.getAlreadyHas("1") == None

#Test if the mac address is return when it is present in FingerPrintSample
def test_AlreadyPresentMacAdressFingerPrintSample():
    fps = obj.FingerprintSample([obj.RSSISample("0",[3.])])
    assert fps.getAlreadyHas("0") == obj.RSSISample("0",[3.])
