class HealthBarCreator:
    def __init__(self, full_pool_length: int, pool_length: int):
        self.fullPoolLength = full_pool_length
        self.poolLength = pool_length
        self.start_full = '<:heartStart:958440903729639434>'
        self.start_empty = '<:heartStartEmpty:958446558041473074>'
        self.middle_full = '<:heartMiddle:958445631406493751>'
        self.middle_empty = '<:heartMiddleEmpty:958446546473615381>'
        self.end_full = '<:heartEnd:958442103447384144>'
        self.end_empty = '<:heartEndEmpty:958749811316768828>'

    def __str__(self):
        health = ''
        if self.fullPoolLength <= 0:
            health = health + self.start_empty
        else:
            health = health + self.start_full

        health = health + ((self.fullPoolLength - 1) * self.middle_full)
        health = health + ((self.poolLength - self.fullPoolLength) * self.middle_empty)

        if self.fullPoolLength >= self.poolLength:
            health = health + self.end_full
        else:
            health = health + self.end_empty

        return health


