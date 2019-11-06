class MahjongTile:

    TILE_TYPES = ['manzu', 'pinzu', 'souzu', 'ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    TILE_TYPES_ZIHAI = ['ton', 'nan', 'sha', 'pei', 'haku', 'hatu', 'tyun']
    NUMBER_READING_JP = {1:'イー', 2:'リャン', 3:'サン', 4:'スー', 5:'ウー', 6:'ロー', 7:'チー', 8:'パー', 9:'キュー'}
    TILE_READING_JP = {'manzu':'ワン', 'pinzu':'ピン', 'souzu':'ソー', 'ton':'トン', 'nan':'ナン', 'sha':'シャー', 'pei':'ペイ', 'haku':'ハク', 'hatu':'ハツ', 'tyun':'チュン'}
    TILE_DISPLAY = {'manzu':'萬', 'pinzu':'●', 'souzu':'Ⅰ', 'ton':'東', 'nan':'南', 'sha':'西', 'pei':'北', 'haku':'白', 'hatu':'發', 'tyun':'中'}
    def __init__(self, tile_type, number, aka_dora=False):
        if not tile_type in self.TILE_TYPES: raise ValueError('unknown tile types')
        if not number in [i for i in range(1,10)]: raise ValueError('unknown tile types')
        self.tile_type = tile_type
        self.number = number
        if tile_type in self.TILE_TYPES_ZIHAI: self.number = None
        self.aka_dora = aka_dora
        self.name_jp = self.NUMBER_READING_JP[number] + self.TILE_READING_JP[tile_type]
        self.display = str(number) + self.TILE_DISPLAY[tile_type]
