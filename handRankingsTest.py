import unittest
import handRankings

class TestCheckPairing(unittest.TestCase):
    def test_four_of_a_kind(self):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (2, 'S'), (5, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + (13 * 7))  # Four of a kind (2)
        self.assertEqual(potentialHands, []) 

    def test_full_house(self):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (3, 'S'), (3, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + (13 * 6))  # Full house (2)
        self.assertEqual(potentialHands, ['Four of a kind']) 

    def test_full_house_no_potential(self):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (3, 'S'), (3, 'C'), (4, 'S'), (4, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + (13 * 6))  # Full house (2)
        self.assertEqual(potentialHands, []) 

    def test_three_of_a_kind(self):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (3, 'S'), (5, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + (13 * 3))  # Three of a kind (2)
        self.assertEqual(potentialHands, ['Four of a kind', 'Full house']) 

    def test_three_of_a_kind_no_potential(self):
        cards = [(2, 'C'), (2, 'D'), (2, 'H'), (3, 'S'), (5, 'C'), (6, 'S'), (7, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + (13 * 3))  # Three of a kind (2)
        self.assertEqual(potentialHands, []) 

    def test_two_pair(self):
        cards = [(2, 'C'), (2, 'D'), (3, 'H'), (3, 'S'), (5, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 3 + (13 * 2))  # Two pair (3, 2)
        self.assertEqual(potentialHands, ['Full house', 'Three of a kind']) 

    def test_two_pair_no_potential(self):
        cards = [(2, 'C'), (2, 'D'), (3, 'H'), (3, 'S'), (5, 'C'), (7, 'C'), (8, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 3 + (13 * 2))
        self.assertEqual(potentialHands, []) 

    def test_pair(self):
        cards = [(2, 'C'), (2, 'D'), (5, 'H'), (3, 'S'), (9, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + 13)  # Two pair (2)
        self.assertEqual(potentialHands, ['Three of a kind', 'Two pair']) 

    def test_pair_no_potential(self):
        cards = [(2, 'C'), (2, 'D'), (3, 'H'), (4, 'S'), (5, 'C'), (6, 'H'), (7, 'H')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 2 + 13)  # Two pair (2)
        self.assertEqual(potentialHands, []) 

    def test_high_card(self):
        cards = [(2, 'C'), (4, 'D'), (7, 'H'), (8, 'S'), (10, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 10)  # High card (10)
        self.assertEqual(potentialHands, ['Pair']) 

    def test_high_card_no_potential(self):
        cards = [(2, 'C'), (3, 'D'), (4, 'H'), (5, 'S'), (6, 'C'), (7, 'C'), (8, 'C')]
        isOwnHand = True
        rankings, potentialHands = handRankings.checkPairing(cards, isOwnHand)
        self.assertEqual(rankings, 8)  # High card (8)
        self.assertEqual(potentialHands, []) 


class TestCheckStraightOrFlush(unittest.TestCase):


    def test_flush(self):
        # Test case where a flush is present
        cards = [(2, 'C'), (3, 'C'), (4, 'C'), (9, 'C'), (11, 'C'), (8, 'S'), (9, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 11 + (13 * 5))  # Assuming that the flush strength is 82
        self.assertEqual(potential_hands, [])

    def test_flush_potential_straight(self):
        # Test case where a flush is present
        cards = [(2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (11, 'C')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 11 + (13 * 5)) 
        self.assertEqual(potential_hands, ['Straight'])

    def test_straight(self):
        # Test case where a straight is present
        cards = [(2, 'C'), (3, 'D'), (4, 'S'), (5, 'C'), (6, 'H'), (8, 'S'), (9, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 6 + (13 * 4))  # Assuming that the straight strength is 104
        self.assertEqual(potential_hands, [])

    def test_straight_potential_flush(self):
        # Test case where a straight is present
        cards = [(2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 6 + (13 * 4))  # Assuming that the straight strength is 104
        self.assertEqual(potential_hands, ['Flush'])

    def test_full_house(self):
        # Test case where both straight and flush are present
        cards = [(9, 'C'), (10, 'C'), (11, 'C'), (12, 'C'), (13, 'C'), (8, 'S'), (9, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 130)  # Assuming that the straight flush strength is 130
        self.assertEqual(potential_hands, [])


    def test_straight_flush(self):
        # Test case where both straight and flush are present
        cards = [(8, 'C'), (9, 'C'), (10, 'C'), (11, 'C'), (12, 'C'), (8, 'S'), (9, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 12 + (13 * 8))  # Assuming that the straight flush strength is 130
        self.assertEqual(potential_hands, [])

    def test_no_straight_or_flush(self):
        # Test case where neither straight nor flush is present
        cards = [(2, 'C'), (3, 'D'), (4, 'S'), (7, 'C'), (8, 'H'), (10, 'S'), (12, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 0)
        self.assertEqual(potential_hands, [])

    def test_potential_hands(self):
        # Test case where potential hands are identified
        cards = [(2, 'C'), (4, 'C'), (5, 'S'), (9, 'C'), (12, 'H')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 0)  # Assuming that the flush strength is 82
        self.assertEqual(potential_hands, ['Flush', 'Straight'])

    def test_potential_straight(self):
        # Test case where potential hands are identified
        cards = [(1, 'H'), (4, 'S'), (5, 'S'), (6, 'C'), (8, 'H'), (8, 'D')]
        result, potential_hands = handRankings.checkStraightOrFlush(cards, True)
        self.assertEqual(result, 0)  # Assuming that the flush strength is 82
        self.assertEqual(potential_hands, ['Straight'])


class TestHandRanking(unittest.TestCase):

    def test_high_card(self):
        cards = ["KD", "7D"]
        result, potential_hands = handRankings.calculateHandRanking(cards, True)
        self.assertEqual(result, 12) 
        self.assertEqual(potential_hands, ['Pair'])

    def test_straight_potential_flush(self):
        cards = ["5D", "7D", "6C", "8D", "KD", "4H"]
        result, potential_hands = handRankings.calculateHandRanking(cards, True)
        self.assertEqual(result, 7 + (13 * 4)) 
        self.assertEqual(potential_hands, ['Flush'])

    def test_pair_potential_straight_flush(self):
        cards = ["5D", "5D", "6C", "8D", "KD", "4H"]
        result, potential_hands = handRankings.calculateHandRanking(cards, True)
        self.assertEqual(result, 4 + 13) 
        self.assertEqual(potential_hands, ['Three of a kind', 'Two pair', 'Flush', 'Straight'])

    def test_three_of_a_kind(self):
        cards = ["5D", "5D", "5C", "8D", "KD", "4H"]
        result, potential_hands = handRankings.calculateHandRanking(cards, True)
        self.assertEqual(result, 4 + (13 * 3)) 
        self.assertEqual(potential_hands, ['Four of a kind', 'Flush'])


class TestGetHandRankinf(unittest.TestCase):

    def test_strong_hand(self):
        playersHand = ["AD", "KD"]
        board = ["QD", "JD", "10D", "2H", "3D"]
        hand_strength, potentialHands = handRankings.getHandRanking(playersHand, board)
        self.assertEqual(hand_strength, "Very Strong")
        self.assertEqual(potentialHands, [])

    def test_very_weak_hand(self):
        playersHand = ["2S", "3H"]
        board = ["QD", "JD", "10D", "8H", "4D"]
        hand_strength, potentialHands = handRankings.getHandRanking(playersHand, board)
        self.assertEqual(hand_strength, "Extremely Weak")
        self.assertEqual(potentialHands, [])

    def test_potential_straight(self):
        playersHand = ["6S", "9H"]
        board = ["7D", "JC", "10D"]
        hand_strength, potentialHands = handRankings.getHandRanking(playersHand, board)
        self.assertEqual(hand_strength, "Extremely Weak")
        self.assertEqual(potentialHands, ["Pair", "Straight"])

if __name__ == '__main__':
    unittest.main()