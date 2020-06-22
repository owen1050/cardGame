from collections import Counter
from itertools import combinations


def isFlush(hand):
    sCard = []
    hCard = []
    dCard = []
    cCard = []
    for card in hand:
        if card[0] == "H":
            hCard.append(card)
        if card[0] ==  "D":
            dCard.append(card)
        if card[0] == "C":
            cCard.append(card)
        if card[0] == "S":
            sCard.append(card)

    if len(sCard) >= 5:
        return True
    if len(dCard) >= 5:
        return True
    if len(cCard) >= 5:
        return True
    if len(hCard) >= 5:
        return True

def isStraight(handIn):
    hand= inNumOrder(handIn)
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    #no low ace straight support
    vals.sort(reverse = True)
    print(vals)
    if vals == [14, 5, 4, 3, 2]:
        return True
    for i in vals:
        cv = 0
        sc = True
        while cv < 5:
            if((i - cv) in vals):
                pass
            else:
                sc = False
                break
            cv = cv + 1
        if(sc):
            return True


    else:
        return False

def isRoyal(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))
    return min(vals)==10

def isRoyalFlush(hand):

    st= isStraight(hand)
    fl = isFlush(hand)
    if isRoyal(hand) and fl and st:
        return True
    return False

def isStraightFlush(hand):
    st = isStraight(hand)
    fl = isFlush(hand)
    if fl and st:
        return True
    return False

def inNumOrder(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    vals.sort()
    oh = []
    hc = hand.copy()
    for v in vals:
        for card in hc:
            vi = int(card[1:])
            if v == vi:
                oh.append(card)
                hc.remove(card)
                break
    return oh

def isFullHouse(hand):
    return isNOfAKind(hand, 3) and isNOfAKind(hand, 2)

def isNOfAKind(hand, n):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    for v in cnt:
        if(cnt[v] == n):
            return True               
    return False

def isTwoPair(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    twoCount = 0
    for v in cnt:
        if(cnt[v] == 2):
            twoCount = twoCount + 1        
    return twoCount == 2

def valueOfHighN(hand, n):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    vals.sort(reverse= True)

    return vals[0] + vals[1]

def valueOfLow1(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    vals.sort()
    if(vals[4] == 14):
        return 1

    return vals[0]

def valueOf4OfAKind(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    v4 = 0
    v1 = 0
    for v in cnt:
        if(cnt[v] == 4):
            v4 = v
        else:
            v1 = v
    return v4, v

def valueOfFH(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    v3 = 0
    v2 = 0
    for v in cnt:
        if(cnt[v] == 3):
            v3 = v
        else:
            v2 = v
    return v3, v2

def valueOf3(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    v3 = 0
    for v in cnt:
        if(cnt[v] == 3):
            v3 = v
    return v3

def valueOf2Pair(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    v2= []
    v3 = 0
    for v in cnt:
        if(cnt[v] == 2):
            v2.append(v)
        else:
            v3 = v
    v0 = max(v2)
    v1 = min(v2)

    return v0 * 20 + v1 + v3/20

def valueOf2(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    cnt = Counter(vals)
    vp=0
    vals = []
    for v in cnt:
        if(cnt[v] == 2):
            vp = v
        else:
            vals.append(v)
    
    vals.sort(reverse= True)
    v0 = vals[0] * 65000
    v1 = vals[1] * 4500
    v2 = vals[2] * 300

    return vp + (v0 + v1 + v2)/1000000


def tiebreakerCalc(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    vals.sort(reverse = True)

    v0 = vals[0] * 65000
    v1 = vals[1] * 4500
    v2 = vals[2] * 300
    v3 = vals[3] * 20
    v4 = vals[4]

    return (v0 + v1 + v2 + v3 + v4)/1000000

def calcSingleVal(hand):
    if(isRoyalFlush(hand)):
        return 6000

    if(isStraightFlush(hand)):
        return 5000 + valueOfLow1(hand)

    if(isNOfAKind(hand, 4)):
        v4, v1 = valueOf4OfAKind(hand)
        return 4000 + v4 + v1/20

    if(isFullHouse(hand)):
        v3, v2 = valueOf4OfAKind(hand)
        return 3000+  v3 + v2/20

    if(isFlush(hand)):
        return 2000 + tiebreakerCalc(hand)

    if(isStraight(hand)):
        return 1000 + valueOfLow1(hand)

    if(isNOfAKind(hand, 3)):
        return 750 + valueOf3(hand)

    if(isTwoPair(hand)):
        return 100 + valueOf2Pair(hand)

    if(isNOfAKind(hand, 2)):
        return 14 + valueOf2(hand)

    return tiebreakerCalc(hand)

def calcValue(hand):
    hands = combinations(hand, 5)

    maxScore = 0
    for h2 in hands:
        h = list(h2)
        score = calcSingleVal(h)
        if score > maxScore:
            maxScore = score
    return maxScore

