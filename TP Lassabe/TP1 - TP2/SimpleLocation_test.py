import obj

#test if two equal simple location are equal
def test_equalSimpleLocation():
    sl1 = obj.SimpleLocation(1,2,3)
    sl2 = obj.SimpleLocation(1,2,3)
    assert sl1 == sl2

#test if two different simple location are not equal
def test_notEqualSimpleLocation():
    sl1 = obj.SimpleLocation(1,2,3)
    sl2 = obj.SimpleLocation(1,3,3)
    assert sl1 != sl2
