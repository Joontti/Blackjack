import random
import time

# Classic casino game coded in python

# Cards

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    
    def show(self):
        ranks = ["Jack", "Queen", "King", "Ace"]
        if self.value in range(11, 15):             # if the card is a Jack, Queen, King or an Ace
            print(f"{ranks[self.value - 11]} of {self.suit}")
        else:
            print(f"{self.value} of {self.suit}")

    def show_text(self):
        if self.value in range(11, 15):             # if the card is a Jack, Queen, King or an Ace
            ranks = ["Jack", "Queen", "King", "Ace"]
            self.ranks = ranks
            return f"{ranks[self.value - 11]} of {self.suit}"
        
        return f"{self.value} of {self.suit}"

    def rank(self):
        if self.value in range(11, 15):             # if the card is a Jack, Queen, King or an Ace
            ranks = ["Jacks", "Queens", "Kings", "Aces"]
            self.ranks = ranks
            return f"{ranks[self.value - 11]}"
        
        return f"{self.value}'s"


    def points(self, score):
        value = self.value
        if value == 11 or value == 12 or value == 13:       # if the card is a Jack, Queen or King
            return 10
        
        elif value == 14:   # if the card is an Ace
            if 11 + score > 21:
                return 1
    
            return 11
        else:               # else return face-value
            return value


class Deck:
    def __init__(self, cards):
        self.cards = cards   
        
        def build(self):
            for i in range(7):  # amount of decks which will be added
                for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
                    for value in range(2, 15):
                        self.cards.append(Card(s, value))
        if len(self.cards) == 0:
            build(self)
            self.shuffled = False
        
    def show(self):
        for c in self.cards:
            Card.show(c)

    def value_holder(self, shuffled):
        self.shuffled = shuffled

    def shuffle(self):          # To play BlackJack you need to have multiple decks which are shuffled 
        for i in range(len(self.cards)):
            r = random.randint(0, len(self.cards) - 1)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
        
        self.shuffled = True
        print("The cards has been shuffled.")


class Player:
    def __init__(self, name, chips):
        self.name, self.chips = name, chips

    def variables(self, bet, hand, splits, result):
        self.bet = bet
        self.hand = hand
        self.splits = splits
        self.result = result

    def add_chips(self, amount):
        self.chips += amount


class Hand:
    def __init__(self, name):
        self.name = name
    
    def variables(self, bet, cards, score, double, result):
        self.bet = bet
        self.cards = cards
        self.score = score
        self.double = double
        self.result = result


class Game:
    def __init__(self, list_of_players):
        self.players = list_of_players

    
def score_counter(l):
    score = 0
    temp = []
    # Sorts the card 
    for i in range(len(l)):
        if l[i].value != 14:
            temp.insert(0, l[i])
        else:
            temp.append(l[i])
    for i in range(len(temp)):
        score += Card.points(temp[i], score)
    return score


def trialAndError(text):
    retry = 0
    while retry < 5:
        answer = input(text)
        try:
            number = int(answer)
        except ValueError:
            if answer == "q":
                quit()
            
            elif answer == "all" or answer == "max":
                return "all"
            
            elif answer == "r":
                print("Oh you want me to choose... hmmmm..")
                time.sleep(1.5)
                x = random.randint(1, 50) * 100
                print(f"I have chosen {x}")
                return x
            
            print("\nValue error, please try again!")
            retry += 1
            continue
        
        return number
        
    print("Too many errors! System is shutting down.")
    return 0


def chips_check(player):
    for i in range(len(player)):
        p = player[i]
        print(f"{p.name}'s chip amount: {p.chips}")
        time.sleep(2)


def result_check(result, bet):

    endings = {"win": bet * 2, "loss" : 0, "push" : bet, "blackjack" : round(bet * 2.5), "left" : 0}
    return endings[result]


def printer(player, hand):
    p = player
    h = p.hand[hand]
    name = p.name
    bet = h.bet
    result = h.result

    print(f"{name} cards: ")
    for card in h.cards:
        Card.show(card)
    print(f"Points in hand: {h.score}")

    msg = ""
    if result_check(result, bet) - bet < 0:
        msg = "lost"
    
    elif result_check(result, bet) - bet > 0:
        msg = "earned"

    else:
        msg = "got back the bet of"

    print(f"{name} {msg} {bet} chips.")
    print(f"Chips total before betting: {p.chips + bet}")
    p.chips += result_check(result, bet)
    print(f"Chips total after betting: {p.chips}")

