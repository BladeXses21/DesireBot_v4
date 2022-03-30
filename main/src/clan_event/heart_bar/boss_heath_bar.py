from clan_event.heart_bar.health_bar import HealthBarCreator


class BossHealthBarCreator(HealthBarCreator):
    def __init__(self, full_pool_length: int, pool_length: int):
        super().__init__(full_pool_length, pool_length)
        self.middle_full = '<:bossHeartMiddle:958466183684817007>'
        self.end_full = '<:bossHeartEnd:958470219129565225>'
        self.start_full = '<:bossHeartStart:958470228755513484>'
