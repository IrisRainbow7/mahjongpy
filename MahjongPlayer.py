class MahjongPlayer:


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
        return(False)

    def is_hora(self):
        return(False)

    def displayed_doras(self, dora):
        return(1)

    def akadoras(self):
        return(1)

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
