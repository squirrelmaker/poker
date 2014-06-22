from rangeparser import Combo, Card, Shape, Hand
from pytest import raises


def test_first_and_second_are_Card_instances():
    assert isinstance(Combo('AsKc').first, Card)
    assert isinstance(Combo('AsKc').second, Card)


def test_case_insensitive():
    assert Combo('ASKC') > Combo('QCJH')
    assert Combo('askc') > Combo('qcjh')
    assert Combo('KSjh').is_broadway is True

    assert Combo('2s2c') == Combo('2S2C')


def test_card_order_is_not_significant():
    assert Combo('2s2c') == Combo('2c2s')
    assert Combo('AsQc') == Combo('QcAs')


def test_pairs_are_NOT_equal():
    assert Combo('2s2c') != Combo('2d2h')
    assert Combo('5d5h') != Combo('5s5h')


def test_pairs_are_better_than_non_pairs():
    assert Combo('2s2c') > Combo('AsKh')
    assert Combo('5s5h') > Combo('JsTs')


def test_card_are_better_when_ranks_are_higher():
    assert Combo('AsKc') > Combo('QcJh')
    assert Combo('KsJh') > Combo('QcJh')


def test_pair_comparisons():
    assert (Combo('2d2c') < Combo('2s2c')) is True
    # reverse
    assert (Combo('2s2c') < Combo('2d2c')) is False


def test_equal_pairs_are_not_less():
    assert (Combo('2s2c') < Combo('2s2c')) is False
    assert (Combo('2s2c') > Combo('2s2c')) is False


def test_unicode():
    assert Combo('AsAh') == Combo('A♠A♥')
    assert Combo('5s5h') > Combo('J♠T♠')
    assert Combo('5s5h') >= Combo('J♠T♠')


def test_repr():
    assert str(Combo('2s2c')) == '2♠2♣'
    assert str(Combo('KhAs')) == 'A♠K♥'
    assert str(Combo('ThTd')) == 'T♥T♦'


def test_is_suited():
    assert Combo('AdKd').is_suited is True


def test_is_pair():
    assert Combo('2s2c').is_pair is True
    assert Combo('AhAd').is_pair is True


def test_is_connector():
    assert Combo('AdKs').is_connector is True
    assert Combo('JdTc').is_connector is True
    assert Combo('KsQs').is_connector is True


def test_is_suited_connector():
    assert Combo('AdKd').is_connector
    assert Combo('KsQs').is_suited_connector


def test_is_broadway():
    assert Combo('KsJc').is_broadway is True


def test_invalid_combination():
    with raises(ValueError):
        Combo('2s2s')

    with raises(ValueError):
        Combo('2222')

    with raises(ValueError):
        Combo('KQJQ')


def test_hash():
    combination1 = Combo('2s2c')
    combination2 = Combo('2c2s')
    assert hash(combination1) == hash(combination2)

def test_putting_them_in_set_doesnt_raise_Exception():
    {Combo('AsAh'), Combo('2s2c')}


def test_two_set_of_combinations_are_equal_if_they_contains_same_cards():
    assert {Combo('2s2c')} == {Combo('2c2s')}


def test_from_cards():
    assert Combo.from_cards(Card('As'), Card('Kh')) == Combo('AsKh')

    combination = Combo.from_cards(Card('Kh'), Card('As'))
    assert combination == Combo('AsKh')
    assert repr(combination) == "Combo('A♠K♥')"


def test_shape_property():
    assert Combo('2s2c').shape == Shape.PAIR
    assert Combo('AsKs').shape == Shape.SUITED
    assert Combo('AdKs').shape == Shape.OFFSUIT


def test_to_hand_converter_method():
    assert Combo('2s2c').to_hand() == Hand('22')
    assert Combo('AsKc').to_hand() == Hand('AKo')
    assert Combo('7s6s').to_hand() == Hand('76s')
