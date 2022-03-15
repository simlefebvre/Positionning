import obj


fps = obj.FingerprintSample([obj.RSSISample("",100)])
print(fps.get_average_rssi())

obj.Parser("data.csv")