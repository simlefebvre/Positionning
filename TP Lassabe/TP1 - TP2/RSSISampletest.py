import unittest
import obj

class RSSISampleTest(unittest.TestCase):

    def setUp(self) -> None:
        pass
    
    def avarageWithOneRSSIValue(self):
        RssiSample = obj.RSSISample("",[10])
        RssiSample.setAverageRssi()
        self.assertEqual(RssiSample.rssi,40)

if __name__ == '__main__':
    unittest.main()