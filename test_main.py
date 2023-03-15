import pytest
from unittest import mock
from deck import Deck
from main import *


@pytest.fixture
def dk():
    return Deck()


def test_get_bet(capsys):
    """ get bet test in different inputs"""
    balance = 200
    mock_input = mock.Mock(side_effect=['300', '-1', 'abc', '100'])

    with mock.patch('builtins.input', mock_input):
        assert get_bet(balance) == 100
        # capture the standard output
        out, _ = capsys.readouterr()
        # check if the output contains error messages for invalid inputs
        assert f"You don't have enough balance(${balance}) to bet.." in out
        assert "The minimum bet is $1." in out
        assert "Please enter a number." in out


def test_player_get_start(dk, capsys):
    """test player get started"""
    dk.shuffle()
    role = []
    role += [dk.content[-1]] + [dk.content[-2]]
    role_test = []
    assert role == player_get_start(role_test, dk)
    out, _ = capsys.readouterr()
    assert f'You are dealt: {role[0]}, {role[1]}' in out


def test_dealer_get_start(dk, capsys):
    """test dealer get started"""
    dk.shuffle()
    role = []
    role += [dk.content[-1]] + [dk.content[-2]]
    role_test = []
    assert role == dealer_get_start(role_test, dk)
    out, _ = capsys.readouterr()
    assert f'The dealer is dealt: {role[0]}, Unknown' in out


def test_convert_point():
    """test convert point"""
    convert_standard = {
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

    for key, value in convert_standard.items():
        assert convert_point(key) == value


def test_player_check():
    """check player points"""
    player = ['K3', 'Qb']
    assert player_check(player) == 20
    player = ['A3', 'A4']
    assert player_check(player) == 12
    player = ['K3', 'A4', 'A5', 'A6']
    assert player_check(player) == 13
    player = ['A3', 'A4', 'A5', 'A6']
    assert player_check(player) == 14
    player = ['K3', '64', '45', 'A6']
    assert player_check(player) == 21


def test_dealer_check(dk):
    """check dealer points"""
    dk.shuffle()

    dealer = ['K3', 'Qb']
    assert dealer_check(dealer, dk) == 20

    dealer = ['A3', 'A4']
    assert dealer_check(dealer, dk) > 16
    assert len(dealer) > 2

    dealer = ['K3', 'A4']
    assert dealer_check(dealer, dk) == 21
    assert len(dealer) == 2

    dealer = ['83', '94']
    assert dealer_check(dealer, dk) == 17
    assert len(dealer) == 2

    dealer = ['4i', '8g']
    assert dealer_check(dealer, dk) > 16
    assert len(dealer) > 2


def test_winning_check(capsys):
    """test winning check"""
    assert winning_check(21, 22, 200, 100) == 300
    out, _ = capsys.readouterr()
    assert 'The dealer busts, you win $100!\n' == out

    assert winning_check(18, 17, 200, 100) == 300
    out, _ = capsys.readouterr()
    assert 'You win $100!\n' == out

    assert winning_check(22, 17, 200, 100) == 100
    out, _ = capsys.readouterr()
    assert 'Your hand value is over 21 and you lose $100!\n' == out

    assert winning_check(16, 17, 200, 100) == 100
    out, _ = capsys.readouterr()
    assert 'The dealer wins, you lose $100 :(\n' == out

    assert winning_check(17, 17, 200, 100) == 200
    out, _ = capsys.readouterr()
    assert 'You tie. Your bet has been returned.\n' == out
