class MahjongTile:
    """
    麻雀牌を表すクラス

    Attributes
    ----------
    tile_type : str
        牌の種類。萬子:manzu　pinzu:筒子　souzu:索子　ton:東　nan:南　sha:東　pei:北　haku:白　hatu:發　tyun:中
    number : int
        牌の数字。字牌の場合はNone
    akadora : bool
        赤ドラかどうか
    from_tacha : bool
        他家からの牌かどうか(鳴いた時に他家からの牌を横向きに表示する時の判定に使用)
    """

    TILE_TYPES = ['manzu', 'pinzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    TILE_TYPES_ZIHAI = ['ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    NUMBER_READING_JP = {1:'イー', 2:'リャン', 3:'サン', 4:'スー', 5:'ウー', 6:'ロー', 7:'チー', 8:'パー', 9:'キュー', None:''}
    TILE_READING_JP = {'manzu':'ワン', 'pinzu':'ピン', 'souzu':'ソー', 'ton':'トン', 'nan':'ナン', 'sha':'シャー', 'pei':'ペイ', 'haku':'ハク', 'hatu':'ハツ', 'tyun':'チュン', None:'虚無'}
    TILE_DISPLAY = {'manzu':'萬', 'pinzu':'●', 'souzu':'Ⅰ', 'ton':'東', 'nan':'南', 'sha':'西', 'pei':'北', 'haku':'白', 'hatu':'發', 'tyun':'中', None:'虚無'}
    NEXT_ZIHAI = {'ton':'nan', 'nan':'sha', 'sha':'pei', 'pei':'ton', 'haku':'hatu', 'hatu':'tyun', 'tyun':'haku'}

    def __init__(self, tile_type, number=1, akadora=False, from_tacha=False):
        if not tile_type in self.TILE_TYPES+[None]: raise ValueError('unknown tile types')
        if not number in [i for i in range(1,10)]+[None]: raise ValueError('unknown tile types')
        self.tile_type = tile_type
        self.number = number
        if tile_type in self.TILE_TYPES_ZIHAI: self.number = None
        self.akadora = akadora
        self.from_tacha = from_tacha
        self.name_jp = self.NUMBER_READING_JP[self.number] + self.TILE_READING_JP[self.tile_type]
        self.display = str(self.number) + self.TILE_DISPLAY[self.tile_type]
        if self.akadora:
            self.display += '*'
            self.name_jp += '*'
        if self.number is None: self.display = self.TILE_DISPLAY[self.tile_type]

    @classmethod
    def make_tiles_set(cls, use_akadora=True):
        """
        1局で使用する麻雀牌34種136枚のセットを生成

        Parameters
        ----------
        use_akadora : bool
            赤ドラを入れるかどうか

        Returns
        -------
        tiles : list
            MahjongTile136枚のリスト
        """
        tiles = []
        for _ in range(4):
            for i in range(1,10):
                tiles.append(MahjongTile('manzu',i))
                tiles.append(MahjongTile('souzu',i))
                tiles.append(MahjongTile('pinzu',i))
            tiles.append(MahjongTile('ton'))
            tiles.append(MahjongTile('nan'))
            tiles.append(MahjongTile('sha'))
            tiles.append(MahjongTile('pei'))
            tiles.append(MahjongTile('haku'))
            tiles.append(MahjongTile('hatu'))
            tiles.append(MahjongTile('tyun'))
        if use_akadora:
            tiles.pop(12)
            tiles.pop(12)
            tiles.pop(12)
            tiles.append(MahjongTile('manzu',5,akadora=True))
            tiles.append(MahjongTile('souzu',5,akadora=True))
            tiles.append(MahjongTile('pinzu',5,akadora=True))
        return(tiles)

    @classmethod
    def make_hands_set(cls, man='', sou='', pin='', wind='', zihai='', checkamount=True):
        """
        指定された種類と枚数の牌のリスト(手牌)を作成する

        Parameters
        ----------
        man : str
            萬子の種類と枚数。種類(数字)を必要枚数分並べる。
            例:一萬2枚を五萬と六萬と七萬　->　"11567"
        sou : str
            索子の種類と枚数
            例:二索3枚と九索3枚　->　"222999"
        pin : str
            筒子の枚数と種類
            例:一筒から九筒まで1枚ずつ　->　"123456789"
        wind : str
            風牌の種類と枚数。東南西北の順で1～4で表す
            例:東2枚と北3枚　->　"11444"
        zihai : str
            字牌の三元牌の種類と枚数。白發中の順で1～4で表す
            例:白3枚と發3枚　->　"111222"
        checkamount : bool
            枚数チェックをするかどうか。デフォルトTrue
            13枚または14枚でない場合例外を投げる(手牌生成するとき用)

        Returns
        -------
        tiles : list
            MahjongTileのリスト

        Raises
        ------
        ValueError
            牌の枚数が13または14でないとき(checkamount=Falseで枚数が足りなくても無視して生成)

        Examples
        --------
        >>> hands_pinfu = mahjongpy.MahjongTile.make_hands_set('22345', '567', '123567') #平和
        >>> hands_chitoitu = mahjongpy.MahjongTile.make_hands_set('1155', '77', '3399', '22', '33') #七対子
        >>> hands_daisangen = mahjongpy.MahjongTile.make_hands_set('123', '77', '', '', '111222333') #大三元
        >>> hands_kokushi = mahjongpy.MahjongTile.make_hands_set('19', '19', '19', '1234', '1233') #国士無双
        >>> hands_lack_of_amout = mahjongpy.MahjongTile.make_hands_set('123', '456', '789') #枚数不足
        ValueError
        >>> hands_lack_of_amout = mahjongpy.MahjongTile.make_hands_set('123', '456', '789', checkamount=False)
        """
        WIND_TILES = {'1':'ton', '2':'nan', '3':'sha', '4':'pei'}
        ZIHAI_TILES = {'1':'haku', '2':'hatu', '3':'tyun'}
        if checkamount:
            if not len(man)+len(sou)+len(pin)+len(wind)+len(zihai) in [13,14]:
                raise ValueError('amount of tile is not 13 or 14')
        tiles = []
        for i in man:
            tiles.append(MahjongTile('manzu',int(i)))
        for i in sou:
            tiles.append(MahjongTile('souzu',int(i)))
        for i in pin:
            tiles.append(MahjongTile('pinzu',int(i)))
        for i in wind:
            tiles.append(MahjongTile(WIND_TILES[i]))
        for i in zihai:
            tiles.append(MahjongTile(ZIHAI_TILES[i]))
        return(tiles)


    def next(self):
        """
        数字が次の牌を返す。字牌の場合は次の種類の牌。ドラ表示牌からドラ牌求めるときのやつ

        Returns
        -------
        tile : MahjongTile
            自身の次の牌
        """
        if self.number is not None:
            new_number = self.number + 1
            if new_number == 10: new_number = 1
            return (MahjongTile(self.tile_type, new_number))
        else:
            return(MahjongTile(self.NEXT_ZIHAI[self.tile_type]))

    def __lt__(self, other):
            TYPE_PRIORITY = {'manzu':1, 'souzu':2, 'pinzu':3, 'ton':4, 'nan':5, 'sha':6, 'pei':7, 'haku':8, 'hatu':9, 'tyun':10}
            if self.tile_type != other.tile_type:
                return(TYPE_PRIORITY[self.tile_type] < TYPE_PRIORITY[other.tile_type])
            else:
                if self.number is None or other.number is None:
                    return True
                else:
                    return(self.number < other.number)

    def __eq__(self, other):
        return(self.tile_type == other.tile_type and self.number == other.number and self.akadora == other.akadora)
