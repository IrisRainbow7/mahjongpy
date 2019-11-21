import mahjongpy
import random

class MahjongTable:
    """
    麻雀卓を表すクラス
    卓のルールや情報を保持する

    Attributes
    ----------
    tiles : list
        場の牌山(MahjongTileのリスト)
    wind : str
        現在の場の風。東:'ton'　南:'nan'　東:'sha'　北:'pei'
    kyoku : int
        現在の局数。東1局なら1
    honba : int
        現在の局が何本場か
    dora_showing_tiles : list
        ドラ表示牌(MahjongTile)のリスト
    uradora_showing_tiles : list
        裏ドラ表示牌(MahjongTile)のリスト
    dora_tiles : list
        ドラ牌(MahjongTile)のリスト
    ri_bou : int
        リー棒の数
    players : list
        MahjongPlayer4人のリスト
    use_akadora : bool
        赤ドラを使用するかどうか(デフォルト:True)
    kuitan : bool
        喰いタン(門前でないタンヤオ)ありかどうか(デフォルト:True)
    kandora_sokumekuri : bool
        槓ドラ即めくりするかどうか(デフォルト:False)
    rules : dict
        ルールを表す辞書(use_akadora, kuitan, kandora_sokumekuri)
    round_name_jp : str
        局の風と数を表す文字列。"東1局"、"東3局"
    info : str
        round_name_jpに加え何本場かを示す文字列。"東2局1本場"
    is_furoed : bool
        誰か1人でもすでに鳴いたかどうか
    """

    WIND_NAME_JP = {'ton':'東', 'nan':'南', 'sha':'西', 'pei':'北'}

    def __init__(self, tiles=[], wind="ton", kyoku=1, honba=0, dora_showing_tiles=[], dora_tiles=[], \
                players=[], use_akadora=True, kuitan=True, kandora_sokumekuri=False, rules={}):
        self.tiles = mahjongpy.MahjongTile.make_tiles_set(use_akadora=rules.get('use_akadora', use_akadora))
        random.shuffle(self.tiles)
        self.wind = wind
        self.kyoku = kyoku
        self.honba = honba
        self.dora_showing_tiles = dora_showing_tiles[:]
        self.uradora_showing_tiles = [][:]
        self.dora_tiles = dora_tiles[:]
        self.dora_showing_tiles.append(self.tiles.pop(random.randrange(136)))
        self.dora_tiles.append(self.dora_showing_tiles[0].next())
        self.ri_bou = self.honba
        h1, h2, h3, h4 = self.deal_tiles()
        p1 = mahjongpy.MahjongPlayer(hands=h1, oya=True, wind='ton', table=self)
        p2 = mahjongpy.MahjongPlayer(hands=h2, wind='nan', table=self)
        p3 = mahjongpy.MahjongPlayer(hands=h3, wind='sha', table=self)
        p4 = mahjongpy.MahjongPlayer(hands=h4, wind='pei', table=self)
        self.players = [p1, p2, p3, p4]
        self.use_akadora = rules.get('use_akadora', use_akadora)
        self.kuitan = rules.get('kuitan', kuitan)
        self.kandora_sokumekuri = rules.get('kandora_sokumekuri', kandora_sokumekuri)
        self.round_name_jp = self.WIND_NAME_JP[self.wind] + str(kyoku) + '局'
        self.info = self.round_name_jp + str(self.honba) + '本場'
        self.is_furoed = False

    def deal_tiles(self,oya=1):
        """
        配牌する

        Parameters
        ----------
        oya : int
            何人目のプレイヤーが親かを示す(1～4)

        Returns
        -------
        hands : list
            プレイヤーの手牌のリスト　*4人分。親のみ14枚他3人は13枚
        """
        hands = [[], [], [], []]
        for i in range(4):
            for _ in range(13):
                hands[i].append(self.tiles.pop(random.randrange(10)))
        hands[oya-1].append(self.tiles.pop(random.randrange(10)))
        return(hands)

    def draw(self, player):
        """
        山から牌を引き、プレイヤーに配る

        Parameters
        ----------
        player : MahjongPlayer
            牌を配るプレイヤー
        """
        draw_tile = self.tiles.pop(random.randrange(5))
        player.hands.append(draw_tile)
        player.latest_tile = draw_tile
        player.sort()

    def add_kandora(self, ura=False):
        """
        カンドラをめくる
        """
        tile = self.tiles.pop(random.randrange(5))
        if ura:
            self.uradora_showing_tiles.append(tile)
        else:
            self.dora_showing_tiles.append(tile)
        self.dora_tiles.append(tile.next())

    def tiles_left(self):
        """
        Returns
        -------
        count : int
            残りの牌の枚数
        """
        return(len(self.tiles)-14)
