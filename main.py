from deck import Deck


def get_bet(balance):
    """input bet amount"""

    while True:
        amount = input('Place your bet: $')
        try:
            amount = float(amount)
            if 1 <= amount <= balance:
                return amount
            elif amount > balance:
                print(f"You don't have enough balance(${balance}) to bet..")
            else:
                print("The minimum bet is $1.")
        except ValueError:
            print("Please enter a number.")


def player_get_start(role, deck):
    """start the play of the player"""

    role.append(deck.hit())
    role.append(deck.hit())
    print(f'You are dealt: {role[0]}, {role[1]}')

    return role


def dealer_get_start(role, deck):
    """start the play of the dealer"""

    role.append(deck.hit())
    role.append(deck.hit())
    print(f'The dealer is dealt: {role[0]}, Unknown')

    return role


def convert_point(item):
    """to convert the cards to points"""
    convert_table = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'A': 11
    }
    return convert_table[item]


def player_check(player):
    """check player points"""

    points = 0
    number_a = 0

    for item in player:
        point = convert_point(item[0])
        if point == 11:
            number_a += 1
        points += point

    while points > 21:
        if number_a != 0:
            number_a -= 1
            points -= 10
        else:
            break

    return points


def dealer_check(dealer, deck):
    """check dealer points
    This will give the final points that dealer will have:
    if points < 17, hit again.
    if 17 <= points <= 21, stay.
    if points > 21:
        check if there is A,
        use A=1 instead of A=11
        check the conditions again.
    return points
    """

    points = 0
    number_a = 0

    for item in dealer:
        point = convert_point(item[0])
        if point == 11:
            number_a += 1
        points += point
    print('The dealer has:', ', '.join(dealer))

    while True:

        if points < 17:
            hit = deck.hit()
            print(f'The dealer hits and is dealt: {hit}')
            dealer.append(hit)
            print('The dealer has:', ', '.join(dealer))
            point = convert_point(hit[0])
            if point == 11:
                number_a += 1
            points += point
        elif 17 < points <= 21:
            print('The dealer stays.')
            return points
        else:
            if number_a != 0:
                number_a -= 1
                points -= 10
            else:
                return points


def winning_check(player_point, dealer_point, balance, bet):
    """check the points to decide the winner"""

    if dealer_point > 21:
        print(f'The dealer busts, you win ${bet}!')
        balance += bet
    elif player_point > 21:
        print(f'Your hand value is over 21 and you lose ${bet}!')
        balance -= bet
    elif player_point > dealer_point:
        print(f'You win ${bet}!')
        balance += bet
    elif player_point < dealer_point:
        print(f'The dealer wins, you lose ${bet} :(')
        balance -= bet
    else:
        print('You tie. Your bet has been returned.')

    return balance


def main():
    """main part of the program"""

    print('Welcome to Blackjack!')

    balance = 500
    run = True

    while run:

        if balance == 0:
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye!")

        print('')
        answer = input(
            f'You are starting with ${balance}. Would you like to play a hand? ')

        if answer == 'yes':

            bet = get_bet(balance)

            deck = Deck()
            deck.shuffle()

            player = []
            dealer = []

            player = player_get_start(player, deck)
            dealer = dealer_get_start(dealer, deck)

            while True:
                if player_check(player) == 21:
                    print('Blackjack!')
                    if dealer_check(dealer, deck) != 21:
                        print(f'Blackjack! You win ${bet * 1.5}!')
                        balance += bet * 1.5
                        break
                    elif dealer_check(dealer, deck) == 21:
                        print('The dealer is also Blackjack!')
                        print('You tie. Your bet has been returned.')
                        break

                hit_stay = input('Would you like to hit or stay? ')

                if hit_stay == 'stay':
                    player_point = player_check(player)
                    dealer_point = dealer_check(dealer, deck)
                    balance = winning_check(
                        player_point, dealer_point, balance, bet)
                    break

                elif hit_stay == 'hit':
                    player_hit = deck.hit()
                    player.append(player_hit)
                    print(f'You are dealt: {player_hit}')
                    print('You now have:', ', '.join(player))
                    player_point = player_check(player)
                    if player_point > 21:
                        print(
                            f'You hand value is over 21 and you lose ${bet}.')
                        balance -= bet
                        break

                else:
                    print('This is not a valid option.')

        elif answer == 'no':
            print(
                f'You are leaving with balance ${balance}. See you next time:)')
            run = False
        else:
            pass


if __name__ == '__main__':
    main()
