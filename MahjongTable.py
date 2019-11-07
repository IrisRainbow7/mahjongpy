import MahjongTile
import MahjongPlayer

import random

class MahjongTable:


    def __init__(self, tiles=[], wind="ton", kyoku=1, honba=0, dora_showing_tile=None, dora_tile=None, \
                ri_bou=0, players=[], use_akadora=True, kuitan=True, rules={}):
        self.tiles = MahjongTile.MahjongTile.make_tiles_set(use_akadora=rules.get('use_akadora', use_akadora))
        random.shuffle(self.tiles)
        self.wind = wind
        self.kyoku = kyoku
        self.honba = honba
        self.dora_showing_tile = self.tiles.pop(random.randrange(136))
        self.dora_tile = self.dora_showing_tile.next()
        self.ri_bou = ri_bou
        h1, h2, h3, h4 = self.deal_tiles()
        p1 = MahjongPlayer.MahjongPlayer(hands=h1, oya=True, wind='ton')
        p2 = MahjongPlayer.MahjongPlayer(hands=h2, wind='nan')
        p3 = MahjongPlayer.MahjongPlayer(hands=h3, wind='sha')
        p4 = MahjongPlayer.MahjongPlayer(hands=h4, wind='pei')
        self.players = [p1, p2, p3, p4]
        self.use_akadora = rules.get('use_akadora', use_akadora)
        self.kuitan = rules.get('kuitan', kuitan)



    def deal_tiles(self,oya=1):
        hands = [[], [], [], []]
        for i in range(4):
            for _ in range(13):
                hands[i].append(self.tiles.pop(random.randrange(10)))
        hands[oya-1].append(self.tiles.pop(random.randrange(10)))
        return(hands)
