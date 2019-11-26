import mahjongpy

class MahjongPlayer:
    """
    プレイヤーを表すクラス。各プレイヤーの情報などを保持する

    Attributes
    ----------
    hands : list
        プレイヤーの手牌。MahjongTileのリスト
    discards : list
        プレイヤーの河。MahjongTileのリスト
    melds : list
        プレイヤーが鳴いた牌のリストのリスト。
        ポン、カン、チーをしたときに3枚または4枚のMahjongTileのリストが追加される。
    oya : bool
        プレイヤーが親かどうか
    points : int
        プレイヤーの持ち点
    wind : str
        プレイヤーの自風。東:'ton'　南:'nan'　西:'sha'　北:'pei'
    latest_tile : MahjongTile
        一番最後に引いた牌(一番最新の牌)
    table : MahjongTable
        プレイヤーがゲームを行っている卓
    turn : int
        局が始まってから経過したターン数
    riichi_turn : int
        リーチした時のターン数
    is_tumo : bool
        ツモしたかどうか
    id_ron : bool
        ロンしたかどうか
    ankans : list
        暗槓のリスト。MahjongTile4枚のリスト(暗槓)のリスト
    minkans :list
        明槓のリスト。MahjongTile4枚のリスト(明槓)のリスト
    minkos :list
        明刻のリスト。MahjongTile3枚のリスト(明刻)のリスト
    is_riichi : bool
        リーチしているかどうか
    is_doubleriichi : bool
        和了った時にダブルリーチ(役)がつく状態かどうか
    is_rinsyankaihou : bool
        和了った時に嶺上開花(役)がつく状態かどうか
    score_cache : int
        プレイヤーの点数のキャッシュ
    score_without_tsumibo_cache : int
        プレイヤーの点数(積み棒分を除く)のキャッシュ
    yakus_cache : list
        プレイヤーの手牌でできる役のリストのキャッシュ
    tilse_cache : list
        手牌のキャッシュ
    """

    TILE_TYPES = ['pinzu', 'manzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    KYOMU_TILE = mahjongpy.MahjongTile(None)

    def __init__(self, hands=[], discards=[], melds=[], oya=False, points=25000, wind='ton', latest_tile=KYOMU_TILE, \
                table=None, turn=0, is_tumo=False, ankans=[], minkans=[], minkos=[]):
        if len(hands)+len(sum(melds,[])) not in [13, 14]: raise ValueError('amout of hands is not 13 or 14.')
        self.hands = hands[:]
        self.discards = discards[:]
        self.melds = melds[:]
        self.oya = oya
        self.points = points
        self.wind = wind
        self.latest_tile = latest_tile
        self.is_riichi = False
        self.turn = turn
        self.riichi_turn = 100
        self.is_tumo = is_tumo
        self.is_ron = False
        self.ankans = ankans[:]
        self.minkans = minkans[:]
        self.minkos = minkos[:]
        self.is_doubleriichi = False
        self.is_rinsyankaihou = False
        self.table = table
        self.score_cache = 0
        self.score_without_tsumibo_cache = 0
        self.yakus_cache = []
        self.tiles_cache = []
        self.sort()

    def sort(self):
        """
        プレイヤーの手牌を種類、番号順にソートする

        Notes
        -----
        self.hands を　破壊的に　ソートするので注意

        """
        self.hands = sorted(self.hands)

    def hands_display(self):
        """
        プレイヤーの手牌すべてを実際の牌のような感じで表示
        """
        for i in self.hands:
            print(i.display)

    def hands_name_jp(self):
        """
        プレイヤーの手牌すべての名前を表示
        """
        for i in self.hands:
            print(i.name_jp)

    def discards_display(self):
        """
        プレイヤーの河すべてを実際の牌のような感じで表示
        """
        for i in self.discards:
            print(i.display)

    def discards_name_jp(self):
        """
        プレイヤーの河すべての名前を表示
        """
        for i in self.discards:
            print(i.name_jp)

    def shanten(self):
        """
        プレイヤーのシャンテン数を計算。一向聴で1、二向聴で2……　を返す

        Returns
        -------
        count : int
            プレイヤーのシャンテン数
        """
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
                if mahjongpy.MahjongTile(i,j) in tmp:
                    if mahjongpy.MahjongTile(i,j+1) in tmp:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j+1)))
                        count += 1
                    if mahjongpy.MahjongTile(i,j+2) in tmp:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j+2)))
                        count += 1
        for i in self.TILE_TYPES:
            for j in range(1,8):
                    if tmp.count(mahjongpy.MahjongTile(i,j))==2:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
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
                if mahjongpy.MahjongTile(i,j) in tmp:
                    if mahjongpy.MahjongTile(i,j+1) in tmp:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j+1)))
                        count += 1
                    if mahjongpy.MahjongTile(i,j+2) in tmp:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j+2)))
                        count += 1
        for i in self.TILE_TYPES:
            for j in range(1,8):
                    if tmp.count(mahjongpy.MahjongTile(i,j))==2:
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        tmp.pop(tmp.index(mahjongpy.MahjongTile(i,j)))
                        count += 1
                    if len(tmp)-count == 2:
                        tmp.pop(0)
                        count += 1
        if len(tmp) == count: counts.append(count)

        tmp = tiles[:]
        count = 0
        for i in self.TILE_TYPES:
            for j in range(1,10):
                if tmp.count(mahjongpy.MahjongTile(i,j))==2: count += 1
        counts.append(7-count) #七対子用

        tiles = self.hands[:]
        tmp = []
        tmp.append(tiles.count(mahjongpy.MahjongTile('pinzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('pinzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('manzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('manzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('souzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('souzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('ton')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('nan')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('sha')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('pei')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('haku')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('hatu')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('tyun')))
        if tmp.count(1) == 13: counts.append(1)
        elif tmp.count(2) > 1: counts.append(13-tmp.count(1))
        else: counts.append(13-tmp.count(1)+1)

        return(min(counts)-1)


    def is_tenpai(self):
        """
        Returns
        -------
        is_tenpai : bool
            プレイヤーがテンパイかどうか
        """
        return(self.shanten() == 0)

    def is_furiten(self):
        """
        Returns
        -------
        is_furiten : bool
            プレイヤーがフリテン状態かどうか
        """
        is_furiten = False

    def is_kyusyukyuhai(self):
        """
        Returns
        -------
        is_kyusyukyuhai : bool
            手牌が九種九牌かどうか
        """
        count = 0
        for i in self.hands:
            if i.number in [1, 9, None]:
                count += 1
        return(count > 8)

    def is_hora(self):
        """
        Returns
        -------
        is_hora : bool
            プレイヤーの手牌が和了形かどうか
        """
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
        """
        プレイヤーの手牌の内、雀頭を返す

        Returns
        -------
        tiles : list
            雀頭(2枚のMahjongTileのリスト)。雀頭がない場合ダミータイル(self.KYOMU_TILE)1枚のみのリストが返る
        """
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
        """
        順子を作る

        Parameters
        ----------
        tiles : list
            未処理のMahjongTileのリスト(手牌)
        mentus: list
            処理済みのMahjongTileのリスト。このリストに順子が、MahjongTile3枚のリストとして追加される

        Notes
        -----
        引数のtiles、およびmentusを　破壊的に　変更するので注意
        """
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if mahjongpy.MahjongTile(j,i) in tiles and mahjongpy.MahjongTile(j,i+1) in tiles and mahjongpy.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+2))))
                        mentus.append(tmp)

    def make_kotus(self, tiles, mentus):
        """
        刻子を作る

        Parameters
        ----------
        tiles : list
            未処理のMahjongTileのリスト(手牌)
        mentus: list
            処理済みのMahjongTileのリスト。このリストに刻子が、MahjongTile3枚のリストとして追加される

        Notes
        -----
        引数のtiles、およびmentusを　破壊的に　変更するので注意
        """
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(mahjongpy.MahjongTile(j,i)) == 3:
                    tmp = []
                    for _ in range(3):
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                    mentus.append(tmp)

    def make_zyantou(self, tiles, mentus):
        """
        雀頭を作る

        Parameters
        ----------
        tiles : list
            未処理のMahjongTileのリスト(手牌)
        mentus: list
            処理済みのMahjongTileのリスト。このリストに雀頭が、MahjongTile2枚のリストとして追加される

        Notes
        -----
        引数のtiles、およびmentusを　破壊的に　変更するので注意
        """
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(mahjongpy.MahjongTile(j,i)) == 2:
                    tmp = []
                    for _ in range(2):
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                    mentus.append(tmp)
                    return(None)

    def is_zyantou(self, tiles, mentus):
        """
        残りの牌が雀頭かどうかを判定する

        Parameters
        ----------
        tiles : list
            未処理のMahjongTileのリスト
        mentus: list
            処理済みのMahjongTileのリスト。雀頭判定されたとき、MahjongTile2枚がリストとして追加される

        Notes
        -----
        引数のtiles、およびmentusを　破壊的に　変更するので注意
        """
        if len(tiles) == 2 and tiles[0] == tiles[1]:
            mentus.append([tiles[0], tiles[1]])
            return(True)
        else:
            return(False)

    def is_chitoitu(self):
        """
        Returns
        -------
        is_chitoitu : bool
            プレイヤーの手牌が七対子かどうか
        """
        if not self.is_menzen(): return(False)
        mentus = []
        tiles = self.hands[:]
        for i in range(1,10):
            for j in self.TILE_TYPES:
                if tiles.count(mahjongpy.MahjongTile(j,i)) == 2:
                    tmp = []
                    for _ in range(2):
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                    mentus.append(tmp)
        return(len(tiles) == 0)

    def is_kokushimusou(self):
        """
        Returns
        -------
        is_kokushimusou : bool
            プレイヤーの手牌が国士無双かどうか
        """
        if not self.is_menzen(): return(False)
        tmp = []
        tiles = self.hands[:]
        tmp.append(tiles.count(mahjongpy.MahjongTile('pinzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('pinzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('manzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('manzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('souzu',1)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('souzu',9)))
        tmp.append(tiles.count(mahjongpy.MahjongTile('ton')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('nan')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('sha')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('pei')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('haku')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('hatu')))
        tmp.append(tiles.count(mahjongpy.MahjongTile('tyun')))
        return(tmp.count(1) == 12 and tmp.count(2) == 1)

    def is_chanta(self):
        """
        Returns
        -------
        is_kokushimusou : bool
            プレイヤーの手牌がチャンタかどうか
        """
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
        """
        Returns
        -------
        is_kokushimusou : bool
            プレイヤーの手牌がジュンチャンかどうか
        """
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
        """
        Returns
        -------
        is_kokushimusou : bool
            プレイヤーの手牌が一盃口かどうか
        """
        if not self.is_menzen(): return(False)
        count = []
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if mahjongpy.MahjongTile(j,i) in tiles and mahjongpy.MahjongTile(j,i+1) in tiles and mahjongpy.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+2))))
                        mentus.append(tmp)
            count.append(len(tiles))
        return(count == [5,2])

    def is_ryanpeikou(self, tiles, mentus):
        """
        Returns
        -------
        is_kokushimusou : bool
            プレイヤーの手牌が二盃口かどうか
        """
        if not self.is_menzen(): return(False)
        count = []
        for _ in range(2):
            for i in range(1,8):
                for j in self.TILE_TYPES[:3]:
                    if mahjongpy.MahjongTile(j,i) in tiles and mahjongpy.MahjongTile(j,i+1) in tiles and mahjongpy.MahjongTile(j,i+2) in tiles:
                        tmp = []
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+1))))
                        tmp.append(tiles.pop(tiles.index(mahjongpy.MahjongTile(j,i+2))))
                        mentus.append(tmp)
            count.append(len(tiles))
        return(count == [8,2])


    def displayed_doras(self):
        """
        手牌の内ドラ表示牌の次の牌の数

        Returns
        -------
        count : int
            手牌のドラ牌の数
        """
        count = 0
        tiles = self.hands[:] + sum(self.melds, [])
        doras = None if self.table is None else self.table.dora_tiles
        for i in tiles:
            for j in doras:
                if i == j: count += 1
        return(count)

    def akadoras(self):
        """
        手牌の赤ドラの数

        Returns
        count : int
            手牌の赤ドラの数
        """
        count = 0
        tiles = self.hands[:] + sum(self.melds, [])
        for i in tiles:
            if i.akadora: count += 1
        return(count)

    def doras(self):
        """
        Returns
        count : int
            手牌の内、ドラ表示牌の次の牌の数と、赤ドラの数の和
        """
        return(self.displayed_doras() + self.akadoras())

    def shuntus(self):
        """
        手牌の内、順子のリストを返す

        Returns
        -------
        tiles : list
            手牌の順子のリスト。順子1つごとにMahjongTile3枚のリストになっているためリストのリストが返る
        """
        tiles = self.hands[:]
        mentus = []
        self.make_shuntus(tiles, mentus)
        return(mentus)

    def ankos(self):
        """
        手牌の内、暗刻のリストを返す

        Returns
        -------
        tiles : list
            手牌の暗刻のリスト。暗刻1つごとにMahjongTile3枚のリストになっているためリストのリストが返る
        """
        tiles = self.hands[:]
        mentus = []
        self.make_kotus(tiles, mentus)
        if self.is_tumo or self.is_ron:
            for i in mentus:
                if self.latest_tile in i:
                    mentus.remove(i)
        return(mentus)

    def kotus(self):
        """
        Returns
        -------
        tiles : list
            手牌の刻子のリスト。刻子1つごとにMahjongTile3枚のリストになっているためリストのリストが返る
        """
        return(self.ankos() + self.minkos)

    def kantus(self):
        """
        Returns
        -------
        tiles : list
            手牌の槓子のリスト。槓子1つごとにMahjongTile3枚のリストになっているためリストのリストが返る
        """
        return(self.ankans + self.minkans)

    def yakus(self, cache=True):
        """
        プレイヤーの手牌でできる役のリストを返す

        Parameters
        ----------
        cache : bool
            キャッシュを使用するかどうか(Falseにするとキャッシュの有無を無視して再計算します)

        Returns
        -------
        yakus : list
            役のリスト。役の名前(適当ローマ字表記)が入っている
        """
        if not self.is_hora: raise RuntimeError('Not hora')
        yakus = []

        if self.tiles_cache != self.hands:
            cache = False
            self.tiles_cache = self.hands[:]

        if self.yakus_cache != [] and cache:
            return(self.yakus_cache)

        if self.is_riichi: yakus.append('riichi')
        if self.riichi_turn + 1 == self.turn: yakus.append('ippatu')
        if self.is_menzen() and self.is_tumo: yakus.append('menzentumo')
        tiles = self.hands[:] + sum(self.melds, [])
        table_wind = 'ton' if self.table is None else self.table.wind
        TILE_TYPES_YAKUHAI = self.TILE_TYPES[7:] + [self.wind] + [table_wind]
        for i in TILE_TYPES_YAKUHAI:
            if tiles.count(mahjongpy.MahjongTile(i)) == 3:
                yakus.append('yakuhai')
        kuitan = 'True' if self.table is None else self.table.kuitan
        tmp = tiles[:] if kuitan else self.hands[:]
        count = 0
        count += tmp.count(mahjongpy.MahjongTile('pinzu',1))
        count += tmp.count(mahjongpy.MahjongTile('pinzu',9))
        count += tmp.count(mahjongpy.MahjongTile('manzu',1))
        count += tmp.count(mahjongpy.MahjongTile('manzu',9))
        count += tmp.count(mahjongpy.MahjongTile('souzu',1))
        count += tmp.count(mahjongpy.MahjongTile('souzu',9))
        count += tmp.count(mahjongpy.MahjongTile('ton'))
        count += tmp.count(mahjongpy.MahjongTile('nan'))
        count += tmp.count(mahjongpy.MahjongTile('sha'))
        count += tmp.count(mahjongpy.MahjongTile('pei'))
        count += tmp.count(mahjongpy.MahjongTile('haku'))
        count += tmp.count(mahjongpy.MahjongTile('hatu'))
        count += tmp.count(mahjongpy.MahjongTile('tyun'))
        if count == 0: yakus.append('tanyao')
        if self.is_menzen() and len(self.shuntus()) == 4 and self.zyantou()[0].tile_type not in TILE_TYPES_YAKUHAI and self.is_wait_ryanmen(): yakus.append('pinfu')
        if self.is_ipeikou(self.hands[:], []): yakus.append('ipeikou')
        table_tiles = [] if self.table is None else self.table.tiles
        if len(table_tiles) == 14 and self.is_tumo: yakus.append('haitei')
        if len(table_tiles) == 14 and self.is_ron: yakus.append('houtei')
        if False: yakus.append('rinsyankaihou')
        if False: yakus.append('tyankan')
        if self.is_doubleriichi: yakus.append('doubleriichi')
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
        if len(self.ankos()) == 3 or len(self.ankos())+len(self.ankans)==3: yakus.append('sanankou')
        #if len(self.minkos) < 2  and len(self.kotus())+len(self.kantus()) == 3: yakus.append('sanankou')
        #if len(self.minkos) == 1  and len(self.kotus())+len(self.kantus()) == 4: yakus.append('sanankou')
        if len(self.kotus()) == 4 or len(self.kotus())+len(self.kantus()) == 4:
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
        if len([i for i in tiles if i.number in [1,9,None]]) == 14 and (not self.is_kokushimusou()): yakus.append('honroutou')
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
                    count.append(self.hands.count(mahjongpy.MahjongTile(i,j)))
                if count.count(3)==2 and count.count(2)==1 and count.count(1)==6: yakus.append('tyurenboutou')
            is_furoed = False if self.table is None else self.table.is_furoed
            if not is_furoed and self.oya==False and self.turn == 0: yakus.append('chihou')
            if self.oya==True and self.turn==0: yakus.append('tenhou')

        self.yakus_cache = yakus
        return(yakus)

    def score_fu(self, debug=False):
        """
        Parameters
        ----------
        debug : bool
            符の内訳を表示

        Returns
        -------
        score_fu : int
            手牌の符数
        """
        yakus = self.yakus()
        if self.is_tumo and 'pinfu' in yakus: return(20)
        if 'chitoitu' in yakus: return(25)

        score_fu = 20
        if debug: print('Futei:20')

        if self.is_menzen() and self.is_ron:
            score_fu += 10
            if debug: print('Menzen&Ron:10')
        elif self.is_tumo:
            score_fu += 2
            if debug: print('Tumo:2')

        for i in self.minkos:
            if i[0].number in range(2,9):
                score_fu += 2
                if debug: print('Tyuntyanpai Minko:2')
            else:
                score_fu += 4
                if debug: print('Yaotyuhai Minko:4')
        #ankos = []
        #self.make_kotus(self.hands[:], ankos)
        for i in self.ankos():
            if i[0].number in range(2,9):
                score_fu += 4
                if debug: print('Tyuntyanpai Anko:4')
            else:
                score_fu += 8
                if debug: print('Yaotyuhai Anko:8')
        for i in self.minkans:
            if i[0].number in range(2,9):
                score_fu += 8
                if debug: print('Tyuntyanpai Minkan:8')
            else:
                score_fu += 16
                if debug: print('Yaotyuhai Minkan:16')
        for i in self.ankans:
            if i[0].number in range(2,9):
                score_fu += 16
                if debug: print('Tyuntyanpai Ankan:16')
            else:
                score_fu += 32
                if debug: print('Yaotyuhai Ankan:32')
        table_wind = "" if self.table is None else self.table.wind
        if self.zyantou()[0].tile_type in ['haku', 'hatu', 'tyun', self.wind, table_wind]:
            score_fu += 2
            if debug: print('Zyantou Yakuhai:2')
        if (not self.is_wait_ryanmen()) and (not self.is_wait_syabo()):
            score_fu += 2
            if debug: print('Not ryanmenmachi:2')

        if debug: print('sum:{}'.format(score_fu))
        if score_fu % 10 == 0: score_fu -= 10
        score_fu = ((score_fu // 10)+1)*10
        score_fu = max(30, score_fu)

        if debug: print('kiriage:{}'.format(score_fu))
        return(score_fu)

    def score_han(self, debug=False):
        """
        Parameters
        ----------
        debug : bool
            翻の内訳を表示
        Returns
        -------
        score_fu : int
            手牌の翻数
        """
        if self.is_yakuman():
            if debug: print('yakuman')
            return(13)
        elif self.is_doubleyakuman():
            if debug: print('doubleYakuman')
            return(23)
        elif self.is_tripleyakuman():
            if debug: print('TripleYakuman')
            return(30)
        yaku_hans =  {'riichi':1, 'ippatu':1, 'menzentumo':1, 'pinfu':1, 'tanyao':1, 'ipeikou':1, 'yakuhai':1, \
                    'rinsyankaihou':1, 'haitei':1, 'houtei':1, 'tyankan':1, 'doubleriichi':2, 'chanta':2, \
                    'ikkituukan':2, 'sansyokudouzyun':2, 'sansyokudoukou':2, 'sanankou':2, 'sankantu':2, \
                    'toitoi':2, 'chitoitu':2, 'zyuntyan':3, 'ryanpeikou':3, 'honitu':3, 'honroutou':4, \
                    'syousangen':4, 'chinitu':6}
        yaku_hans_furoed = dict(yaku_hans.items())
        yaku_hans_furoed['tyankan'] = 1
        yaku_hans_furoed['ikkituukan'] = 1
        yaku_hans_furoed['sansyokudouzyun'] = 1
        yaku_hans_furoed['zyuntyan'] = 2
        yaku_hans_furoed['honitu'] = 2
        yaku_hans_furoed['chinitu'] = 5
        score_han = 0
        yakus = self.yakus()
        if self.is_menzen():
            for i in yakus:
                score_han += yaku_hans[i]
                if debug: print('{}:{}'.format(i,yaku_hans[i]))
        else:
            for i in yakus:
                score_han += yaku_hans_furoed[i]
                if debug: print('{}(kui):{}'.format(i,yaku_hans[i]))

        score_han += self.doras()
        if debug: print('dora:{}'.format(self.displayed_doras()))
        if debug: print('akadora:{}'.format(self.akadoras()))

        if debug: print('sum:{}'.format(score_han))
        return(score_han)

    def is_mangan(self):
        """
        Returns
        -------
        is_mangan : bool
            満貫かどうか
        """
        fu = self.score_fu()
        han = self.score_han()
        return((han==3 and fu>69) or (han==4 and fu>39) or (han==5))

    def is_haneman(self):
        """
        Returns
        -------
        is_haneman : bool
            跳満かどうか
        """
        return(self.score_han() in [6,7])

    def is_baiman(self):
        """
        Returns
        -------
        is_baiman : bool
            倍満かどうか
        """
        return(self.score_han() in [8,9,10])

    def is_sanbaiman(self):
        """
        Returns
        -------
        is_sanbaiman : bool
            三倍満かどうか
        """
        return(self.score_han() in [11,12,13])

    def is_kazoeyakuman(self):
        """
        Returns
        -------
        is_kazoeyakuman : bool
            数え役満かどうか
        """
        return(self.score_han() > 12)

    def yakuman_count(self):
        """
        Returns
        -------
        count : int
            役満の役の数
        """
        count = 0
        for i in self.yakus():
            if i in ['suankou', 'daisangen', 'kokushimusou', 'ryuisou', 'tuisou', 'chinroutou', 'sukantu', \
                    'syoususi', 'daisusi', 'tyurenboutou', 'chihou', 'tenhou']:
                count += 1
        return(count)

    def is_yakuman(self):
        """
        Returns
        -------
        is_sanbaiman : bool
            役満かどうか
        """
        return(self.yakuman_count()==1)

    def is_doubleyakuman(self):
        """
        Returns
        -------
        is_sanbaiman : bool
            ダブル役満かどうか
        """
        return(self.yakuman_count()==2)

    def is_tripleyakuman(self):
        """
        Returns
        -------
        is_sanbaiman : bool
            トリプル役満かどうか
        """
        return(self.yakuman_count()==3)

    def score_ron(self):
        """
        Returns
        -------
        score : int
            ロンのときの獲得点数
        """
        SCORE_OYA = [[0,0,1500,2000,2400,2900,3400,3900,4400,4800,5300], \
                     [2100,2400,2900,3900,4800,5800,6800,7700,8700,9600,10600], \
                     [3900,4800,5800,7700,9600,11600]+[12000]*5, \
                     [7800,9600,11600]+[12000]*8, \
                     [12000]]+[[18000]]*2+[[24000]]*3+[[36000]]*2+[[48000]]*9+[[96000]]*9+[[144000]]*9
        SCORE_KO = [[0,0,1000,1300,1600,2000,2300,2600,2900,3200,3600], \
                    [1500,1600,2000,2600,3200,3900,4500,5200,5800,6400,7100], \
                    [2700,3200,3900,5200,6400,7700]+[8000]*5, \
                    [5200,6400,7700]+[8000]*8, \
                    [8000]]+[[12000]]*2+[[16000]]*3+[[24000]]*2+[[32000]]*9+[[64000]]*9+[[96000]]*9
        fu_index = ([20,25] + [i*10 for i in range(3,12)]).index(self.score_fu())
        if self.score_han() > 4:fu_index = 0
        if self.oya:
            score = SCORE_OYA[self.score_han()-1][fu_index]
        else:
            score = SCORE_KO[self.score_han()-1][fu_index]
        return(score)

    def score_without_tsumibo(self):
        """
        Returns
        -------
        score : int
            手牌の点数(場の積み棒分の点数を除く)
        """
        if not self.is_hora: raise RuntimeError('Not hora')

        if self.score_without_tsumibo_cache != 0: return(self.score_without_tsumibo_cache)

        score = self.score_ron()
        if self.is_tumo:
            if self.oya:
                tmp = ((score//100)//3)*100
                if (score//100) % 3 != 0:
                    tmp += 100
                score = tmp * 3
            else:
                tmp_oya = ((score//100)//2)*100
                if (score//100) % 2 != 0:
                    tmp_oya += 100
                tmp_ko = ((score//100)//4)*100
                if (score//100) % 4 != 0:
                    tmp_ko += 100
                score = tmp_oya + tmp_ko*2

        self.score_without_tsumibo_cache = score
        return(score)

    def score(self):
        """
        Returns
        -------
        score : int
            手牌の点数(積み棒分を含む)
        """
        if self.score_cache != 0: return(self.score_cache)
        honba = 0 if self.table is None else self.table.honba

        self.score_cache = self.score_without_tsumibo() + honba*300
        return(self.score_cache)

    def payed_score(self):
        """
        Returns
        -------
        score : list
            他家に払ってもらう手牌の点数のリスト。
            [ロンした時に振り込んだ人に払ってもらう点数, 親に払ってもらう点数, 子に払ってもらう点数]
        """
        score = self.score_ron()
        honba = 0 if self.table is None else self.table.honba
        if not self.is_hora: raise RuntimeError('Not hora')
        if self.is_ron: return([self.score(), 0, 0])
        elif self.oya:
            tmp = ((score//100)//3)*100
            if (score//100) % 3 != 0:
                tmp += 100
            tmp += honba*100
            return([0, 0, tmp])
        else:
            tmp_oya = ((score//100)//2)*100
            if (score//100) % 2 != 0:
                tmp_oya += 100
            tmp_oya += honba*100
            tmp_ko = ((score//100)//4)*100
            if (score//100) % 4 != 0:
                tmp_ko += 100
            tmp_ko += honba*100
            return([0, tmp_oya, tmp_ko])

    def is_menzen(self):
        """
        Returns
        -------
        is_menzen : bool
            門前かどうか
        """
        return((len(self.melds)-len(self.ankans))==0)

    def is_wait_ryanmen(self):
        """
        Returns
        -------
        is_wait_ryanmen : bool
            両面待ちかどうか
        """
        tiles = []
        if self.latest_tile.number is None: return(False)
        if self.latest_tile.number > 2:
            tiles.append(mahjongpy.MahjongTile(self.latest_tile.tile_type, self.latest_tile.number-2))
        if self.latest_tile.number < 8:
            tiles.append(mahjongpy.MahjongTile(self.latest_tile.tile_type, self.latest_tile.number+2))
        return(any([(i in self.hands) for i in tiles]))

    def is_wait_syabo(self):
        """
        Returns
        -------
        is_wait_syabo : bool
            シャボ待ちかどうか
        """
        return(self.hands.count(self.latest_tile) == 3)

    def discard(self, tile):
        """
        牌を捨てる

        Parameters
        ----------
        tile : MahjongTile
            捨てる牌

        """
        if not tile in self.hands:
            raise RuntimeError('does NOT have such tile')
        else:
            self.turn += 1
            self.discards.append(self.hands.pop(self.hands.index(mahjongpy.MahjongTile(tile.tile_type,tile.number,akadora=tile.akadora))))

    def riichi(self):
        """
        リーチする

        Raises
        ------
        RuntimeError
            門前でないと鳴けない
            テンパイでないと鳴けない
        """
        if not self.is_menzen(): raise RuntimeError('Can Riichi ONLY when menzen')
        if not self.is_tenpai(): raise RuntimeError('Can Riichi ONLY when tenpai')
        if self.points < 1000: raise RuntimeError('Cannot Richii by lack of points')
        if self.table is not None and len(self.table.tiles) < 4: raise RuntimeError('Cannot Riichi by lack of table tiles')
        is_furoed = False if self.table is None else self.table.is_furoed
        if self.turn == 0 and is_furoed: self.doubleriichi = True
        self.riichi_turn = self.turn
        self.is_riichi = True
        if self.table is not None: self.table.ri_bou += 1

    def can_pon(self, tile):
        """
        Parameters
        ----------
        tile : MahjongTile
            他家が捨てた牌

        Returns
        -------
        can_pon : bool
            ポンできるかどうか
        """
        return(self.hands.count(tile) > 1)

    def can_chi(self, tile):
        """
        Parameters
        ----------
        tile : MahjongTile
            上家が捨てた牌

        Returns
        -------
        can_pon : bool
            チーできるかどうか
        """
        if tile.tile_type in self.TILE_TYPES[3:]: return(False)
        count = []
        if tile.number>2:
            count.append(self.hands.count(mahjongpy.MahjongTile(tile.tile_type,tile.number-2)))
        else:
            count.append(0)
        if tile.number>1:
            count.append(self.hands.count(mahjongpy.MahjongTile(tile.tile_type,tile.number-1)))
        else:
            count.append(0)
        if tile.number<9:
            count.append(self.hands.count(mahjongpy.MahjongTile(tile.tile_type,tile.number+1)))
        else:
            count.append(0)
        if tile.number<8:
            count.append(self.hands.count(mahjongpy.MahjongTile(tile.tile_type,tile.number+2)))
        else:
            count.append(0)

        judge = False
        for i in range(3):
            if count[i:i+2].count(1) == 2:
                judge = True
        return(judge)

    def can_ankan(self):
        """
        Returns
        -------
        can_ankan : bool
            暗槓できるかどうか
        """
        count = []
        for i in self.TILE_TYPES:
            for j in range(1,10):
                count.append(self.hands.count(mahjongpy.MahjongTile(i,j)))
        return(count.count(4) > 0)

    def can_minkan(self, tile):
        """
        Parameters
        ----------
        tile : MahjongTile
            他家が捨てた牌

        Returns
        -------
        can_minkan : bool
            明槓できるかどうか
        """
        return(self.hands.count(tile)==3)

    def can_kakan(self):
        """
        Returns
        -------
        can_kakan : bool
            加槓できるかどうか
        """
        judge = False
        for i in self.hands:
            for j in self.minkos:
                if j[0] == i:
                    judge = True
        return(judge)

    def can_ron(self, tile):
        """
        Parameters
        ----------
        tile : MahjongTile
            他家が捨てた牌

        Returns
        -------
        can_tumo : bool
            ツモできるかどうか
        """
        return(mahjongpy.MahjongPlayer(hands=self.hands[:]+[tile],melds=self.melds[:]).is_hora())

    def kan(self, tile):
        """
        カンする(暗槓または大明槓)

        Parameters
        ----------
        tile : MahjongTile
            カンする牌
        """
        p = None
        players = [None] if self.table is None else self.table.players
        count = self.hands.count(tile)
        if count != 4:
            for i in players:
                if len(i.discards) != 0 and i.discards[-1] == tile:
                    p = i
        if p is None and count != 4: raise RuntimeError('Nobody discards such tile')
        if count < 3: raise RuntimeError('Lack of amount of tiles for kan')
        tmp = []
        if p is None: #暗槓
            for _ in range(4):
                tmp.append(self.hands.pop(self.hands.index(tile)))
            self.ankans.append(tmp)
            self.melds.append(tmp[:3])
            self.table.draw(self)
            if self.is_hora: self.is_rinsyankaihou = True
            self.table.add_kandora()
            #self.discard(SOME_TILE)
        else:
            for _ in range(3): #大明槓
                tmp.append(self.hands.pop(self.hands.index(tile)))
            tmp.append(p.discards.pop(p.discards.index(tile)))
            index = 0 if self.table is None else {0:3,1:1,2:0}[self.table.players[1:].index(p)]
            tmp[index].from_tacha = True
            self.minkans.append(tmp)
            self.melds.append(tmp[:3])
            self.table.draw(self)
            if self.is_hora:self.is_rinsyankaihou = True
            if self.table.kandora_sokumekuri:
                self.table.add_kandora()
                #self.discard(SOME_TILE)
            else:
                pass
                #self.discard(SOME_TILE)
                #self.table.add_kandora()

    def kakan(self, tile):
        """
        カンする(加槓(小明槓))

        Parameters
        ----------
        tile : MahjongTile
            カンする牌
        """
        if not tile in self.hands: raise RuntimeError('You DON\'T have such tile')
        flag = False
        index = None
        for i in range(len(self.minkos)):
            if self.minkos[i][0] == tile:
                flag = True
                index = i
        if not flag: raise RuntimeError('You DON\'T have such tile of minko')
        tmp = self.hands.pop(self.hands.index(tile))
        self.minkans.append(self.minkos[i]+[tile])

    def pon(self, tile):
        """
        ポンする

        Parameters
        ----------
        tile : MahjongTile
            ポンする牌
        """
        p = None
        players = [None] if self.table is None else self.table.players
        for i in players:
            if len(i.discards) != 0:
                if i.discards[-1] == tile:
                    p = i
        count = self.hands.count(tile)
        if p is None: raise RuntimeError('Nobody discards such tile')
        if count != 2: raise RuntimeError('You DON\'T have toitu of such tile')
        tmp = []
        for _ in range(2):
            tmp.append(self.hands.pop(self.hands.index(tile)))
        tmp.append(p.discards.pop(p.discards.index(tile)))
        index = 0 if self.table is None else {0:2,1:1,2:0}[self.table.players[1:].index(p)]
        tmp[index].from_tacha = True
        self.melds.append(tmp)
        self.minkos.append(tmp)

    def chi(self, tile):
        """
        チーする

        Parameters
        ----------
        tile : MahjongTile
            チーする牌
        """
        p = None
        players = [None] if self.table is None else self.table.players
        for i in players:
            if len(i.discards) != 0:
                if i.discards[-1] == tile:
                    p = i
        if p is None: raise RuntimeError('Nobody discards such tile')
        tiles = self.hands + [tile]
        shuntus = []
        self.make_shuntus(tiles, shuntus)
        tmp = []
        for i in shuntus:
            for j in i:
                if j == tile:
                    tmp = i
        tmp2 = []
        for i in tmp:
            if i == tile:
                tmp2.append(p.discards.pop(p.discards.index(i)))
            else:
                tmp2.append(self.hands.pop(self.hands.index(i)))
        self.melds.append(tmp2)

    def ron(self, tile):
        """
        ロンする

        Parameters
        ----------
        tile : MahjongTile
            ロンする牌
        """
        p = None
        players = [None] if self.table is None else self.table.players
        for i in players:
            if len(i.discards) != 0 and i.discards[-1] == tile:
                p = i
        self.hands.append(tile)
        self.sort()
        if not self.is_hora():
            raise RuntimeError('Cannot hora')
            self.hands.pop(self.hands.index(tile))
        elif len(self.yakus()) == 0:
            raise RuntimeError('NO YAKUS!!')
        else:
            self.is_ron = True
            if self.riichi and self.table is not None:
                for i in range(len(self.table.dora_tiles)):
                    self.table.add_kandora(ura=True)
        if self.table is not None:
            self.table.furikomi_player = p
            self.table.win_player = self
            self.table.calculate_score()

    def tumo(self):
        """
        ツモする
        """
        if not self.is_hora():
            raise RuntimeError('Cannot hora')
        elif len(self.yakus()) == 0:
            raise RuntimeError('NO YAKUS!!')
        else:
            self.is_tumo = True
            if self.table is not None:
                self.table.win_player = self
                self.table.calculate_score()
            if self.riichi and self.table is not None:
                for i in range(len(self.table.dora_tiles)):
                    self.table.add_kandora(ura=True)


    def next_player(self):
        """
        Returns
        -------
        player : MahjongPlayer
            自身の次のプレイヤー
        """
        players = [None]*4 if self.table is None else self.table.players
        p1, p2, p3, p4 = players
        next_player = {p1:p2, p2:p3, p3:p4, p4:p1}
        return(next_player[self])

