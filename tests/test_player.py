import unittest
import mahjongpy

class TestPlayer(unittest.TestCase):

    HANDS1 = mahjongpy.MahjongTile.make_hands_set('22456', '333567', '234')    #タンヤオ
    HANDS2 = mahjongpy.MahjongTile.make_hands_set('888', '333678', '123','11') #役無し
    HANDS3 = mahjongpy.MahjongTile.make_hands_set('22345', '567', '123567') #平和
    HANDS4 = mahjongpy.MahjongTile.make_hands_set('345345', '123', '56788') #一盃口
    HANDS5 = mahjongpy.MahjongTile.make_hands_set('1155', '77', '3399', '22', '33') #七対子
    HANDS6 = mahjongpy.MahjongTile.make_hands_set('123', '77', '', '', '111222333') #大三元
    HANDS7 = mahjongpy.MahjongTile.make_hands_set('19', '19', '19', '1234', '1233') #国士無双
    HANDS8 = mahjongpy.MahjongTile.make_hands_set('1155', '77', '3399', '22', '32') #七対子(テンパイ)
    HANDS9 = mahjongpy.MahjongTile.make_hands_set('1199', '77', '3399', '22', '32') #九種九牌
    HANDS10 = mahjongpy.MahjongTile.make_hands_set('123456789', '', '', '222', '33') #一気通貫
    HANDS11 = mahjongpy.MahjongTile.make_hands_set('123', '123', '123', '222', '33') #三色同順
    HANDS12 = mahjongpy.MahjongTile.make_hands_set('222', '222', '222', '222', '33') #三色同刻
    HANDS13 = mahjongpy.MahjongTile.make_hands_set('123', '123999', '', '222', '33') #チャンタ
    HANDS14 = mahjongpy.MahjongTile.make_hands_set('345345', '345345', '', '', '33') #二盃口
    HANDS15 = mahjongpy.MahjongTile.make_hands_set('123', '123999', '11789') #ジュンチャン
    HANDS16 = mahjongpy.MahjongTile.make_hands_set('111456678', '', '', '333', '22') #混一色
    HANDS17 = mahjongpy.MahjongTile.make_hands_set('11122245667899') #清一色
    HANDS18 = mahjongpy.MahjongTile.make_hands_set('111666', '444', '11', '444') #四暗刻
    HANDS19 = mahjongpy.MahjongTile.make_hands_set('11122345678999') #九蓮宝燈
    HANDS20 = mahjongpy.MahjongTile.make_hands_set('1346', '36', '578', '14', '112') #何もなし

    def test_make_player(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.points, 25000)
        self.assertEqual(p.turn, 0)
        self.assertEqual(p.riichi_turn, None)
        self.assertFalse(p.oya)
        self.assertFalse(p.is_riichi)
        self.assertFalse(p.is_tumo)
        self.assertFalse(p.is_ron)
        self.assertRaises(ValueError, mahjongpy.MahjongPlayer())

    def test_shanten(self):
        h = mahjongpy.MahjongTile.make_hands_set('11345', '267', '123567')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 1)
        h = mahjongpy.MahjongTile.make_hands_set('11345', '267', '123569')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 2)
        h = mahjongpy.MahjongTile.make_hands_set('11345', '266', '123569')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 2)
        h = mahjongpy.MahjongTile.make_hands_set('22345', '267', '123567')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 1)
        h = mahjongpy.MahjongTile.make_hands_set('223348', '567', '12366')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 1)
        h = mahjongpy.MahjongTile.make_hands_set('223348', '567', '12338')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 2)
        h= mahjongpy.MahjongTile.make_hands_set('19', '129', '19', '1234', '123')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 1)
        h= mahjongpy.MahjongTile.make_hands_set('123', '19', '19', '1234', '123')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 2)
        h= mahjongpy.MahjongTile.make_hands_set('19', '123', '19', '1234', '123')
        p = mahjongpy.MahjongPlayer(hands=h)
        self.assertEqual(p.shanten(), 2)



    def test_riichi(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertFalse(p.is_riichi)
        p.riichi()
        self.assertTrue(p.is_riichi)
        self.assertTrue(p.is_doubleriichi)

    def test_tenpai(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS8)
        self.assertTrue(p.is_tenpai())
        p = mahjongpy.MahjongPlayer(hands=self.HANDS20)
        self.assertTrue(p.is_tenpai())

    def test_furiten(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS8, discards=[mahjongpy.MahjongTile('tyun')])
        self.assertTrue(p.is_furiten())

    def test_kyusyukyuhai(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS9)
        self.assertTrue(p.is_kyusyukyuhai())

    def test_hora(self):
        hands = [self.HANDS1, self.HANDS3, self.HANDS4, self.HANDS5, self.HANDS6, self.HANDS7, self.HANDS6, \
                self.HANDS10, self.HANDS11, self.HANDS12, self.HANDS13, self.HANDS14, self.HANDS15, self.HANDS16, \
                self.HANDS17, self.HANDS19]
        for i in hands:
            p = mahjongpy.MahjongPlayer(hands=i)
            self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('123', '123', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '123',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('222', '222', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '222',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('222', '333', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '567',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('111', '', '777', '', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '777',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('111', '55',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('444', '', '', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '999', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False))
        minkans = [mahjongpy.MahjongTile.make_hands_set('4444', '', '', '', '',checkamount=False)]
        ankans = [mahjongpy.MahjongTile.make_hands_set('', '', '9999', '', '',checkamount=False)]
        ankans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '3333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkans=minkans, ankans=ankans)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('222', '345', '', '', '11222',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('111999', '', '111', '', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        self.assertIn('sanankou', p.yakus())
        self.assertIn('toitoi', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('111999', '', '111', '444', '11',checkamount=False)
        p = mahjongpy.MahjongPlayer(hands=h, is_tumo=True)
        self.assertTrue(p.is_hora())
        self.assertIn('suankou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('22', '345', '', '', '111222',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '345', '', '11222333',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '33', '', '111222333',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '234444666', '', '', '22',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '888', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '', '', '111333', '22233',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('11999', '111', '999', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '999', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '55',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('666', '', '', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '222',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '111', '', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False))
        minkans = [mahjongpy.MahjongTile.make_hands_set('6666', '', '', '', '',checkamount=False)]
        minkans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '2222',checkamount=False))
        ankans = [mahjongpy.MahjongTile.make_hands_set('', '1111', '', '', '',checkamount=False)]
        ankans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '3333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkans=minkans, ankans=ankans)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('123456', '234', '99', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('789', '', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('123', '', '', '', '22',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '123', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '789', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '999', '',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, ankans=[m[-1]])
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('11123', '', '', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '123', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '999', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '789', '',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, ankans=[m[-2]])
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '111456', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '678', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertTrue(p.is_hora())
        h = mahjongpy.MahjongTile.make_hands_set('', '', '11122245699', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '678', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertTrue(p.is_hora())



    def test_displayed_doras(self):
        t = mahjongpy.MahjongTable()
        t.dora_tiles = [mahjongpy.MahjongTile('manzu', 1)]
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1, table=t)
        self.assertEqual(p.displayed_doras(), 2)

    def test_akadoras(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        p.hands[0].akadora = True
        p.hands[1].akadora = True
        self.assertEqual(p.akadoras(), 2)

    def test_shuntus(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS3)
        self.assertEqual(len(p.shuntus()), 4)

    def test_ankos(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS6)
        self.assertEqual(len(p.ankos()), 3)

    def test_minkos(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(len(p.minkos), 9)

    def test_ankans(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(len(p.ankans), 9)

    def test_minkans(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(len(p.minkans), 9)

    def test_kantus(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(len(p.kantus()), 9)


    def test_yakus(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS2, turn=5)
        self.assertEqual(p.yakus(), [])
        p = mahjongpy.MahjongPlayer(hands=self.HANDS18, is_tumo=True)
        self.assertIn('suankou', p.yakus())
        yakus = {0:'tanyao', 1:'pinfu', 2:'ipeikou', 3:'chitoitu', 4:'daisangen', 5:'kokushimusou', 6:'yakuhai', \
                7:'ikkituukan', 8:'sansyokudouzyun', 9:'sansyokudoukou', 10:'chanta', 11:'ryanpeikou', \
                12:'zyuntyan', 13:'honitu', 14:'chinitu', 15:'tyurenboutou'}
        hands = [self.HANDS1, self.HANDS3, self.HANDS4, self.HANDS5, self.HANDS6, self.HANDS7, self.HANDS6, \
                self.HANDS10, self.HANDS11, self.HANDS12, self.HANDS13, self.HANDS14, self.HANDS15, self.HANDS16, \
                self.HANDS17, self.HANDS19]
        for i in yakus:
            p = mahjongpy.MahjongPlayer(hands=hands[i])
            self.assertIn(yakus[i], p.yakus())

    def test_yakus_with_melds(self):
        h = mahjongpy.MahjongTile.make_hands_set('123', '123', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '123',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertIn('sansyokudouzyun', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('222', '222', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '222',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('sansyokudoukou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('222', '333', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '567',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertIn('sanankou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('111', '', '777', '', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '777',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('toitoi', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('111', '55',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('444', '', '', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '999', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False))
        minkans = [mahjongpy.MahjongTile.make_hands_set('4444', '', '', '', '',checkamount=False)]
        ankans = [mahjongpy.MahjongTile.make_hands_set('', '', '9999', '', '',checkamount=False)]
        ankans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '3333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkans=minkans, ankans=ankans)
        self.assertIn('sankantu', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('222', '345', '', '', '11222',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('syousangen', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('111999', '', '111', '', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('honroutou', p.yakus())
        self.assertIn('sanankou', p.yakus())
        self.assertIn('toitoi', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('111999', '', '111', '444', '11',checkamount=False)
        p = mahjongpy.MahjongPlayer(hands=h, is_tumo=True)
        self.assertIn('honroutou', p.yakus())
        self.assertIn('suankou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('22', '345', '', '', '111222',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('daisangen', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '345', '', '11222333',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('syoususi', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '33', '', '111222333',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('daisusi', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '234444666', '', '', '22',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '888', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('ryuisou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '', '', '111333', '22233',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '', '444',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('tuisou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('11999', '111', '999', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '999', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkos=m)
        self.assertIn('chinroutou', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '55',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('666', '', '', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '222',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '111', '', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '333',checkamount=False))
        minkans = [mahjongpy.MahjongTile.make_hands_set('6666', '', '', '', '',checkamount=False)]
        minkans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '2222',checkamount=False))
        ankans = [mahjongpy.MahjongTile.make_hands_set('', '1111', '', '', '',checkamount=False)]
        ankans.append(mahjongpy.MahjongTile.make_hands_set('', '', '', '', '3333',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, minkans=minkans, ankans=ankans)
        self.assertIn('sukantu', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('123456', '234', '99', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('789', '', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertIn('ikkituukan', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('123', '', '', '', '22',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '123', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '789', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '999', '',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, ankans=[m[-1]])
        self.assertIn('chanta', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('11123', '', '', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '123', '', '',checkamount=False)]
        m.append(mahjongpy.MahjongTile.make_hands_set('', '999', '', '',checkamount=False))
        m.append(mahjongpy.MahjongTile.make_hands_set('', '', '789', '',checkamount=False))
        p = mahjongpy.MahjongPlayer(hands=h, melds=m, ankans=[m[-2]])
        self.assertIn('zyuntyan', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '111456', '', '222', '11',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '678', '', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertIn('honitu', p.yakus())
        h = mahjongpy.MahjongTile.make_hands_set('', '', '11122245699', '', '',checkamount=False)
        m = [mahjongpy.MahjongTile.make_hands_set('', '', '678', '',checkamount=False)]
        p = mahjongpy.MahjongPlayer(hands=h, melds=m)
        self.assertIn('chinitu', p.yakus())


    def test_score_hu(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS3)
        self.assertEqual(p.yakus(), 20)

    def test_score_han(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertEqual(p.yakus(), 2)

    def test_mangan(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_mangan())

    def test_haneman(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_haneman())

    def test_baiman(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_baiman())

    def test_sanbaiman(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_sanbaiman())

    def test_kazoeyakuman(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertTrue(p.is_kazoeyakuman())

    def test_score(self):
        t = mahjongpy.MahjongTable()
        p, p2 = t.players[:2]
        self.assertTrue(p.oya)
        t.dora_tiles = [mahjongpy.MahjongTile('souzu',3)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('78','35','23499','','3333',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('manzu',9))
        p.chi(mahjongpy.MahjongTile('manzu',9))
        p.kan(mahjongpy.MahjongTile('tyun'))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('manzu',7)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('souzu',4))
        p.latest_tile = mahjongpy.MahjongTile('souzu',4)
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('souzu',3),mahjongpy.MahjongTile('manzu',7)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai'])
        self.assertFalse(p.is_yakuman())
        self.assertEqual(p.score_fu(), 60)
        self.assertEqual(p.score_han(), 3)
        self.assertEqual(p.score(), 11600)
        self.assertEqual(p.payed_score(), [11600,0,0])

    def test_score2(self):
        t = mahjongpy.MahjongTable(honba=1)
        self.assertEqual(t.info, '東1局1本場')
        p, p2 = t.players[1:3]
        self.assertFalse(p.oya)
        self.assertEqual(p.wind, 'nan')
        t.dora_tiles = [mahjongpy.MahjongTile('souzu',7)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('678','4','9999','','2233',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('tyun'))
        p.pon(mahjongpy.MahjongTile('tyun'))
        p2.discards.append(mahjongpy.MahjongTile('hatu'))
        p.pon(mahjongpy.MahjongTile('hatu'))
        p.kan(mahjongpy.MahjongTile('pinzu',9))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('manzu',6)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('souzu',4))
        p.latest_tile = mahjongpy.MahjongTile('souzu',4)
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('souzu',7),mahjongpy.MahjongTile('manzu',6)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai','yakuhai'])
        self.assertEqual(p.score_fu(), 70)
        self.assertEqual(p.score_han(), 3)
        self.assertTrue(p.is_mangan())
        self.assertEqual(p.score_without_tsumibo(), 8000)
        self.assertEqual(p.score(), 8300)
        self.assertEqual(p.payed_score(), [8300,0,0])

    def test_score3(self):
        t = mahjongpy.MahjongTable()
        self.assertEqual(t.info, '東1局0本場')
        p, p2 = t.players[1:3]
        self.assertFalse(p.oya)
        self.assertEqual(p.wind, 'nan')
        t.dora_tiles = [mahjongpy.MahjongTile('souzu',3)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('333','1333','3333567',checkamount=False)
        p.kan(mahjongpy.MahjongTile('pinzu',3))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('manzu',7)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('souzu',1))
        p.latest_tile = mahjongpy.MahjongTile('souzu',1)
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('souzu',3),mahjongpy.MahjongTile('manzu',7)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['sansyokudoukou','sanankou'])
        self.assertEqual(p.score_fu(), 60)
        self.assertEqual(p.score_han(), 7)
        self.assertTrue(p.is_haneman())
        self.assertEqual(p.score(), 12000)
        self.assertEqual(p.payed_score(), [12000,0,0])

    def test_score4(self):
        t = mahjongpy.MahjongTable(kyoku=2)
        self.assertEqual(t.info, '東2局0本場')
        p = t.players[3]
        self.assertFalse(p.oya)
        p2 = t.players[0]
        self.assertEqual(p.wind, 'pei')
        t.dora_tiles = [mahjongpy.MahjongTile('hatu')]
        p.hands = mahjongpy.MahjongTile.make_hands_set('99','2367','234','','22',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('souzu',5))
        p.chi(mahjongpy.MahjongTile('souzu',5))
        p2.discards.append(mahjongpy.MahjongTile('souzu',1))
        p.chi(mahjongpy.MahjongTile('souzu',1))
        p.hands.append(mahjongpy.MahjongTile('hatu'))
        p.latest_tile = mahjongpy.MahjongTile('hatu')
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('hatu')])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai'])
        self.assertEqual(p.score_fu(), 30)
        self.assertEqual(p.score_han(), 4)
        self.assertEqual(p.score(), 7700)
        self.assertEqual(p.payed_score(), [7700,0,0])

    def test_score5(self):
        t = mahjongpy.MahjongTable(wind='nan')
        self.assertEqual(t.info, '南1局0本場')
        p,p2 = t.players[2:]
        self.assertFalse(p.oya)
        self.assertEqual(p.wind, 'sha')
        t.dora_tiles = [mahjongpy.MahjongTile('souzu',1)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('2356','44','88','22',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('manzu',1))
        p.chi(mahjongpy.MahjongTile('manzu',1))
        p2.discards.append(mahjongpy.MahjongTile('souzu',4))
        p.pon(mahjongpy.MahjongTile('souzu',4))
        p2.discards.append(mahjongpy.MahjongTile('nan'))
        p.pon(mahjongpy.MahjongTile('nan'))
        p.hands.append(mahjongpy.MahjongTile('manzu',4))
        p.latest_tile = mahjongpy.MahjongTile('manzu',4)
        p.turn = 5
        p.is_tumo = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('souzu',1)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai'])
        self.assertEqual(p.score_fu(), 30)
        self.assertEqual(p.score_han(), 1)
        self.assertTrue(p.is_wait_ryanmen())
        self.assertEqual(p.score(), 1100)
        self.assertEqual(p.payed_score(), [0,500,300])

    def test_score6(self):
        t = mahjongpy.MahjongTable(kyoku=3)
        self.assertEqual(t.info, '東3局0本場')
        p,p2 = t.players[2:]
        self.assertFalse(p.oya)
        self.assertEqual(p.wind, 'sha')
        t.dora_tiles = [mahjongpy.MahjongTile('manzu',2)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('2267','','1133','11',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('pinzu',1))
        p.pon(mahjongpy.MahjongTile('pinzu',1))
        p2.discards.append(mahjongpy.MahjongTile('pinzu',3))
        p.pon(mahjongpy.MahjongTile('pinzu',3))
        p2.discards.append(mahjongpy.MahjongTile('ton'))
        p.pon(mahjongpy.MahjongTile('ton'))
        p.hands.append(mahjongpy.MahjongTile('manzu',5))
        p.latest_tile = mahjongpy.MahjongTile('manzu',5)
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('manzu',2)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai'])
        self.assertEqual(p.score_fu(), 30)
        self.assertEqual(p.score_han(), 3)
        self.assertTrue(p.is_wait_ryanmen())
        self.assertEqual(p.score(), 3900)
        self.assertEqual(p.payed_score(), [3900,0,0])

    def test_score7(self):
        t = mahjongpy.MahjongTable(wind='nan',kyoku=4)
        self.assertEqual(t.info, '南4局0本場')
        p = t.players[-1]
        self.assertFalse(p.oya)
        p2 = t.players[0]
        t.dora_tiles = [mahjongpy.MahjongTile('pinzu',3)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('222','45','779999','','11',checkamount=False)
        p2.discards.append(mahjongpy.MahjongTile('souzu',3))
        p.chi(mahjongpy.MahjongTile('souzu',3))
        p.kan(mahjongpy.MahjongTile('pinzu',9))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('souzu',1)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('haku'))
        p.latest_tile = mahjongpy.MahjongTile('haku')
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('pinzu',3),mahjongpy.MahjongTile('souzu',1)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['yakuhai'])
        self.assertEqual(p.score_fu(), 60)
        self.assertEqual(p.score_han(), 1)
        self.assertEqual(p.score(), 2000)
        self.assertEqual(p.payed_score(), [2000,0,0])

    def test_score8(self):
        t = mahjongpy.MahjongTable(wind='nan',kyoku=3)
        self.assertEqual(t.info, '南3局0本場')
        p = t.players[-1]
        self.assertFalse(p.oya)
        self.assertEqual(p.wind, 'pei')
        p2 = t.players[0]
        t.dora_tiles = [mahjongpy.MahjongTile('souzu',7)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('3457777','77889','','','22',checkamount=False)
        p.kan(mahjongpy.MahjongTile('manzu',7))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('pinzu',3)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('souzu',9))
        p.latest_tile = mahjongpy.MahjongTile('souzu',9)
        p.turn = 5
        p.is_ron = True
        self.assertEqual(t.dora_tiles, [mahjongpy.MahjongTile('souzu',7),mahjongpy.MahjongTile('pinzu',3)])
        self.assertTrue(p.is_hora())
        self.assertEqual(p.yakus(), ['ipeikou'])
        self.assertEqual(p.score_fu(), 50)
        self.assertEqual(p.score_han(), 3)
        self.assertEqual(p.score(), 6400)
        self.assertEqual(p.payed_score(), [6400,0,0])

    def test_score9(self):
        t = mahjongpy.MahjongTable(wind='nan',kyoku=3)
        self.assertEqual(t.info, '南3局0本場')
        p,p2 = t.players[:2]
        self.assertTrue(p.oya)
        self.assertEqual(p.wind, 'ton')
        t.dora_tiles = [mahjongpy.MahjongTile('manzu',4),mahjongpy.MahjongTile('manzu',8),mahjongpy.MahjongTile('manzu',7)]
        p.hands = mahjongpy.MahjongTile.make_hands_set('222','4455','','','1111333',checkamount=False)
        p.kan(mahjongpy.MahjongTile('haku'))
        t.dora_tiles[-1] = mahjongpy.MahjongTile('souzu',7)
        p.hands.pop(p.hands.index(p.latest_tile))
        p.hands.append(mahjongpy.MahjongTile('souzu',4))
        p.latest_tile = mahjongpy.MahjongTile('souzu',4)
        p.turn = 5
        p.is_tumo = True
        self.assertTrue(p.is_hora())
        self.assertTrue(p.is_menzen())
        self.assertEqual(len(p.ankos())+len(p.kantus()), 3)
        self.assertEqual(len(p.ankos()), 2)
        self.assertEqual(len(p.minkos), 2)
        self.assertEqual(len(p.kotus()), 3)
        self.assertEqual(p.yakus(), ['menzentumo','yakuhai','yakuhai','suankou'])
        self.assertTrue(p.is_yakuman())
        self.assertEqual(p.score_fu(), 70)
        self.assertEqual(p.score_han(), 13)
        self.assertEqual(p.score(), 48000)
        self.assertEqual(p.payed_score(), [0,0,16000])





    def test_payed_score(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS1)
        self.assertEqual(p.payed_score(), [2000, 1000])

    def test_kokushimusou(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS7)
        self.assertTrue(p.is_kokushimusou())
        p = mahjongpy.MahjongPlayer(hands=self.HANDS2)
        self.assertFalse(p.is_kokushimusou())

    def test_chitoitu(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_chitoitu())

    def test_chanta(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_chanta())

    def test_zyuntyan(self):
        pass

    def test_ipeikou(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_ipeikou())

    def test_ryanpeikou(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_ryanpeikou())

    def test_menzen(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertTrue(p.is_menzen())

    def test_wait_ryanmen(self):
        p = mahjongpy.MahjongPlayer(hands=self.HANDS5)
        self.assertFalse(p.is_wait_ryanmen())

    def test_kan(self):
        pass

    def test_kakan(self):
        pass

    def test_pon(self):
        pass

    def test_chi(self):
        pass



