import unittest
import MahjongTable

class TestTable(unittest.TestCase):


    def test_make_table(self):
        t = MahjongTable.MahjongTable()
        self.assertEqual(len(t.tiles), 82)
        self.assertEqual(t.wind, 'ton')
        self.assertEqual(t.kyoku, 1)
        self.assertEqual(t.honba, 0)
        self.assertEqual(t.ri_bou, 0)
        self.assertTrue(t.use_akadora)
        self.assertTrue(t.kuitan)
        self.assertFalse(t.kandora_sokumekuri)

    def test_change_rules(self):
        t = MahjongTable.MahjongTable(use_akadora=False, kuitan=False, kandora_sokumekuri=True)
        self.assertFalse(t.use_akadora)
        self.assertFalse(t.kuitan)
        self.assertTrue(t.kandora_sokumekuri)
        t = MahjongTable.MahjongTable(rules={'use_akadora':False, 'kuitan':False, 'kandora_sokumekuri':True})
        self.assertFalse(t.use_akadora)
        self.assertFalse(t.kuitan)
        self.assertTrue(t.kandora_sokumekuri)

    def test_deal(self):
        t = MahjongTable.MahjongTable()
        self.assertEqual(len(t.players[0].hands), 14)
        self.assertEqual(len(t.players[1].hands), 13)
        self.assertEqual(len(t.players[2].hands), 13)
        self.assertEqual(len(t.players[3].hands), 13)
