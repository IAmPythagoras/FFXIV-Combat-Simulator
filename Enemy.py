class Enemy:

    def __init__(self):
        self.EffectList = []
        self.TotalPotency = 0
        self.TotalDamage = 0
        self.buffList = []
        self.ChainStratagem = False
        self.WanderingMinuet = False # +2% crit chance
        self.BattleVoice = False # +20% direct hit
        self.ArmyPaeon = False # + 3% direct hit

