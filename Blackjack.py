import random
import csv


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

# Returns string representation of a Card object
    def __str__(self):
        return f"{self.value} of {self.suit}"


# Gives each card the value that it has in blackjack
card_value = {
    "Ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10
}


class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King"]
        # Creates a list with cards
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)  # Shuffles the list

    def deal_card(self):
        return self.cards.pop()  # Deals cards by removing the last card from the list


class Participant:  # A class with useful methods for both the dealer and the player
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.blackjack = False

    def add_card(self, card):
        self.hand.append(card)  # Adds a card into you hand(list)

    # Method is returning a boolean value to indicate if the participant has a blackjack.
    def has_blackjack(self):
        return len(self.hand) == 2 and self.hand_value() == 21

    # Calculates the value of the participants hand. It uses the card_value dictionary.
    def hand_value(self):
        value = sum(card_value[card.value] for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.value == 'Ace')

        # Calculates if the ace should be counted as 1 or 11 depending on the other cards in participants deck
        for _ in range(num_aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1

        return value

    def display_hand(self, show_all=True):
        if show_all:
            hand_str = ', '.join(str(card)
                                 for card in self.hand)  # Shows full hand
        else:
            # Shows only one card(only for dealer)
            hand_str = str(self.hand[0]) + ", **Hidden Card**"
        print(f"{self.name}'s hand: {hand_str}")

    def clear_hand(self):  # Clears hand
        self.hand = []


class Player(Participant):
    def __init__(self, name, balance):
        super().__init__(name)
        self.balance = balance

    def update_balance(self, bet):
        self.balance += bet
        self.update_balance_in_csv()

    def update_balance_in_csv(self):  # Used to update balance in the csv file
        with open("accounts.csv", "r") as file:  # Reads your balance
            reader = csv.reader(file)
            rows = list(reader)

        with open("accounts.csv", "w", newline="") as file:  # Writes new balance
            writer = csv.writer(file)
            for row in rows:
                if row[0] == self.name:
                    row[2] = str(self.balance)
                writer.writerow(row)

    def show_balance(self):
        print(f"{self.name}'s balance: ${self.balance}")


class Dealer(Participant):
    def __init__(self):
        super().__init__("Dealer")


def create_account(player_name, password, balance):
    with open("accounts.csv", "a", newline="") as file:  # Appends a new account into the csv file
        writer = csv.writer(file)
        writer.writerow([player_name, password, balance])
    print("Account created successfully.")


def login():
    while True:
        username = input(
            "Enter your username (or 'exit' to return to the main menu): ").lower()
        if username == 'exit':
            break

        password = input("Enter your password: ")

        with open("accounts.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    balance = float(row[2])
                    print(f"Welcome back, {username}!")
                    return Player(username, balance)

        print("Invalid username or password. Please try again.")


def main_menu():
    while True:
        print("Welcome to Blackjack!")
        print("1. Log in")
        print("2. Create an account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            player = login()
            if player:
                game(player)  # Starts the game if user logs in
            else:
                print("Returning to the main menu.")
        elif choice == "2":
            player_name = input("Enter your name: ")
            password = input("Enter your password: ")
            starting_balance = 100
            create_account(player_name, password, starting_balance)
            print("Account created successfully.")
        elif choice == "3":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def game(player):
    dealer = Dealer()

    while True:
        player.show_balance()

        if player.balance == 0:
            print("You're broke. Game over!")
            break

        while True:
            try:
                bet = int(input("Place your bet: "))
                if bet > player.balance:
                    print("Bet exceeds balance. Please place a lower bet.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        player.clear_hand()
        dealer.clear_hand()

        deck = Deck()
        deck.shuffle()

        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

        player.display_hand()
        dealer.display_hand(show_all=False)

        while True:
            if player.has_blackjack():
                break
            else:
                choice = input(
                    "Do you want to hit or stand? hit/stand: ").lower()
                if choice == 'hit':
                    player.add_card(deck.deal_card())
                    player.display_hand()
                    if player.hand_value() > 21:
                        print("Bust! You lose.")
                        player.update_balance(-bet)
                        break
                elif choice == 'stand':
                    break

        if player.has_blackjack() and dealer.has_blackjack():
            print("It's a tie!")
        elif player.has_blackjack() and not dealer.has_blackjack():
            print("You win!")
        elif not player.has_blackjack() and dealer.has_blackjack():
            print("You lose")
        elif player.hand_value() <= 21:
            dealer.display_hand(show_all=True)
            while dealer.hand_value() < 17:
                dealer.add_card(deck.deal_card())
                dealer.display_hand(show_all=True)

            if player.has_blackjack() and dealer.has_blackjack():
                print("It's a tie!")
            elif player.has_blackjack() and not dealer.has_blackjack():
                print("You win!")
                player.update_balance(bet)
            elif not player.has_blackjack() and dealer.has_blackjack():
                print("You lose")
                player.update_balance(-bet)
            else:
                player_value = player.hand_value()
                dealer_value = dealer.hand_value()
                if dealer_value > 21 or player_value > dealer_value:
                    print("You win!")
                    player.update_balance(bet)
                elif player_value < dealer_value:
                    print("You lose.")
                    player.update_balance(-bet)
                else:
                    print("It's a tie!")

        player.show_balance()

        while True:
            play_again = input("Do you want to play again? yes/no: ").lower()
            if play_again == "yes" or play_again == "no":
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if play_again == "no":
            print("Thanks for playing!")
            break


player = main_menu()


if player:
    game(player)
