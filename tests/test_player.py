import unittest
import MahjongTile
import MahjongPlayer

class TestPlayer(unittest.TestCase):

    HANDS1 = MahjongTile.MahjongTile.make_hands_set('22456', '333567', '234')    #タンヤオ
    HANDS2 = MahjongTile.MahjongTile.make_hands_set('888', '333678', '123','11') #役無し
    HANDS3 = MahjongTile.MahjongTile.make_hands_set('22345', '567', '123567') #平和
    HANDS4 = MahjongTile.MahjongTile.make_hands_set('345345', '123', '56788') #一盃口
    HANDS5 = MahjongTile.MahjongTile.make_hands_set('1155', '77', '3399', '22', '33') #七対子
    HANDS6 = MahjongTile.MahjongTile.make_hands_set('123', '77', '', '', '111222333') #大三元
    HANDS7 = MahjongTile.MahjongTile.make_hands_set('19', '19', '19', '1234', '1233') #国士無双
    HANDS8 = MahjongTile.MahjongTile.make_hands_set('1155', '77', '3399', '22', '32') #七対子(一向聴)
    HANDS9 = MahjongTile.MahjongTile.make_hands_set('1199', '77', '3399', '22', '32') #九種九牌

    def test_make_player(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.points, 25000)
        self.assertFalse(p.oya)

    def test_shanten(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS8)
        self.assertEqual(p.shanten(), 1)

    def test_riichi(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertFalse(p.is_riichi())

    def test_tenpai(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_tenpai())

    def test_furiten(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS8, discards=[MahjongTile.MahjongTile('tyun')])
        self.assertTrue(p.is_furiten())

    def test_kyusyukyuhai(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_kyusyukyuhai())

    def test_hora(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_hora())

    def test_displayed_doras(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.displayed_doras(MahjongTile.MahjongTile('manzu', 2)), 2)

    def test_akadoras(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.akadoras(), 2)

    def test_shuntus(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS3)
        self.assertEqual(p.shuntus(), 4)

    def test_ankos(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS6)
        self.assertEqual(p.ankos(), 3)

    def test_minkos(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.minkos(), 9)

    def test_ankans(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.ankans(), 9)

    def test_minkans(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.minkans(), 9)

    def test_yakus(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.yakus(), 9)

    def test_score_hu(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS3)
        self.assertEqual(p.yakus(), 20)

    def test_score_han(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS5)
        self.assertEqual(p.yakus(), 2)

    def test_mangan(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_mangan())

    def test_haneman(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_haneman())

    def test_baiman(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_baiman())

    def test_sanbaiman(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_sanbaiman())

    def test_kazoeyakuman(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_kazoeyakuman())

    def test_score(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.score(), 2000)

    def test_payed_score(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.payed_score(), [2000, 1000])

    def test_kokushimusou(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS7)
        self.assertTrue(p.is_kokushimusou())

    def test_chitoitu(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_chitoitu())

    def test_hora(self):
        hands = [self.HANDS1, self.HANDS2, self.HANDS3, self.HANDS4, self.HANDS5, self.HANDS6, self.HANDS7]
        for i in hands:
            p = MahjongPlayer.MahjongPlayer(hands=i)
            self.assertTrue(p.is_hora())





