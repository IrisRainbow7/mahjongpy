import unittest
import MahjongTile

class TestTile(unittest.TestCase):


    def test_make_tiles(self):
        t = MahjongTile.MahjongTile('pinzu',1)
        self.assertEqual(t.tile_type, 'pinzu')
        self.assertEqual(t.number, 1)
        t = MahjongTile.MahjongTile('manzu',8)
        self.assertEqual(t.tile_type, 'manzu')
        self.assertEqual(t.number, 8)
        t = MahjongTile.MahjongTile('haku')
        self.assertEqual(t.tile_type, 'haku')
        self.assertEqual(t.number, None)
        t = MahjongTile.MahjongTile('tyun')
        self.assertEqual(t.tile_type, 'tyun')
        self.assertEqual(t.number, None)
        t = MahjongTile.MahjongTile('ton')
        self.assertEqual(t.tile_type, 'ton')
        self.assertEqual(t.number, None)
        t = MahjongTile.MahjongTile('sha')
        self.assertEqual(t.tile_type, 'sha')
        self.assertEqual(t.number, None)

    def test_tiles_equal(self):
        t1 = MahjongTile.MahjongTile('pinzu', 5)
        t2 = MahjongTile.MahjongTile('souzu', 7)
        t3 = MahjongTile.MahjongTile('tyun')
        t4 = MahjongTile.MahjongTile('tyun')
        self.assertTrue(t1 == t1)
        self.assertTrue(t3 == t4)
        self.assertFalse(t1 == t2)
        self.assertFalse(t2 == t4)

    def test_tiles_less_than(self):
        t1 = MahjongTile.MahjongTile('pinzu', 5)
        t2 = MahjongTile.MahjongTile('pinzu', 8)
        t3 = MahjongTile.MahjongTile('manzu', 2)
        t4 = MahjongTile.MahjongTile('hatu')
        t5 = MahjongTile.MahjongTile('haku')
        t6 = MahjongTile.MahjongTile('nan')
        t7 = MahjongTile.MahjongTile('pei')
        self.assertTrue(t1 < t2)
        self.assertTrue(t6 < t7)
        self.assertTrue(t3 < t1)
        self.assertTrue(t3 < t2)
        self.assertTrue(t5 < t4)
        self.assertTrue(t6 < t4)

    def test_next_tile(self):
        t1 = MahjongTile.MahjongTile('pinzu', 5)
        t2 = MahjongTile.MahjongTile('tyun')
        t3 = MahjongTile.MahjongTile('nan')
        self.assertTrue(t1.next() == MahjongTile.MahjongTile('pinzu', 6))
        self.assertTrue(t2.next() == MahjongTile.MahjongTile('haku'))
        self.assertTrue(t3.next() == MahjongTile.MahjongTile('sha'))

    def test_make_tiles_set(self):
        t = MahjongTile.MahjongTile.make_tiles_set()
        self.assertEqual(len(t), 136)
        self.assertEqual(len([i for i in t if i.tile_type=='pinzu']), 36)
        self.assertEqual(len([i for i in t if i.tile_type=='manzu']), 36)
        self.assertEqual(len([i for i in t if i.tile_type=='souzu']), 36)
        self.assertEqual(len([i for i in t if i.tile_type=='haku']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='hatu']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='tyun']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='ton']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='nan']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='sha']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='pei']), 4)
        for j in range(1,10):
            self.assertEqual(len([i for i in t if i.number==j]), 12)
        self.assertEqual(len([i for i in t if i.number==None]), 28)
        self.assertEqual(len([i for i in t if i.akadora==True]), 3)

    def test_make_hands_Set(self):
        t = MahjongTile.MahjongTile.make_hands_set('1234','56789','123','1','1')
        self.assertEqual(len([i for i in t if i.tile_type=='pinzu']), 3)
        self.assertEqual(len([i for i in t if i.tile_type=='manzu']), 4)
        self.assertEqual(len([i for i in t if i.tile_type=='souzu']), 5)
        self.assertEqual(len([i for i in t if i.tile_type=='haku']), 1)
        self.assertEqual(len([i for i in t if i.tile_type=='ton']), 1)
        self.assertEqual(len([i for i in t if i.number==1]), 2)
        self.assertEqual(len([i for i in t if i.number==2]), 2)
        self.assertEqual(len([i for i in t if i.number==3]), 2)
        self.assertEqual(len([i for i in t if i.number==4]), 1)
        self.assertEqual(len([i for i in t if i.number==5]), 1)
        self.assertEqual(len([i for i in t if i.number==6]), 1)
        self.assertEqual(len([i for i in t if i.number==7]), 1)
        self.assertEqual(len([i for i in t if i.number==8]), 1)
        self.assertEqual(len([i for i in t if i.number==9]), 1)
        self.assertEqual(len([i for i in t if i.number==None]), 2)
