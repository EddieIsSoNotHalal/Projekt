
"""
+----------------+     +-----------------+
|     Card       |     |      Deck       |
+----------------+     +-----------------+
| - suit: string |     | - cards: list   |
| - value: string|     |                 |
+----------------+     +-----------------+
| + __init__(suit, value)                 |
| + __str__(): string                     |
+-----------------------------------------+
          ^
          |
          |
+-----------------+
|   Participant   |
+-----------------+
| - name: string  |
| - hand: list    |
| - blackjack: bool |
+-----------------+
| + __init__(name)                        |
| + add_card(card)                        |
| + has_blackjack(): bool                 |
| + hand_value(): int                     |
| + display_hand(show_all=True): None     |
| + clear_hand(): None                    |
+-----------------+
          ^
          |
          |
+-----------------+
|     Player      |
+-----------------+
| - balance: int|
+-----------------+
| + __init__(name, balance)               |
| + update_balance(bet)                   |
| + update_balance_in_csv(): None         |
| + show_balance(): None                  |
+-----------------+
          ^
          |
          |
+-----------------+
|     Dealer      |
+-----------------+
| + __init__()                            |
+-----------------+
"""
