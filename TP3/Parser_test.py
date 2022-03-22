import obj

#Test if the Parser parse 1 line correctly with one mac adress and one RSSI

def test_parser_one_line():
    fgdb = obj.FingerprintDatabase()
    parser = obj.Parser("test/ressource/OneLine.csv",fgdb)
    loc = obj.SimpleLocation(5.4,29.59,1.2)
    rss = obj.RSSISample("00:13:ce:8f:77:43",[-63.0])
    fp = obj.Fingerprint(loc,obj.FingerprintSample([rss]))
    expectFgdb = obj.FingerprintDatabase()
    expectFgdb.db.append(fp)
    assert fgdb == expectFgdb

#Test if the parser parse several lines correctly with several mac adresses and one RSSI per mac address and one line per points

def test_parser_several_lines():
    fgdb = obj.FingerprintDatabase()
    parser = obj.Parser("test/ressource/SeveralLineOneRSSI.csv",fgdb)
    loc1 = obj.SimpleLocation(5.40,29.59,1.20)
    rss11 = obj.RSSISample("00:13:ce:8f:77:43",[-63.0])
    rss12 = obj.RSSISample("00:13:ce:97:78:79",[-80.0])
    rss13 = obj.RSSISample("00:13:ce:8f:78:d9",[-29.0])
    fp1 = obj.Fingerprint(loc1,obj.FingerprintSample([rss11,rss12,rss13]))
    expectFgdb = obj.FingerprintDatabase()
    expectFgdb.db.append(fp1)

    loc2 = obj.SimpleLocation(6.40,29.59,1.20)
    rss21 = obj.RSSISample("00:13:ce:95:e1:6f",[-57.0])
    rss22 = obj.RSSISample("00:13:ce:95:de:7e",[-77.0])
    rss23 = obj.RSSISample("00:13:ce:8f:78:d9",[-37.0])
    fp2 = obj.Fingerprint(loc2,obj.FingerprintSample([rss21,rss22,rss23]))

    expectFgdb.db.append(fp2)
    
    loc3 = obj.SimpleLocation(5.40,29.59,3.20)
    rss31 = obj.RSSISample("00:13:ce:97:78:79",[-84.0])
    rss32 = obj.RSSISample("00:13:ce:8f:77:43",[-61.0])
    rss33 = obj.RSSISample("00:13:ce:95:e1:6f",[-57.0])
    rss34 = obj.RSSISample("00:13:ce:8f:78:d9",[-24.0])
    fp3 = obj.Fingerprint(loc3,obj.FingerprintSample([rss31,rss32,rss33,rss34]))

    expectFgdb.db.append(fp3)
    assert fgdb == expectFgdb

#Test if the parser parse several lines correctly with several mac adresses and several RSSI per mac address and one line per point

def test_parser_several_lines_several_rssi():
    fgdb = obj.FingerprintDatabase()
    parser = obj.Parser("test/ressource/SeveralLineSeveralRSSI.csv",fgdb)
    
    loc1 = obj.SimpleLocation(5.40,29.59,1.20)
    rss12 = obj.RSSISample("00:13:ce:97:78:79",[-63.,-80.0])
    rss13 = obj.RSSISample("00:13:ce:8f:78:d9",[-29.0])
    fp1 = obj.Fingerprint(loc1,obj.FingerprintSample([rss12,rss13]))
    expectFgdb = obj.FingerprintDatabase()
    expectFgdb.db.append(fp1)

    loc2 = obj.SimpleLocation(6.40,29.59,1.20)
    rss21 = obj.RSSISample("00:13:ce:95:e1:6f",[-57.0])
    rss23 = obj.RSSISample("00:13:ce:8f:78:d9",[-77.,-37.0])
    fp2 = obj.Fingerprint(loc2,obj.FingerprintSample([rss21,rss23]))

    expectFgdb.db.append(fp2)
    
    loc3 = obj.SimpleLocation(5.40,29.59,3.20)
    rss31 = obj.RSSISample("00:13:ce:97:78:6f",[-84.0])
    rss32 = obj.RSSISample("00:13:ce:8f:77:43",[-61.0,-24.0])
    fp3 = obj.Fingerprint(loc3,obj.FingerprintSample([rss31,rss32]))

    expectFgdb.db.append(fp3)
    assert fgdb == expectFgdb

#Test if the parser parse several lines correctly with several mac adresses and several RSSI per mac address and several lines per point

def test_parser_several_lines_several_rssi_several_lines():
    fgdb = obj.FingerprintDatabase()
    parser = obj.Parser("test/ressource/SeveralLineSeveralRSSIonePoint.csv",fgdb)
    expectFgdb = obj.FingerprintDatabase()


    loc1 = obj.SimpleLocation(5.40,29.59,1.20)
    rss12 = obj.RSSISample("00:13:ce:97:78:79",[-63.,-80.0])
    rss13 = obj.RSSISample("00:13:ce:8f:78:d9",[-29.0,-77.,-37.0])
    rss21 = obj.RSSISample("00:13:ce:95:e1:6f",[-57.0,-84.0])
    rss32 = obj.RSSISample("00:13:ce:8f:77:43",[-61.0,-24.0])
    
    fp = obj.Fingerprint(loc1,obj.FingerprintSample([rss12,rss13,rss21,rss32]))
    expectFgdb.db.append(fp)
    assert fgdb == expectFgdb

#Test if the parser compute well the mean of the RSSI

def test_parser_compute_mean():
    fgdb = obj.FingerprintDatabase()
    parser = obj.Parser("test/ressource/SeveralLineSeveralRSSIonePoint.csv",fgdb)
    for fp in fgdb.db:
        for rssi in fp.sample.samples:
            rssi.setAverageRssi()
    expectFgdb = obj.FingerprintDatabase()


    loc1 = obj.SimpleLocation(5.40,29.59,1.20)
    rss12 = obj.RSSISample("00:13:ce:97:78:79",[-63.,-80.0])
    rss12.rssi = 10 ** (-71.5 / 10.)
    rss13 = obj.RSSISample("00:13:ce:8f:78:d9",[-29.0,-77.,-37.0])
    rss13.rssi = 10 ** ((-143/3) / 10.)
    rss21 = obj.RSSISample("00:13:ce:95:e1:6f",[-57.0,-84.0])
    rss21.rssi = 10 ** (-70.5 / 10.)
    rss32 = obj.RSSISample("00:13:ce:8f:77:43",[-61.0,-24.0])
    rss32.rssi = 10 ** (-42.5 / 10.)
        
    fp = obj.Fingerprint(loc1,obj.FingerprintSample([rss12,rss13,rss21,rss32]))
    expectFgdb.db.append(fp)
    assert fgdb == expectFgdb