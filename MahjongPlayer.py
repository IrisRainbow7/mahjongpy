class MahjongPlayer:


    def __init__(self, hands=[], discards=[], melds=[], oya=False, points=25000, wind=''):
        if len(hands) not in [13, 14]: raise ValueError('amout of hands is not 13 or 14.')
        self.hands = hands
        self.discards = discards
        self.melds = melds
        self.oya = oya
        self.points = points
        self.wind = wind
        self.hands = sorted(self.hands)

    def shanten():
        return(1)

    def is_riichi():
        return(False)

    def is_tenpai():
        return(True)

    def is_furiten():
        return(False)

    def is_hora():
        return(False)

    def displayed_doras():
        return(1)

    def akadoras():
        return(1)

    def doras():
        return(self.displayed_doras() + self.akadoras())

    def shuntus():
        return(1)

    def ankos():
        return(1)

    def minkos():
        return(1)

    def kotus():
        return(self.ankos() + self.minkos())

    def ankans():
        return(1)

    def minkans():
        return(1)

    def kantus():
        return(self.ankans() + self.minkans())

    def yakus():
        if not is_hora: raise RuntimeError('Not hora')
        return([])

    def score_hu():
        return(30)

    def score_han():
        return(3)

    def is_mangan():
        return(False)

    def is_haneman():
        return(False)

    def is_baiman():
        return(False)

    def is_sanbaiman():
        return(False)

    def is_kazoeyakuman():
        return(False)

    def score():
        if not is_hora: raise RuntimeError('Not hora')
        return(1000)

    def payed_score():
        if not is_hora: raise RuntimeError('Not hora')
        return([1000, 500])
