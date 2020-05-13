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
        self.bet = 0
    
    def print_bank(self):
        if self.bank <= 0:
            place = randint(0,3)
            place_array = ["in their pants", "on the ground", "stuck to their shoe", "in the back of a taxi"]
            print(f"{self.name} found $2 {place_array[place]}! What luck!")
            self.bank = 2
        print(f"{self.name} bank: ${self.bank}")
        return self
        

def draw_board():
    dealer_hand = " ".join(card.__repr__() for card in dealer.hand)
    # for player in players:
    #     player_hand = " ".join(card.__repr__() for card in player.hand)
    
    print()
    print("|-------------------------------------------------|")
    print(f"|   Dealer: {dealer_hand:38}|")
    print("|-------------------------------------------------|")
    print("|            BLACKJACK PAYS 3 TO 2                |")
    print("|             DEALER STAYS ON 17                  |")
    print("|-------------------------------------------------|")
    for player in players:
        print(f"|   {player.name}: {' '.join(card.__repr__() for card in player.hand):37}|")
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

def player_turn(deck, person):
    if (len(person.hand) == 2 and value_check(person)[1] == 21):
        print(f"\nBlackjack, {person.name}!")
        person.bank += person.bet*1.5//1
        print(f"{person.name} win ${person.bet*1.5//1}")
        person.status = "blackjack"
        return
    
    valid_choice = False
    while not valid_choice:
        player_choice = input(f"\n{person.name}, (S)tay or (H)it: ")
        if player_choice.upper() in ("S", "H"):
            valid_choice = True
        else:
            print("Invalid selection")

    if player_choice.upper() == 'H':
        person.hand.append(deck.deal_top_card())
        draw_board()
        if value_check(person)[0] == "bust":
            person.status = "bust"
            print(f"{person.name} busts!")
            print(f"{person.name} lose ${person.bet//1}")
            person.bank -= person.bet
            return
        player_turn(deck, person)
    elif player_choice.upper() == 'S':
        return

def dealer_turn(deck, dealer):
    if value_check(dealer)[0] == "hit":
        dealer.hand.append(deck.deal_top_card())
        print("\nDealer hits")
        draw_board()
        if value_check(dealer)[0] == "bust":
            print("Dealer busts!")

            for player in players:
                if player.status == "fine":
                    print(f"{player.name} win ${player.bet//1}")
                    player.bank += player.bet
            return
        dealer_turn(deck, dealer)
    elif value_check(dealer)[0] == "stay":
        print("\nDealer stays")
        draw_board()

def winners():
    for player in players:
        if player.status not in ("bust", "blackjack"):
            if value_check(dealer)[0] != "bust":
                if value_check(player)[1] > value_check(dealer)[1]:
                    print(f"\n{player.name} wins vs dealer!")
                    print(f"{player.name} win ${player.bet//1}")
                    player.bank += player.bet
                elif value_check(player)[1] < value_check(dealer)[1]:
                    print(f"\nDealer wins vs {player.name}!")
                    print(f"{player.name} lose ${player.bet//1}")
                    player.bank -= player.bet
                else:
                    print(f"Dealer pushes vs {player.name}")
        


# Primary game loop

def new_deal():
    new_deck = Deck()

    dealer.hand = []
    dealer.hand.append(new_deck.deal_top_card())
    dealer.hand.append(new_deck.deal_top_card())
    dealer.hand[1].hidden = True

    for player in players:
        player.status = "fine"
        player.hand = []
        player.hand.append(new_deck.deal_top_card())
        player.hand.append(new_deck.deal_top_card())
        player.print_bank()

        valid_bet = False
        while not valid_bet:
            try:
                player.bet = int(input(f"{player.name}, enter wager (even amounts please): "))
            except:
                print("Number, please")
                player.bet = 0
            if player.bet <= player.bank and player.bet > 0:
                valid_bet = True
                print()
            else:
                print ("Invalid wager")

    draw_board()

    for player in players:
        player_turn(new_deck, player)

    dealer.hand[1].hidden = False
    finished_players = 0

    for player in players:
        if player.status in ("bust", "blackjack"):
            finished_players += 1
    if finished_players < len(players):
        dealer_turn(new_deck, dealer)
    
    winners()
    print()
    
    for player in players:
        player.print_bank()
    
    again = input("\nPlay again (Y/N)?")
    if again.upper() == ("Y"):
        new_deal()
    else:
        return


# Player selection

valid_num = False
player_num = 0
while not valid_num:
    try:
        player_num = int(input("How many players (1-4): "))
    except:
        print("Number, please")
    if player_num >= 1 and player_num <= 4:
        valid_num = True
        print()
    else:
        print("Invalid entry")

dealer = Player("Dealer")
players = []
for i in range(0, player_num):
    players.append(Player("Player"+str(i+1)))
new_deal()