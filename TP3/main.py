import obj


fps = obj.FingerprintSample([obj.RSSISample("",100)])
#print(fps.get_average_rssi())
fpdb = obj.FingerprintDatabase()
pars = obj.Parser("data.csv",fpdb)
pars.compute(fpdb)
obj.exportateur("export.csv",fpdb)