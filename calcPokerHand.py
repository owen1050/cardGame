hand = ["D10", "D11", "D9", "D13", "D12", "D8"]



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
        return True, highest5(sCard)
    if len(dCard) >= 5:
        return True, highest5(dCard)
    if len(cCard) >= 5:
        return True, highest5(cCard)
    if len(hCard) >= 5:
        return True, highest5(hCard)

def isStraight(handIn):
    hand= inNumOrder(handIn)
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))

    #no low ace straight support
    vals.sort(reverse = True)
    
    i = 0
    i0 = 0
    i1 = 0
    while i < len(vals)-1 and i1 - i0 < 4:
        if vals[i] - 1 == vals[i + 1]:
            i1 = i1 + 1
        else:
            i0 = i0 + 1
            i1 = i0
        i = i + 1
    if i1-i0 == 4:
        vals = vals[i0:i1+1]
        oh = []
        hc = hand.copy()
        for v in vals:
            for card in hc:
                vi = int(card[1:])
                if v == vi:
                    oh.append(card)
                    hc.remove(card)
                    break
        return True, inNumOrder(oh)
    else:
        return False

def isRoyal(hand):
    vals = []
    for card in hand:
        v = card[1:]
        vals.append(int(v))
    return min(vals)==10

def isRoyalFlush(hand):

    st, h1 = isStraight(hand)
    fl, h2 = isFlush(h1)
    if isRoyal(h2) and fl and st:
        return True, h2
    return False

def isStraightFlush(hand):
    st, h1 = isStraight(hand)
    fl, h2 = isFlush(h1)
    if fl and st:
        return True, h2
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

def highest5(hand):
    if len(hand) == 5:
        return hand
    else:
        nh = hand.copy()
        vals = []
        for card in hand:
            v = card[1:]
            vals.append(int(v))

        while len(vals) > 5:
            m = min(vals)
            i = vals.index(m)
            vals.pop(i)
            nh.pop(i)
        return nh

print(isStraightFlush(hand))