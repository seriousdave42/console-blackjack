from random import randint

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if value == 1:
            self.rank = 'A'
        elif value == 10:
            self.rank = 'T'
        elif value == 11:
            self.rank = 'J'
        elif value == 12:
            self.rank = 'Q'
        elif value == 13:
            self.rank = 'K'
        elif value == 0:
            self.rank = ' '
        else:
            self.rank = str(value)
        self.hidden = False

    def greater_than(self, other_card):
        return self.value > other_card.value
        
    def __repr__(self):
        if self.hidden:
            return("XX")
        else:
            return(f"{self.rank}{self.suit}")

            
class Deck():
    
    def __init__(self):
        self.suits = ['H', 'D', 'S', 'C']
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.contents = []
    
        for suit in self.suits:
            for value in self.values:
                self.contents.append(Card(suit, value))
        
        self.shuffle_deck()
        
    def shuffle_deck(self):
        for i in range(0, len(self.contents)):
            x = randint(0, len(self.contents) - 1)
            self.contents[i], self.contents[x] = self.contents[x], self.contents[i]
            
    def deal_top_card(self):
        try:
            return self.contents.pop(0)
        except:
            print('Deck is empty!')
            return None
            
    def add_to_bottom(self, card):
        self.contents.append(card)
        
    def add_to_top(self, card):
        self.contents.insert(0, card)

class Player():

    def __init__(self, name):
        self.name = name
        self.bank = 2000
        self.hand = []
        self.status = "fine"

def draw_board():
    dealer_hand = " ".join(card.__repr__() for card in dealer.hand)
    player_hand = " ".join(card.__repr__() for card in player.hand)
    
    print()
    print("|-------------------------------------------------|")
    print(f"|   Dealer: {dealer_hand:38}|")
    print("|-------------------------------------------------|")
    print("|            BLACKJACK PAYS 3 TO 2                |")
    print("|             DEALER STAYS ON 17                  |")
    print("|-------------------------------------------------|")
    print(f"|   Player: {player_hand:38}|")
    print("|-------------------------------------------------|")
    print()

def value_check(person):
    hand_total = 0
    ace_count = 0

    for card in person.hand:
        if card.rank in ('T', 'J', 'Q', 'K'):
            hand_total += 10
        elif card.rank == 'A':
            if ace_count == 0:
                hand_total += 11
                ace_count += 1
            else:
                hand_total += 1
        else:
            hand_total += card.value
    
    if (hand_total - min(ace_count,1) * 10) > 21:
        person.status = "bust"
        return ["bust", hand_total]
    elif (person.name == "Dealer") and ((hand_total < 17) or (hand_total > 21 and (hand_total - min(ace_count,1)*10) < 17)):
        return ["hit", hand_total]
    else:
        while hand_total > 21:
            hand_total = hand_total -10
        return ["stay", hand_total]

def player_turn(deck, person, wager):
    if (len(person.hand) == 2 and value_check(person)[1] == 21):
        print("Blackjack!")
        person.bank += wager*1.5//1
        print(f"Win ${wager*1.5//1}")
        print(f"Player bank: ${person.bank}\n")
        person.status = "blackjack"
        return
    
    valid_choice = False
    while not valid_choice:
        player_choice = input("(S)tay or (H)it: ")
        if player_choice.upper() in ("S", "H"):
            valid_choice = True
        else:
            print("Invalid selection")

    if player_choice.upper() == 'H':
        person.hand.append(deck.deal_top_card())
        draw_board()
        if value_check(person)[0] == "bust":
            person.status = "bust"
            print("Player busts!")
            print(f"Lose ${wager//1}")
            person.bank -= wager
            print(f"Player bank: {person.bank}\n")
            return
        player_turn(deck, person, wager)
    elif player_choice.upper() == 'S':
        return

def dealer_turn(deck, dealer, person, wager):
    if value_check(dealer)[0] == "hit":
        dealer.hand.append(deck.deal_top_card())
        print("\nDealer hits")
        draw_board()
        if value_check(dealer)[0] == "bust":
            print("Dealer busts!")
            print(f"Win ${wager//1}")
            player.bank += wager
            return
        dealer_turn(deck, dealer, person, wager)
    elif value_check(dealer)[0] == "stay":
        print("Dealer stays")
        draw_board()

def winners(wager):
    if value_check(player)[0] != "bust":
        if value_check(dealer)[0] != "bust":
            if value_check(player)[1] > value_check(dealer)[1]:
                print("Player wins!")
                print(f"Win ${wager//1}")
                player.bank += wager
            elif value_check(player)[1] < value_check(dealer)[1]:
                print("Dealer wins!")
                print(f"Lose ${wager//1}")
                player.bank -= wager
            else:
                print("Push")
    print(f"Player bank: ${player.bank//1}\n")

def new_deal():
    new_deck = Deck()
    player.status = "fine"
    valid_bet = False

    dealer.hand = []
    dealer.hand.append(new_deck.deal_top_card())
    dealer.hand.append(new_deck.deal_top_card())
    dealer.hand[1].hidden = True

    player.hand = []
    player.hand.append(new_deck.deal_top_card())
    player.hand.append(new_deck.deal_top_card())
    # player.hand.append(Card('H', 1))
    # player.hand.append(Card('H', 13))


    print(f"\nPlayer bank: ${player.bank//1}")

    while not valid_bet:
        try:
            bet = int(input("Enter wager (even amounts please): "))
        except:
            print("Invalid entry")
            bet = 0
        if bet <= player.bank and bet > 0:
            valid_bet = True
        else:
            print ("Try again")
    
    draw_board()
    player_turn(new_deck, player, bet)
    dealer.hand[1].hidden = False
    if player.status not in ("bust", "blackjack"):
        dealer_turn(new_deck, dealer, player, bet)
        winners(bet)
    if player.bank <= 0:
        print("Your are bankrupt!")
        print("You found $2 on the ground! What luck!")
        player.bank = 2
    again = input("Play again (Y/N)?")
    if again.upper() == ("Y"):
        new_deal()
    else:
        return

dealer = Player("Dealer")
player = Player("Player")
new_deal()