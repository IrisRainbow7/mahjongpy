class MahjongTile:

    TILE_TYPES = ['manzu', 'pinzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    TILE_TYPES_ZIHAI = ['ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    NUMBER_READING_JP = {1:'イー', 2:'リャン', 3:'サン', 4:'スー', 5:'ウー', 6:'ロー', 7:'チー', 8:'パー', 9:'キュー', None:''}
    TILE_READING_JP = {'manzu':'ワン', 'pinzu':'ピン', 'souzu':'ソー', 'ton':'トン', 'nan':'ナン', 'sha':'シャー', 'pei':'ペイ', 'haku':'ハク', 'hatu':'ハツ', 'tyun':'チュン'}
    TILE_DISPLAY = {'manzu':'萬', 'pinzu':'●', 'souzu':'Ⅰ', 'ton':'東', 'nan':'南', 'sha':'西', 'pei':'北', 'haku':'白', 'hatu':'發', 'tyun':'中'}
    NEXT_ZIHAI = {'ton':'nan', 'nan':'sha', 'sha':'pei', 'pei':'ton', 'haku':'hatu', 'hatu':'tyun', 'tyun':'haku'}

    def __init__(self, tile_type, number=1, akadora=False):
        if not tile_type in self.TILE_TYPES: raise ValueError('unknown tile types')
        if not number in [i for i in range(1,10)]: raise ValueError('unknown tile types')
        self.tile_type = tile_type
        self.number = number
        if tile_type in self.TILE_TYPES_ZIHAI: self.number = None
        self.akadora = akadora
        self.name_jp = self.NUMBER_READING_JP[self.number] + self.TILE_READING_JP[self.tile_type]
        self.display = str(self.number) + self.TILE_DISPLAY[self.tile_type]
        if self.akadora:
            self.display += '*'
            self.name_jp += '*'
        if self.number is None: self.display = self.TILE_DISPLAY[self.tile_type]

    @classmethod
    def make_tiles_set(cls, use_akadora=True):
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
    def make_hands_set(cls, man='', sou='', pin='', wind='', zihai=''):
        WIND_TILES = {'1':'ton', '2':'nan', '3':'sha', '4':'pei'}
        ZIHAI_TILES = {'1':'haku', '2':'hatu', '3':'tyun'}
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
        return(self.tile_type == other.tile_type and self.number == other.number)
