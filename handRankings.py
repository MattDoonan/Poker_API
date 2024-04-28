from itertools import combinations
from collections import Counter

cardValue = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}

def checkPairing(cards, isOwnHand):
    """
        Checks if the cards can make up any type of pairing
        Modifies potential hands if it is possible for the player to make any higher pairing
        returns the hand strenght
    """
    potentialHands = []
    numberOfCardValues = Counter(value for value, _ in cards)
    maxNumber = secondMax = 0
    maxNumberKey = 0
    for key, value in numberOfCardValues.items():
        if value > maxNumber and key > maxNumberKey:
            secondMax = maxNumber
            maxNumber = value
            maxNumberKey = key
        elif value > secondMax:
            secondMax = value
            if secondMax == maxNumber and key > maxNumberKey:
                maxNumberKey = key

    if maxNumber >= 4:
        return maxNumberKey + (13 * 7), potentialHands
    elif maxNumber >= 3 and secondMax >= 2:
        if 7 - len(cards) + 3 >= 4 and isOwnHand:
            potentialHands.append("Four of a kind")
        return maxNumberKey + (13 * 6), potentialHands
    elif maxNumber == 3:
        if 7 - len(cards) + 3 >= 4 and isOwnHand:
            potentialHands.append("Four of a kind")
        if 7 - len(cards) + 3 >= 5 and isOwnHand:
            potentialHands.append("Full house")
        return maxNumberKey + (13 * 3), potentialHands
    elif maxNumber == 2 and secondMax == 2:
        if 7 - len(cards) + 4 >= 5 and isOwnHand:
                potentialHands.append("Full house")
        if 7 - len(cards) + 2 >= 3 and isOwnHand:
                potentialHands.append("Three of a kind")
        return maxNumberKey + (13 * 2), potentialHands
    elif maxNumber == 2:
        if 7 - len(cards) + 2 >= 3 and isOwnHand:
            potentialHands.append("Three of a kind")
            potentialHands.append("Two pair")
        return maxNumberKey + 13, potentialHands
    if 7 - len(cards) + 1 >= 2 and isOwnHand:
        potentialHands.append("Pair")
    return max(value for value, _ in cards), potentialHands
    

def checkStraightOrFlush(cards, isOwnHand):
    """
        Checks if the cards can make up a flush of a straight
        Modifies potential hands if it is possible for the player to make a flush or straight with the remaining hands
        returns the hand strenght
    """
    potentialHands = []
    sortedCards = sorted(cards, key=lambda x: x[0])
    suiteCount = {'C': 0, 'S': 0, 'H': 0, 'D': 0}
    for _, letter in sortedCards:
        suiteCount[letter] += 1
    isFlush = None
    inARow = []
    potentialInARow = []
    doNotAdd = False
    for i in range(1, len(sortedCards)):
        if sortedCards[i][0] == sortedCards[i - 1][0] + 1 and not doNotAdd:
            if len(inARow) == 0:
                inARow.append(sortedCards[i-1])
                inARow.append(sortedCards[i])
                potentialInARow.append(sortedCards[i-1])
                potentialInARow.append(sortedCards[i])
            elif len(inARow) >= 5:
                inARow.pop(0)
                inARow.append(sortedCards[i])
            else:
                inARow.append(sortedCards[i])
                potentialInARow.append(sortedCards[i])
        elif sortedCards[i][0] != sortedCards[i - 1][0]:
            if len(inARow) != 5:
                inARow = []
            else:
                doNotAdd = True
            if isOwnHand and len(cards) > 4:
                addedPot = False
                resetLoop = False
                skipped = 0
                for y in range(7 - len(cards) - skipped):
                    if sortedCards[i][0] == sortedCards[i - 1][0] + 2 + y:
                        addedPot = True
                        skipped += 1
                        y = 7 - len(cards) - skipped
                        if len(potentialInARow) == 0:
                            potentialInARow.append(sortedCards[i-1])
                            potentialInARow.append(sortedCards[i])
                        else:
                            potentialInARow.append(sortedCards[i])

                    if not addedPot and len(potentialInARow) + 7 - len(cards) < 5 and not resetLoop:
                        potentialInARow = []
                        skipped = 0
                        y = 1
                        resetLoop = True
    if 7 - len(cards) == 0:
        potentialInARow = []
    for key, value in suiteCount.items(): 
        if value >= 5:
            isFlush = key
            if 'Flush' in potentialHands:
                potentialHands.remove('Flush')
        elif 7 - len(cards) + value >= 5 and isOwnHand and len(cards) > 2 and 'Flush' not in potentialHands:
            potentialHands.append('Flush')
    if (7 - len(cards) + len(potentialInARow) >= 5 and isOwnHand and len(cards) > 2 and len(inARow) < 5):
        potentialHands.append('Straight')
    if (len(inARow) == 5 and isFlush != None):
        numInRow = sum(1 for value1, _ in inARow for value2, suite2 in sortedCards if value1 == value2 and suite2 == isFlush)
        if numInRow == 5:
            if all(item[0] == num for item, num in zip(inARow, [9, 10, 11, 12, 13])):
                return 130, potentialHands
            return inARow[-1][0] + (13 * 8), potentialHands
    if (isFlush):
        return max(value for value, suite in sortedCards if suite == isFlush) + (13 * 5), potentialHands
    elif (len(inARow) == 5):
        return inARow[-1][0] + (13 * 4), potentialHands
    return 0, potentialHands



