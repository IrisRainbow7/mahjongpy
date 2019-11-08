import MahjongTile

class MahjongPlayer:

    TILE_TYPES = ['pinzu', 'manzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']

    def __init__(self, hands=[], discards=[], melds=[], oya=False, points=25000, wind=''):
        if len(hands) not in [13, 14]: raise ValueError('amout of hands is not 13 or 14.')
        self.hands = hands
        self.discards = discards
        self.melds = melds
        self.oya = oya
        self.points = points
        self.wind = wind
        self.sort()

    def sort(self):
        self.hands = sorted(self.hands)

    def hands_display(self):
        for i in self.hands:
            print(i.display)

    def hands_name_jp(self):
        for i in self.hands:
            print(i.name_jp)

    def discards_display(self):
        for i in self.discards:
            print(i.display)

    def discards_name_jp(self):
        for i in self.discards:
            print(i.name_jp)

    def shanten(self):
        return(1)

    def is_riichi(self):
        return(False)

    def is_tenpai(self):
        return(True)

    def is_furiten(self):
        return(False)

    def is_kyusyukyuhai(self):
        count = 0
        for i in self.hands:
            if i.number in [1, 9, None]:
                count += 1
        return(count > 8)

    def is_hora(self):
        is_hora = False

        tiles = self.hands[:]
        mentus = []
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = self.is_zyantou(tiles, mentus)

        tiles = self.hands[:]
        mentus = []
        self.make_zyantou(tiles, mentus)
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = is_hora or (len(tiles) == 0)

        return(is_hora or self.is_chitoitu() or self.is_kokushimusou())


    def make_shuntus(self, tiles, mentus):
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if MahjongTile.MahjongTile(j,i) in tiles and MahjongTile.MahjongTile(j,i+1) in tiles and MahjongTile.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+2))))
                        mentus.append(tmp)

    def make_kotus(self, tiles, mentus):
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(MahjongTile.MahjongTile(j,i)) == 3:
                    tmp = []
                    for _ in range(3):
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                    mentus.append(tmp)

    def make_zyantou(self, tiles, mentus):
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(MahjongTile.MahjongTile(j,i)) == 2:
                    tmp = []
                    for _ in range(2):
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                    mentus.append(tmp)
                    return(None)

    def is_zyantou(self, tiles, mentus):
        if len(tiles) == 2 and tiles[0] == tiles[1]:
            mentus.append([tiles[0], tiles[1]])
            return(True)
        else:
            return(False)

    def is_chitoitu(self):
        mentus = []
        tiles = self.hands[:]
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(MahjongTile.MahjongTile(j,i)) == 2:
                    tmp = []
                    for _ in range(2):
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                    mentus.append(tmp)
        return(len(tiles) == 0)

    def is_kokushimusou(self):
        tmp = []
        tiles = self.hands[:]
        tmp.append(tiles.count(MahjongTile.MahjongTile('pinzu',1)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('pinzu',9)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('manzu',1)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('manzu',9)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('souzu',1)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('souzu',9)))
        tmp.append(tiles.count(MahjongTile.MahjongTile('ton')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('nan')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('sha')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('pei')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('haku')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('hatu')))
        tmp.append(tiles.count(MahjongTile.MahjongTile('tyun')))
        return(tmp.count(1) == 12 and tmp.count(2) == 1)

    def displayed_doras(self, dora):
        count = 0
        for i in self.hands:
            if i==dora: count += 1
        return(count)

    def akadoras(self):
        count = 0
        for i in self.hands:
            if i.akadora: count += 1
        return(count)

    def doras(self):
        return(self.displayed_doras() + self.akadoras())

    def shuntus(self):
        return(1)

    def ankos(self):
        return(1)

    def minkos(self):
        return(1)

    def kotus(self):
        return(self.ankos() + self.minkos())

    def ankans(self):
        return(1)

    def minkans(self):
        return(1)

    def kantus(self):
        return(self.ankans() + self.minkans())

    def yakus(self):
        if not self.is_hora: raise RuntimeError('Not hora')
        return([])

    def score_hu(self):
        return(30)

    def score_han(self):
        return(3)

    def is_mangan(self):
        return(False)

    def is_haneman(self):
        return(False)

    def is_baiman(self):
        return(False)

    def is_sanbaiman(self):
        return(False)

    def is_kazoeyakuman(self):
        return(False)

    def score(self):
        if not self.is_hora: raise RuntimeError('Not hora')
        return(1000)

    def payed_score(self):
        if not self.is_hora: raise RuntimeError('Not hora')
        return([1000, 500])
