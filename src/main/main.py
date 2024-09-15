from random import randint
from src.lib.lib import GamePole


def bot_attacks():
    x = randint(0, 9)
    y = randint(0, 9)
    return x, y


def game(mode='pvp'):
    player1 = GamePole()
    player2 = GamePole()
    queue = 0

    while player1.count_ships > 0 or player2.count_ships > 0:
        if mode == 'pvp':
            player2.show()
            print(["Player1's move", "Player2's move"][queue])
            x, y = map(int, input('x, y: ').split())
        else:  # pve mode
            player1.show()
            print("Your move" if queue == 0 else "Bot's move")
            if queue == 0:
                x, y = map(int, input('x, y: ').split())
            else:
                x, y = bot_attacks()

        if queue == 0:  # Player1 attacks
            z = player2.attack_ship(x, y)
        else:  # Player2 or Bot attacks
            z = player1.attack_ship(x, y)

        if not z:
            queue = 1 if queue == 0 else 0

        print("what should see p1")
        player2.opponent_field_show()
        if mode == 'pvp':
            print("what should see p2")
            player1.opponent_field_show()

        player1.move_ships()
        player2.move_ships()


game(input("choose 'pve' if you want to play against bot, otherwise 'pvp': "))
