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
    HANDS10 = MahjongTile.MahjongTile.make_hands_set('123456789', '', '', '222', '33') #一気通貫
    HANDS11 = MahjongTile.MahjongTile.make_hands_set('123', '123', '123', '222', '33') #三色同順
    HANDS12 = MahjongTile.MahjongTile.make_hands_set('222', '222', '222', '222', '33') #三色同刻
    HANDS13 = MahjongTile.MahjongTile.make_hands_set('123', '123999', '', '222', '33') #チャンタ
    HANDS14 = MahjongTile.MahjongTile.make_hands_set('345345', '345345', '', '', '33') #二盃口
    HANDS15 = MahjongTile.MahjongTile.make_hands_set('123', '123999', '11789') #ジュンチャン
    HANDS16 = MahjongTile.MahjongTile.make_hands_set('111456678', '', '', '333', '22') #混一色
    HANDS17 = MahjongTile.MahjongTile.make_hands_set('11122245667899') #清一色
    HANDS18 = MahjongTile.MahjongTile.make_hands_set('111666', '444', '11', '444') #四暗刻
    HANDS19 = MahjongTile.MahjongTile.make_hands_set('11122345678999') #九蓮宝燈

    def test_make_player(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.points, 25000)
        self.assertEqual(p.turn, 0)
        self.assertEqual(p.riichi_turn, None)
        self.assertFalse(p.oya)
        self.assertFalse(p.is_riichi)
        self.assertFalse(p.is_tumo)
        self.assertFalse(p.is_ron)

    def test_shanten(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS8)
        self.assertEqual(p.shanten(), 1)

    def test_riichi(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertFalse(p.is_riichi)

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
        self.assertEqual(p.minkos, 9)

    def test_ankans(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.ankans, 9)

    def test_minkans(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.minkans, 9)

    def test_yakus(self):
        print('*')#################
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS2, turn=5)
        self.assertEqual(p.yakus(), [])
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS18, is_tumo=True)
        self.assertIn('suankou', p.yakus())
        yakus = {0:'tanyao', 1:'pinfu', 2:'ipeikou', 3:'chitoitu', 4:'daisangen', 5:'kokushimusou', 6:'yakuhai', \
                7:'ikkituukan', 8:'sansyokudouzyun', 9:'sansyokudoukou', 10:'chanta', 11:'ryanpeikou', \
                12:'zyuntyan', 13:'honitu', 14:'chinitu', 15:'tyurenboutou'}
        hands = [self.HANDS1, self.HANDS3, self.HANDS4, self.HANDS5, self.HANDS6, self.HANDS7, self.HANDS6, \
                self.HANDS10, self.HANDS11, self.HANDS12, self.HANDS13, self.HANDS14, self.HANDS15, self.HANDS16, \
                self.HANDS17, self.HANDS19]
        for i in yakus:
            print(yakus[i])#################
            p = MahjongPlayer.MahjongPlayer(hands=hands[i])
            self.assertIn(yakus[i], p.yakus())

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
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS2)
        self.assertFalse(p.is_kokushimusou())

    def test_chitoitu(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_chitoitu())

    def test_hora(self):
        hands = [self.HANDS1, self.HANDS2, self.HANDS3, self.HANDS4, self.HANDS5, self.HANDS6, self.HANDS7]
        for i in hands:
            p = MahjongPlayer.MahjongPlayer(hands=i)
            self.assertTrue(p.is_hora())

    def test_menzen(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_menzen())

    def test_wait_ryanmen(self):
        p = MahjongPlayer.MahjongPlayer(hands=self.HANDS5)
        self.assertFalse(p.is_wait_ryanmen())





