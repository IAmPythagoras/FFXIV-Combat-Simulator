from math import floor

def getDet(x):
    return floor(1000+floor(140*(x-baseMain)/levelMod))/1000

def getDH(x):
    return floor(550*floor(x-baseSub)/levelMod)/1000 # DH rate in decimal

levelMod = 1900
baseMain = 390  
baseSub = 400# Level 90 LevelMod values

detDiff = getDet(2177) - getDet(2141)
dhDiff = (getDH(1580) - getDH(1544))
print("detDiff : " + str(detDiff))
print("dhDiff  : " + str(dhDiff/4))
