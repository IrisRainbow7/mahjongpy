import unittest
import MahjongTile
import MahjongPlayer

class TestPlayer(unittest.TestCase):

    HANDS1 = MahjongTile.MahjongTile.make_hads_set('22456', '333567', '234')    #タンヤオ

    def test_make_player(self):
        p = MahjongPlayer.MahjongPlayer()
        assertEqual(p.points, 25000)
        assertFalse(p.oya)

    def test_tenpai(self):
        p = MahjongPlayer.MahjongPlayer(hands=HANDS1)
        assertTrue(p.is_tenpai)

