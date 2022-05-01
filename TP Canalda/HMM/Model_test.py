import obj

"""Test l'initialisation du model"""
# Test l'initialisation du model avec 0 état
def test_initModelWith0State():
    mod = obj.model(0)
    assert mod.totaux == []
    assert mod.totauxParCible == []
    assert mod.totauxParSource == []

#Test l'initialisation du model avec plusieurs états
def test_initModelWithSeveralStates():
    mod = obj.model(5)
    assert len(mod.totaux) == 5
    for i in range(5):
        assert len(mod.totaux[i]) == 5
    assert len(mod.totauxParCible) == 5
    assert len(mod.totauxParSource) == 5

"""Test l'ajout d'un mouvement"""
#Test l'ajout du premier mouvement
def test_addMovementWithFirstMovement():
    mod = obj.model(5)
    mod.addMovement(0,1)
    assert mod.totaux[1][0] == 1
    assert mod.totauxParCible[1] == 1
    assert mod.totauxParSource[0] == 1

#Test l'ajout d'un mouvement après un autre
def test_addMovementWithSeveralMovements():
    mod = obj.model(5)
    mod.addMovement(0,1)
    mod.addMovement(1,2)
    assert mod.totaux[2][1] == 1
    assert mod.totaux[1][0] == 1
    assert mod.totauxParCible[2] == 1
    assert mod.totauxParSource[1] == 1
    assert mod.totauxParCible[1] == 1
    assert mod.totauxParSource[0] == 1

#Test l'ajout d'un mouvement dans un état inexistant
def test_addMovementWithStateNotExist():
    mod = obj.model(5)
    mod.addMovement(5,1)
    assert mod.totaux[1][0] == 0
    assert mod.totauxParCible[1] == 0
    assert mod.totauxParSource[0] == 0

#Test l'ajout d'un second mouvement depuis le même état
def test_addMovementWithSameStartState():
    mod = obj.model(5)
    mod.addMovement(0,1)
    mod.addMovement(0,3)
    assert mod.totaux[0][1] == 1
    assert mod.totaux[0][3] == 1
    assert mod.totauxParCible[1] == 1
    assert mod.totauxParCible[3] == 1
    assert mod.totauxParSource[0] == 2

#Test l'ajout d'un second mouvement vers le même état
def test_addMovementWithSameEndState():
    mod = obj.model(5)
    mod.addMovement(0,1)
    mod.addMovement(4,1)
    assert mod.totaux[0][1] == 1
    assert mod.totaux[4][1] == 1
    assert mod.totauxParCible[1] == 2
    assert mod.totauxParSource[0] == 1
    assert mod.totauxParSource[4] == 1

#Test l'ajout d'un même mouvement deux fois
def test_addMovementWithSameMovementTwice():
    mod = obj.model(5)
    mod.addMovement(0,1)
    mod.addMovement(0,1)
    assert mod.totaux[0][1] == 2
    assert mod.totauxParCible[1] == 2
    assert mod.totauxParSource[0] == 2


"""Test la récupération de valeurs"""
#Test la récupération de valeurs avec un état source inexistant
def test_getValueWithSourceNotExist():
    mod = obj.model(5)
    mod.addMovement(0,1)
    assert mod.getValue(5,1) == None

#Test la récupération de valeurs avec un état cible inexistant
def test_getValueWithCibleNotExist():
    mod = obj.model(5)
    mod.addMovement(0,1)
    assert mod.getValue(0,5) == None

#Test la récupération des valeurs avec des état initiaux
def test_getValueWithInitialStates():
    mod = obj.model(5)
    assert mod.getValue(0,0) == (0,0,0)

#Test la récupération des valeurs avec des états modifiés
def test_getValueWithModifiedStates():
    mod = obj.model(5)
    mod.addMovement(0,1)
    mod.addMovement(1,3)
    mod.addMovement(3,2)
    mod.addMovement(2,1)
    mod.addMovement(1,0)
    mod.addMovement(0,1)

    assert mod.getValue(0,0) == (0,0,0)
    assert mod.getValue(0,1) == (2,1,2/3)
    assert mod.getValue(1,0) == (1,1/2,1)
    assert mod.getValue(1,3) == (1,1/2,1)
    assert mod.getValue(2,1) == (1,1,1/3)
    assert mod.getValue(3,2) == (1,1,1)