def get_result(player):
    time.sleep(1)
    print("\n" * 10)
    print("\n--- Result for players ---")
    for i in range(len(player)):
        print("---------------------------")
        p = player[i]
        for k in range(len(p.hand)):
            time.sleep(3)
            h = p.hand[k]
            result = h.result
            if len(p.hand) == 1:
                print(f"{p.name}: {result}")

            else:
                print(f"{p.name}'s hand number {k + 1}: {result}")
                if k >= 1:
                    print("\n")
                
            printer(p, k)

           # p.stats_add(result)


def hit(player, the_deck, i):
    p = player
    h = p.hand[i]
    
    card = the_deck.pop(0)
    h.cards.append(card)
    
    print("\nThe card is:")
    time.sleep(1.5)
    Card.show(card)
    h.score = score_counter(h.cards)
    time.sleep(1)


def splitting(deck, player, i):
    p = player
    h = p.hand[i]
    new_h = p.hand[i + 1]
    
    # puts the second card from the hand to the new hand
    new_h.cards = [h.cards.pop(1)]

    # old and new hand recives a new card
    h.cards.append(deck.pop(0)), new_h.cards.append(deck.pop(0))

    # sets values to the new hand
    new_h.bet = p.bet
    new_h.double = False
    new_h.result = ""

    # sets values for both hands
    h.score = score_counter(h.cards)
    new_h.score = score_counter(new_h.cards)

    print("The hand after the split:")
    for card in h.cards:
        time.sleep(1)
        Card.show(card)

    time. sleep(2)


def able_to_split(player, hand):
    msg = ""
    
    if len(hand.cards) == 2 and (Card.points(hand.cards[0], hand.score) == Card.points(hand.cards[1], hand.score) or hand.cards[0].value == hand.cards[1].value) and player.chips - player.bet >= 0 and player.splits < 3:
        return True

    msg += f"{player.name} cannot split unfortunately..."

    if not len(hand.cards) == 2:
        msg += f"\nThe amount of cards is too high: {len(hand.cards)} cards of max 2 cards."

    if not(Card.points(hand.cards[0], hand.score) == Card.points(hand.cards[1], hand.score) or hand.cards[0].value == hand.cards[1].value):
        msg += (f"\nThe cards aren't the same or their value isn't the same: Card 1: {hand.cards[0].show_text()}, Points: {Card.points(hand.cards[0], hand.score)}. "
        f"Card 2: {hand.cards[1].show_text()}, Points: {Card.points(hand.cards[1], hand.score)}.")

    if not(player.chips - player.bet >= 0):
        msg += f"\nPlayer chips balance is too low: Player chips: {player.chips}, Player chips if they splitted: {player.chips - player.bet}."

    if player.splits >= 3:
        msg += f"\nPlayer has splitted the max total times: {player.splits} splits of max 3."
    
    print(msg)


def able_to_dubble(player, hand):
    msg = ""
    
    if (not hand.double) and len(hand.cards) == 2 and player.chips - player.bet >= 0:
        return True
    
    msg += f"{player.name} can't double down!"

    if not len(hand.cards) == 2:
        msg += f"\nThe amount of cards is too high: {len(hand.cards)} cards of max 2 cards."

    if hand.double:
        msg += f"\nThe current hand has already been doubled down: hand.double = {hand.double}."

    if not(player.chips - player.bet >= 0):
        msg += f"\nPlayer chips balance is too low: Player chips: {player.chips}, Player chips if they doubled down: {player.chips - player.bet}."

    print(msg)


def gameplay(player, deck, i, dealer):
    p = player
    h = p.hand[i]

    # Phrases that correlates to an action
    hit_comms = ["h", "hit", "bring it", "another one", "i want to hit"]
    stand_comms = ["s", "stand", "i want to stand", "i am good"]
    split_comms = ["y", "split", "i want to split", "split them"]
    double_comms = ["d", "double", "double down", "i want to dubble down"]

    # The gameloop
    while True:
        
        if h.score == 21:
            print(f"\n{p.name} got exacly 21, well done!")
            time.sleep(2)
            break
            
        elif h.score > 21:
            print(f"\n{p.name} got {h.score} and busted!")
            h.result = "loss"
            time.sleep(2)
            break

        time.sleep(2)
        print("\n" * 10)
        print(f"\nThe cards of {p.name} are: ")
        for cards in h.cards:
            Card.show(cards)

        if h.double:
            print(f"{p.name} doubled down and has to stand. Their score is {h.score}")
            time.sleep(2)
            break    
        
        print("\nThe Dealers card is:")
        Card.show(dealer[0])
        choice = input(f"\n{p.name} has {h.score} points."
        f" Does {p.name} wanna Hit (h), Stand (s), Split (y) or Double down (d)? ").lower()
            
        if choice in hit_comms:
            hit(p, deck, i)
        
        elif choice in stand_comms:
            print(f"{p.name} decided to stand at {h.score}")
            time.sleep(2)
            break

        elif choice in split_comms:
            if able_to_split(p, h):
                if h.cards[0].value == h.cards[1].value:
                    print(f"{p.name} decided to split their pair of {h.cards[0].rank}.")
                
                else:
                    print(f"{p.name} decided to split their hand.")
                
                p.splits += 1
                p.hand.insert(i + 1, Hand(p.name))
                splitting(deck, p, i)

        elif choice in double_comms:
            if able_to_dubble(p, h):
                p.chips -= p.bet
                h.bet *= 2
                h.double = True
                hit(p, deck, i)

        else:
            print("Wrong input, try again!")
            time.sleep(1.5)

