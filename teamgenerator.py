import random 

pitcherTraits = { 2 : 'S+, D+', 3 : 'S+', 4 : 'D+', 10 : 'P+', 11 : 'C+', 12 : 'P++' }

substituteTraits = { 2 : 'S+', 3 : 'C+', 11 : 'D+', 12 : 'P+' }

pitcherTraits = { 2 : 'GB+', 3 : 'K+', 11 : 'ST+', 12 : 'CN+' }

def getStarterAverage():
    return randint(10) + randint(10) + 15

def getSubstituteAverage():
    return randint(10) + 15

def getPitcherAverage():
    return randint(10) + 5

def getHandedness():
    roll = randint(10)
    if (roll < 7):
        return 'R'
    else if (roll < 10):
        return 'L'
    else:
        return 'S'