def calculateHandRanking(cards, isOwnHand):
    """
        Calculates the hand rankings based of cards given
        if is a players hand then adds potential hands
    """
    potentialHands = []
    cardValSuite = []
    for card in cards:
        cardValSuite.append((cardValue[card[:-1]], card[-1:]))
    possiblePairingVal, pairingPotentialHands = checkPairing(cardValSuite, isOwnHand)
    possibleStraightOrFlushVal, flushStraightPotentialHands = checkStraightOrFlush(cardValSuite, isOwnHand)
    if possiblePairingVal < 14 and possibleStraightOrFlushVal > 0:
        potentialHands = flushStraightPotentialHands
    elif len(cards) >= 5:
        potentialHands = pairingPotentialHands + flushStraightPotentialHands
    else:
        potentialHands = pairingPotentialHands
    return max(possiblePairingVal, possibleStraightOrFlushVal), potentialHands


def getHandRanking(playersHand, sharedCards):
    """
        Returns how strong the players hand it compared to all other possible hands
    """
    revealedCards = playersHand + sharedCards
    if len(revealedCards) >= 2:
        ahead = 0
        tied = 0
        behind = 0
        playersRank, potentialHands = calculateHandRanking(revealedCards, True)
        fullDeck = ['10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']
        for card in revealedCards:
            fullDeck.remove(card)
        combinationOfTwo = list(combinations(fullDeck, 2))
        for combination in combinationOfTwo:
            possibility = sharedCards + list(combination)
            opponentsHand, _ = calculateHandRanking(possibility, False)
            if playersRank > opponentsHand:
                ahead += 1
            elif playersRank == opponentsHand:
                tied += 1
            else:
                behind += 1
        value = ((ahead + tied / 2) / (ahead + tied + behind)) * 100
        hand_strength = "Just Fold"
        if 90 <= value:
            hand_strength = "Very Strong"
        elif 80 <= value < 90:
            hand_strength = "Strong"
        elif 70 <= value < 80:
            hand_strength = "Solid"
        elif 60 <= value < 70:
            hand_strength = "Above average"
        elif 40 <= value < 60:
            hand_strength = "Average"
        elif 30 <= value < 40:
            hand_strength = "Below Average"
        elif 20 <= value < 30:
            hand_strength = "Weak"
        elif 10 <= value < 20:
            hand_strength = "Extremely Weak"
        return hand_strength, potentialHands