def deposit(player):
    p = player
    chip_amount = trialAndError("\nHow many chips do you want to deposit? ")
                
    if chip_amount == "all":        #   Same as "max", check trialAndError
        p.chips += 50000
                
    elif chip_amount > 0:
        p.chips += chip_amount
    
    else:
        print("Invalid amount of chips, try again!")

def betting(player):
    p = player
    while True:
        if p.chips == 0:
            answer = input(f"{p.name} have insufficient funds." 
            f" Would {p.name} like to deposit? (Yes or No): ").lower()
            if answer == "yes":
                deposit(player)
 
            elif answer == "no":
                p.result = "left"
                break

            else:
                print("Please select one of the choices")
                continue

        bet = trialAndError(
            f"How many chips does {p.name} want to bet?: ")
        
        if bet == "all":
            bet = p.chips
            p.chips -= bet

        elif bet > 0 and p.chips - bet  >= 0:
            p.chips -= bet
        
        elif bet == 0:
            p.result = "left"
   
        else:
            print("Invalid amount of chips, try again!")
            continue
            
        p.bet = bet
        break


def blackjack(the_deck, player):
    dealer_cards = []

    # Checks with every player how much they want to bet
    for i in range(len(player)):
        p = player[i]
        # puts the result of every player
        # to blank
        p.result = ""
        p.splits = 0
        print(f"\n{p.name} has {p.chips} to bet.")
        
        betting(p)

    d = Deck(the_deck)

    # Checks if the deck has been shuffled
    try:
        d.shuffled
    
    except AttributeError:
        d.shuffled = False

    if not d.shuffled:
        d.shuffle()

    
    player_amount = len(player)

    for n in range(len(player)):
        p = player[n]
        if p.result == "left":
            if n < player_amount:
                player.append(p)
                player.pop(n)
                player_amount -= 1

    print("amount of players:", player_amount)
        
    # The cards are being given out
    for i in range(player_amount):
        time.sleep(1)
        p = player[i]
        # sets list to empty
        p.hand = []
        player_cards = []
        player_cards.append(the_deck.pop(0))
        # the player gets its second card on beforehand 
        # but exacly the card that they are supposed to get
        player_cards.append(the_deck.pop(player_amount - i))
        # defines the starting hand for the player
        h = Hand(p.name)
        # adds the hand to the players hand list
        p.hand.append(h)     
        # setting values to the hand
        h.bet = p.bet
        h.cards = player_cards
        h.score = score_counter(h.cards)
        h.double = False
        h.result = ""
        # shows the players hand
        print(f"\nThe cards of {p.name} are: ")
        time.sleep(1)
        Card.show(h.cards[0]), Card.show(h.cards[1])

    # The dealer gets its cards
    dealer_cards.append(the_deck.pop(0))
    dealer_cards.append(the_deck.pop(0))
    dealer_score = score_counter(dealer_cards)

    time.sleep(1)
    print("\nThe dealer gets: ")
    Card.show(dealer_cards[0])

    # Checks for blackjacks
    time.sleep(1.5)
    # if the dealer has blackjack then 
    # the second card gets revealed
    if dealer_score == 21:      
        print("\nDealer gets:")
        Card.show(dealer_cards[1])
        print("The dealer got blackjack.")
        time.sleep(1)

        for j in range(len(player)):
            p = player[j]
            h = p.hand[0]
            if dealer_score == 21 and h.score == 21:
                h.result = "push"
            
            else:
                h.result = "loss"

        get_result(player)
        return player

    for k in range(player_amount):
        p = player[k]
        h = p.hand[0]
        if h.score == 21:
            h.result = "blackjack"

        # The player plays first
        # and the computer checks for
        # finnished games
        if h.result == "":
            for i in range(4):
                try:
                    h = p.hand[i]
                
                except IndexError:
                    continue
                
                gameplay(p, the_deck, i, dealer_cards)

                # checks if player may have lost
                if dealer_score > h.score:
                    h.result = "unclear"
    
    games_done = 0
    for z in range(len(player)):
        p = player[z]
        if p.result == "left":
            games_done += 1
            continue
        h = p.hand[0]
        if h.result != "":
            games_done += 1

    time.sleep(1)

    print("\nThe Dealer hand is:")
    Card.show(dealer_cards[0])
    time.sleep(2)
    Card.show(dealer_cards[1])

    time.sleep(1)

    if games_done == amount_of_players:
        for i in range(len(player)):
            if player[i].hand[0].result == "unclear":
                player[i].hand[0].result = "loss"
        get_result(player)
        return player
    
    # The dealer plays now

    while True:

        if dealer_score == 21:
            print("The dealer got 21.")
            break

        elif dealer_score < 17:        # The dealer has to hit if they have less than 17 score
            print(f"The dealer has {dealer_score} and must therefore hit.")
            time.sleep(1)
            print("\nThe dealer hits and gets:")
            card = the_deck.pop(0)
            dealer_cards.append(card)
            time.sleep(1.5)
            Card.show(card)
            dealer_score = score_counter(dealer_cards)

        elif dealer_score > 21:
            time.sleep(1)
            print(f"The dealer got {dealer_score} and busted!")
            break
            
        
        else:
            time.sleep(1)
            print(f"The dealer got {dealer_score} and must therefore stand.")
            break

    for z in range(len(player)):
        p = player[z]
        for i in range(len(p.hand)):
            h = p.hand[i]
            if h.result == "unclear":
                h.result = ""
            print(f"result of {p.name} is {h.result}")
            if h.result == "":
                if h.score > dealer_score or (h.score < dealer_score and dealer_score > 21):
                    h.result = "win"

                elif h.score == dealer_score:
                    h.result = "push"

                else:
                    h.result = "loss"
    # Results for all players
    get_result(player)

    time.sleep(1)
    return player


