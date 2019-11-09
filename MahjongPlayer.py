import MahjongTile
import MahjongTable

class MahjongPlayer:

    TILE_TYPES = ['pinzu', 'manzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    KYOMU_TILE = MahjongTile.MahjongTile(None)

    def __init__(self, hands=[], discards=[], melds=[], oya=False, points=25000, wind='ton', latest_tile=KYOMU_TILE, \
                table=None, turn=0, is_tumo=False, ankans=[], minkans=[], minkos=[]):
        if len(hands)+len(sum(melds,[])) not in [13, 14]: raise ValueError('amout of hands is not 13 or 14.')
        self.hands = hands
        self.discards = discards
        self.melds = melds
        self.oya = oya
        self.points = points
        self.wind = wind
        self.latest_tile = latest_tile
        self.is_riichi = False
        self.turn = turn
        self.riichi_turn = 100
        self.is_tumo = is_tumo
        self.is_ron = False
        self.ankans = ankans
        self.minkans = minkans
        self.minkos = minkos
        self.doubleriichi = False
        self.table = None
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
        counts = [100]

        tiles = self.hands[:]
        mentus = []
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        self.make_zyantou(tiles, mentus)
        tmp = tiles[:]
        count = 0
        for i in self.TILE_TYPES[:3]:
            for j in range(1,8):
                if MahjongTile.MahjongTile(i,j) in tmp:
                    if MahjongTile.MahjongTile(i,j+1) in tmp:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j+1)))
                        count += 1
                    if MahjongTile.MahjongTile(i,j+2) in tmp:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j+2)))
                        count += 1
        for i in self.TILE_TYPES:
            for j in range(1,8):
                    if tmp.count(MahjongTile.MahjongTile(i,j))==2:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        count += 1
                    if len(tmp)-count == 2:
                        tmp.pop(0)
                        count += 1
        if len(tmp) == count: counts.append(count)

        tiles = self.hands[:]
        mentus = []
        self.make_zyantou(tiles, mentus)
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        tmp = tiles[:]
        count = 0
        for i in self.TILE_TYPES[:3]:
            for j in range(1,8):
                if MahjongTile.MahjongTile(i,j) in tmp:
                    if MahjongTile.MahjongTile(i,j+1) in tmp:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j+1)))
                        count += 1
                    if MahjongTile.MahjongTile(i,j+2) in tmp:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j+2)))
                        count += 1
        for i in self.TILE_TYPES:
            for j in range(1,8):
                    if tmp.count(MahjongTile.MahjongTile(i,j))==2:
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        tmp.pop(tmp.index(MahjongTile.MahjongTile(i,j)))
                        count += 1
                    if len(tmp)-count == 2:
                        tmp.pop(0)
                        count += 1
        if len(tmp) == count: counts.append(count)

        tmp = tiles[:]
        count = 0
        for i in self.TILE_TYPES:
            for j in range(1,10):
                if tmp.count(MahjongTile.MahjongTile(i,j))==2: count += 1
        counts.append(7-count) #七対子用

        tiles = self.hands[:]
        tmp = []
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
        if tmp.count(1) == 13: counts.append(1)
        elif tmp.count(2) > 1: counts.append(13-tmp.count(1))
        else: counts.append(13-tmp.count(1)+1)

        return(min(counts))


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

    def zyantou(self):
        is_hora = False

        tiles = self.hands[:]
        mentus = []
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = self.is_zyantou(tiles, mentus)
        if is_hora: return(mentus[-1])

        tiles = self.hands[:]
        mentus = []
        self.make_zyantou(tiles, mentus)
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = is_hora or (len(tiles) == 0)
        if is_hora: return(mentus[0])

        return([self.KYOMU_TILE])

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
        if not self.is_menzen: return(False)
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
        if not self.is_menzen: return(False)
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

    def is_chanta(self):
        is_hora = False

        tiles = self.hands[:] + sum(self.melds, [])
        mentus = []
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = self.is_zyantou(tiles, mentus)
        count = 0
        for i in mentus:
            for j in i:
                if j.number in [1, 9, None]:
                    count += 1
                    break
        if is_hora and count==5: return(True)

        count = 0
        tiles = self.hands[:]
        mentus = []
        self.make_zyantou(tiles, mentus)
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = is_hora or (len(tiles) == 0)
        for i in mentus:
            for j in i:
                if j.number in [1, 9, None]:
                    count += 1
                    break
        if is_hora and count==5: return(True)

        return(False)

    def is_zyuntyan(self):
        is_hora = False

        tiles = self.hands[:] + sum(self.melds, [])
        mentus = []
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = self.is_zyantou(tiles, mentus)
        count = 0
        for i in mentus:
            for j in i:
                if j.number in [1, 9]:
                    count += 1
                    break
        if is_hora and count==5: return(True)

        count = 0
        tiles = self.hands[:]
        mentus = []
        self.make_zyantou(tiles, mentus)
        self.make_shuntus(tiles, mentus)
        self.make_kotus(tiles, mentus)
        is_hora = is_hora or (len(tiles) == 0)
        for i in mentus:
            for j in i:
                if j.number in [1, 9]:
                    count += 1
                    break
        if is_hora and count==5: return(True)

        return(False)



    def is_ipeikou(self, tiles, mentus):
        if not self.is_menzen: return(False)
        count = []
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if MahjongTile.MahjongTile(j,i) in tiles and MahjongTile.MahjongTile(j,i+1) in tiles and MahjongTile.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+2))))
                        mentus.append(tmp)
            count.append(len(tiles))
        return(count == [5,2])

    def is_ryanpeikou(self, tiles, mentus):
        if not self.is_menzen: return(False)
        count = []
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if MahjongTile.MahjongTile(j,i) in tiles and MahjongTile.MahjongTile(j,i+1) in tiles and MahjongTile.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(MahjongTile.MahjongTile(j,i+2))))
                        mentus.append(tmp)
            count.append(len(tiles))
        return(count == [8,2])




    def displayed_doras(self, dora):
        count = 0
        for i in self.hands:
            if i == dora: count += 1
        return(count)

    def akadoras(self):
        count = 0
        for i in self.hands:
            if i.akadora: count += 1
        return(count)

    def doras(self):
        return(self.displayed_doras() + self.akadoras())

    def shuntus(self):
        tiles = self.hands[:]
        mentus = []
        self.make_shuntus(tiles, mentus)
        return(mentus)

    def ankos(self):
        tiles = self.hands[:]
        mentus = []
        self.make_kotus(tiles, mentus)
        return(mentus)

    def kotus(self):
        return(self.ankos() + self.minkos)

    def kantus(self):
        return(self.ankans + self.minkans)

    def yakus(self):
        if not self.is_hora: raise RuntimeError('Not hora')
        yakus = []

        if self.is_riichi: yakus.append('riichi')
        if self.riichi_turn + 1 == self.turn: yakus.append('ippatu')
        if self.is_menzen() and self.is_tumo: yakus.append('menzentumo')
        tiles = self.hands[:] + sum(self.melds, [])
        table_wind = 'ton' if self.table is None else self.table.wind
        TILE_TYPES_YAKUHAI = self.TILE_TYPES[7:] + [self.wind] + [table_wind]
        for i in TILE_TYPES_YAKUHAI:
            if tiles.count(MahjongTile.MahjongTile(i)) == 3:
                yakus.append('yakuhai')
        kuitan = 'True' if self.table is None else self.table.kuitan
        tmp = tiles[:] if kuitan else self.hands[:]
        count = 0
        count += tmp.count(MahjongTile.MahjongTile('pinzu',1))
        count += tmp.count(MahjongTile.MahjongTile('pinzu',9))
        count += tmp.count(MahjongTile.MahjongTile('manzu',1))
        count += tmp.count(MahjongTile.MahjongTile('manzu',9))
        count += tmp.count(MahjongTile.MahjongTile('souzu',1))
        count += tmp.count(MahjongTile.MahjongTile('souzu',9))
        count += tmp.count(MahjongTile.MahjongTile('ton'))
        count += tmp.count(MahjongTile.MahjongTile('nan'))
        count += tmp.count(MahjongTile.MahjongTile('sha'))
        count += tmp.count(MahjongTile.MahjongTile('pei'))
        count += tmp.count(MahjongTile.MahjongTile('haku'))
        count += tmp.count(MahjongTile.MahjongTile('hatu'))
        count += tmp.count(MahjongTile.MahjongTile('tyun'))
        if count == 0: yakus.append('tanyao')
        if self.is_menzen and len(self.shuntus()) == 4 and self.zyantou()[0].tile_type not in TILE_TYPES_YAKUHAI and self.is_wait_ryanmen: yakus.append('pinfu')
        if self.is_ipeikou(self.hands[:], []): yakus.append('ipeikou')
        table_tiles = [] if self.table is None else self.table.tiles
        if len(table_tiles) == 14 and self.is_tumo: yakus.append('haitei')
        if len(table_tiles) == 14 and self.is_ron: yakus.append('houtei')
        if False: yakus.append('rinsyankaihou')
        if False: yakus.append('tyankan')
        if self.doubleriichi: yakus.append('doubleriichi')
        if self.is_chitoitu(): yakus.append('chitoitu')
        tiles = self.hands[:] + sum(self.melds, [])
        judge = False
        for i in self.TILE_TYPES[:3]:
            count = []
            for j in range(1,10):
                count.append(len([k for k in tiles if k.tile_type==i and k.number==j]))
            if all([l>0 for l in count]): judge = True
        if judge: yakus.append('ikkituukan')
        for i in range(1,8):
            count = []
            for j in self.TILE_TYPES[:3]:
                count.append(len([k for k in tiles if k.tile_type==j and k.number==i]))
                count.append(len([k for k in tiles if k.tile_type==j and k.number==i+1]))
                count.append(len([k for k in tiles if k.tile_type==j and k.number==i+1]))
            if count.count(1) == 9: yakus.append('sansyokudouzyun')
        for i in range(1,10):
            count = []
            for j in self.TILE_TYPES[:3]:
                count.append(len([k for k in tiles if k.tile_type==j and k.number==i]))
            if count.count(3) == 3: yakus.append('sansyokudoukou')
        if judge: yakus.append('sansyokudoukou')
        if len(self.minkos) < 2  and len(self.kotus()) == 3: yakus.append('sanankou')
        if len(self.minkos) == 1  and len(self.kotus()) == 4: yakus.append('sanankou')
        if len(self.kotus()) == 4:
            if self.is_menzen():
                if self.is_tumo or self.hands.count(self.latest_tile) == 2:
                    yakus.append('suankou')
            else:
                yakus.append('toitoi')
        if self.is_chanta(): yakus.append('chanta')
        if len(self.kantus()) == 3: yakus.append('sankantu')
        if self.is_ryanpeikou(self.hands[:], []): yakus.append('ryanpeikou')
        if self.is_zyuntyan():yakus.append('zyuntyan')
        count = 0
        for i in self.TILE_TYPES[:3]:
            if len([j for j in tiles if j.tile_type in [i]+self.TILE_TYPES[3:]]) == 14: count += 1
        if count > 0: yakus.append('honitu')
        if self.zyantou()[0].number==None and len([i for i in tiles if i.number==None]) > 5: yakus.append('syousangen')
        if len([i for i in tiles if i.number in [1,9,None]]) == 14: yakus.append('honroutou')
        for i in self.TILE_TYPES[:3]:
            if len([j for j in tiles if j.tile_type in [i]]) == 14:yakus.append('chinitu')
        count = 0
        for i in self.TILE_TYPES[7:]:
            if len([j for j in tiles if j.tile_type==i]) > 2: count += 1
        if count == 3: yakus.append('daisangen')
        if self.is_kokushimusou(): yakus.append('kokushimusou')
        if self.zyantou()[0].tile_type in self.TILE_TYPES[3:7] and len([i for i in tiles if i.tile_type in self.TILE_TYPES[3:7]]) > 8: yakus.append('syoususi')
        count = 0
        for i in self.TILE_TYPES[3:7]:
            if len([j for j in tiles if j.tile_type==i]) > 2: count += 1
        if count == 4: yakus.append('daisusi')
        if len([i for i in tiles if i.tile_type in ['souzu', 'hatu']]) == 14: yakus.append('ryuisou')
        if len([i for i in tiles if i.tile_type in self.TILE_TYPES[3:]]) == 14: yakus.append('tuisou')
        if len([i for i in tiles if i.number in [1,9]]) == 14: yakus.append('chinroutou')
        if len(self.kantus()) == 4: yakus.append('sukantu')
        if self.is_menzen:
            for i in self.TILE_TYPES[:3]:
                count = []
                for j in range(1,10):
                    count.append(self.hands.count(MahjongTile.MahjongTile(i,j)))
                if count.count(3)==2 and count.count(2)==1 and count.count(1)==6: yakus.append('tyurenboutou')
            is_furoed = False if self.table is None else self.table.is_furoed
            if not is_furoed and self.oya==False and self.turn == 0: yakus.append('chihou')
            if self.oya==True and self.turn==0: yakus.append('tenhou')

        return(yakus)

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

    def is_menzen(self):
        return(len(self.melds)==0)

    def is_wait_ryanmen(self):
        tiles = []
        if latest_tile.numer > 2:
            tiles.append(MahjongTile.MahjongTile(latest_tile.tile_type, latest_tile.number-2))
        elif latest_tile.number < 8:
            tiles.append(MahjongTile.MahjongTile(latest_tile.tile_type, latest_tile.number+2))
        return(any([(i in self.hands) for i in tiles]))

    def discard(self, tile):
        if not tile in self.hands:
            raise RuntimeError('does NOT have such tile')
        else:
            self.turn += 1
            self.discards.append(self.hands.pop(self.hands.index(MahjongTile.MahjongTile(tile.tile_type,tile.number))))

    def riichi(self):
        if not self.is_menzen():raise RuntimeError('Can Riichi ONLY when menzen')
        is_furoed = False if self.table is None else self.table.is_furoed
        if self.turn == 0 and is_furoed: self.doubleriichi = True
        self.riichi_turn = self.turn
        self.is_riichi = True

    def kan(self):
        return(None)

    def pon(self):
        return(None)

    def chi(self):
        return(None)

