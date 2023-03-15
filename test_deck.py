import pytest
from deck import Deck


@pytest.fixture
def dk():
    """pytest fixture"""
    return Deck()


def test_show(dk):
    """test show method"""
    assert dk.show() == print(dk.content)


def test_shuffle(dk):
    """test shuffle method"""
    dk_origin = dk.content[:]
    dk.shuffle()
    assert dk.content != dk_origin


def test_hit(dk):
    """test hit method"""
    dk_last = dk.content[-1]
    assert dk.hit() == dk_last
