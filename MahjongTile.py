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
            tiles.pop(13)
            tiles.pop(14)
            tiles.append(MahjongTile('manzu',5,akadora=True))
            tiles.append(MahjongTile('souzu',5,akadora=True))
            tiles.append(MahjongTile('pinzu',5,akadora=True))
        return(tiles)

    def next(self):
        if self.number is not None:
            new_number = self.number + 1
            if new_number == 10: new_number = 1
            return (MahjongTile(self.tile_type, new_number))
        else:
            return(MahjongTile(self.NEXT_ZIHAI[self.tile_type]))


