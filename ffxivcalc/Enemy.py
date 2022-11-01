class Enemy:

    """
    This class is the enemy of the simulation. Contains some global effect that will apply to the entire group and keeps track of the total damage done
    """

    def __init__(self):
        self.EffectList = []
        self.TotalPotency = 0
        self.TotalDamage = 0
        self.buffList = []
        self.ChainStratagem = False # +10% crit rate
        self.WanderingMinuet = False # +2% crit rate
        self.BattleVoice = False # +20% direct hit
        self.ArmyPaeon = False # + 3% direct hit

