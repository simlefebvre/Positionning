import obj
import pytest

#test the average of one RSSI value
def test_avarageWithOneRSSIValue():
        RssiSample = obj.RSSISample("",[10])
        RssiSample.setAverageRssi()
        assert RssiSample.rssi == 10

#test the average of two RSSI values
def test_avarageWithSeveralValues():
        RssiSample = obj.RSSISample("",[5,15])
        RssiSample.setAverageRssi()
        assert RssiSample.rssi == 10

#test if an exception is raised when no RSSI values are given
def test_avarageWithNoRSSIValue():
        RssiSample = obj.RSSISample("",[])
        with pytest.raises(Exception):
            RssiSample.setAverageRssi()