def amount_of_players(player):
    player = []
    if (input("Play with default players? (y/n)") == 'y'):
        
        player.append(Player("Walter White", 5000))
        player.append(Player("Hank Schrader", 5000))
        player.append(Player("Jesse Pinkman", 5000))
        player.append(Player("Gus Fring", 5000))
        player.append(Player("Mike Ehrmantraut", 5000))
        player.append(Player("Saul Goodman", 5000))
        
        return player
    
    num_of_players = trialAndError("\nHow many players want to play?(1 - 7): ")        
    
    if num_of_players in range(1,8):
        
        for i in range(num_of_players):
            retry = 0
            while retry < 3:
                name = input(f"\nWhat's the name of player {i + 1}? ")
                '''
                |||     Why is it checking if i > 0??
                |||     TODO: Check out the reasoning behind this
                '''     
                if i > 0:
                    # Checks players name to see if they are the same
                    for person in player:
                        if person.name.lower() == name.lower():
                                print(f"{person.name} is already here.")
                                retry =+ 1
                        else: break  
                        
            if retry == 3: 
                print("Too many attempts, next person!")
                continue

            chips = int(input(f"How many chips does {name} have? "))
            player.append(Player(name, chips))
             
        return player
    
    else:
        print("\nNumber of players is not between 1 and 7. Please try again." )
        #   To avoid a while loop.
        #   In the end it does the same thing, but with 'rekursion'.
        return (amount_of_players(player))


def main():
    l = []
    player = []
    played_before = False
    print("\n" * 25)
    print("Welcome to Blackjack!")
    time.sleep(1)
    
    while True:
        answer = input("\nWould you like to play a game of Blackjack? (Yes or No): ").lower()
        time.sleep(0.25)
        if answer == "yes":
            if played_before:
                same_players = input("\nWould you like to play with the same people as before?(Yes or No) ").lower()
                if same_players == "yes":
                    player = blackjack(l, player)
                
                else:
                    player = amount_of_players(player)
                    player = blackjack(l, player)

            else:
                player = amount_of_players(player)
                player = blackjack(l, player)

            time.sleep(1)
            print(f"\nThere are {len(l)} cards left.")
            played_before = True
            if len(l) <= 52:
                Deck(l).shuffled = False
                l = []
            chips_check(player)
            continue

        elif answer == "no":
            # print results of every player; wins, blackjack etc.
            # print profit / loss and the % increase   
            input("Press any key to quit")
            print("\nGoodbye!")
            quit()
        
        print("Please enter one of the choices.")


main()
