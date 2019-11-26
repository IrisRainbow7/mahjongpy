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
    oya_player : int
        1～４。何人目のプレイヤーが親か
    p1_wind : int
        プレイヤー1の自風。1:東　2:南　3:西　4:北
    players_points : list of int
        プレイヤーの得点
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
    win_player : MahjongPlayer
        この卓の勝者
    furikomi_player : MahjongPlayer
        ロンで和了った時に振り込んだプレイヤー
    """

    WIND_NAME_JP = {'ton':'東', 'nan':'南', 'sha':'西', 'pei':'北'}

    def __init__(self, tiles=[], wind="ton", kyoku=1, honba=0, dora_showing_tiles=[], dora_tiles=[], \
                ri_bou=0, players=[], oya_player=1, p1_wind=0, players_points=[25000]*4, use_akadora=True, kuitan=True, \
                kandora_sokumekuri=False, rules={}):
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
        self.ri_bou = ri_bou
        self.oya_player = oya_player
        self.p1_wind = p1_wind
        h1, h2, h3, h4 = self.deal_tiles()
        p_is_oya = []
        for i in range(1,5):
            p_is_oya.append(i==self.oya_player)
        wind_rot = ['ton','nan','sha','pei','ton','nan','sha','pei']
        p1 = mahjongpy.MahjongPlayer(hands=h1, oya=p_is_oya[0], wind=wind_rot[self.p1_wind], points=players_points[0], table=self)
        p2 = mahjongpy.MahjongPlayer(hands=h2, oya=p_is_oya[1], wind=wind_rot[self.p1_wind+1], points=players_points[1], table=self)
        p3 = mahjongpy.MahjongPlayer(hands=h3, oya=p_is_oya[2], wind=wind_rot[self.p1_wind+2], points=players_points[2], table=self)
        p4 = mahjongpy.MahjongPlayer(hands=h4, oya=p_is_oya[3], wind=wind_rot[self.p1_wind+3], points=players_points[3], table=self)
        self.players = [p1, p2, p3, p4]
        self.use_akadora = rules.get('use_akadora', use_akadora)
        self.kuitan = rules.get('kuitan', kuitan)
        self.kandora_sokumekuri = rules.get('kandora_sokumekuri', kandora_sokumekuri)
        self.round_name_jp = self.WIND_NAME_JP[self.wind] + str(kyoku) + '局'
        self.info = self.round_name_jp + str(self.honba) + '本場'
        self.is_furoed = False
        self.win_player = None
        self.furikomi_player = None
        self.is_ryukyoku = False

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

    def calculate_score(self):
        """
        点数を分配します
        """
        if self.win_player is None and not self.is_ryukyoku: raise RuntimeError('Round NOT finished')
        if self.is_ryukyoku:
            tenpai_count = len([i for i in self.players if i.is_tenpai()])
            if tenpai_count in [0,4]: return()
            t_score = int(3000 / tenpai_count)
            nt_score = int(3000 / (4-tenpai_count))
            for i in self.players:
                if i.is_tenpai():
                    i.points += t_score
                else:
                    i.points -= nt_score
        else:
            score = self.win_player.payed_score()
            if self.win_player.is_tumo:
                self.win_player.points += self.win_player.score()
                for i in self.players:
                    if i==self.win_player: continue
                    elif i.oya: i.points -= score[1]
                    else: i.points -= score[2]
            elif self.win_player.is_ron:
                self.win_player.points += self.win_player.score()
                self.furikomi_player.points -= score[0]


    def next_round(self):
        """
        次の局に進みます

        Notes
        -----
        self.tablesおよびself.playersが更新されるので再取得してください
        """
        NEXT_WIND = {'ton':'nan', 'nan':'sha', 'sha':'pei', 'pei':'ton'}
        if self.is_ryukyoku:
            self.win_player = mahjongpy.MahjongPlayer(hands=[42]*13,oya=False)
        if self.win_player is None: raise RuntimeError('self.win_player is not setted')
        if self.win_player.oya:
            self.honba += 1
        else:
            self.kyoku += 1
            if self.kyoku == 5:
                self.wind = NEXT_WIND[self.wind]
                self.kyoku = 1
            self.oya_player += 1
            if self.oya_player == 5: self.oya_player = 1
        self.p1_wind += 1
        if self.p1_wind == 5: self.p1_wind = 1
        players_points = []
        for i in self.players:
            players_points.append(i.points)
        return(MahjongTable(kyoku=self.kyoku, wind=self.wind, honba=self.honba, oya_player=self.oya_player, p1_wind=self.p1_wind, ri_bou=self.ri_bou, use_akadora=self.use_akadora, kuitan=self.kuitan, kandora_sokumekuri=self.kandora_sokumekuri, players_points=players_points))

    def ryukyoku(self):
        """
        流局する
        """
        self.is_ryukyoku = True
        self.calculate_score()
