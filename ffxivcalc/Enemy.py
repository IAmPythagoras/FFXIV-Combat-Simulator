
from copy import deepcopy

class EnemyEvent:
    """
    This class represents an action or event the boss can take. Such events can be raidwide, a mechanic, untargetable, an enrage, etc.
    """

    def __init__(self, id, CastTime, Damage):
        """Constructor the of the EnemyEvent class

        Args:
            id (int): id of the event.
            CastTime (float): casting time of the event.
            Damage (int): Damage the players receive when the action is used.
        """

        self.CastTime = CastTime
        self.id = id
        self.Damage = Damage

    def begin_cast(self, Enemy):
        """
        This function will begin the casting of an action by the enemy.

        Enemy (Enemy) : Enemy object casting the Event

        """

        Enemy.CastingTimer = self.CastTime
        Enemy.CastingAction = deepcopy(self)

    def cast(self, Enemy):
        """This function will cast and apply damage/effect on all the players

        Args:
            Enemy (Enemy): Enemy casting the action
        """

        # Will do damage on all players

        for player in Enemy.CurrentFight.PlayerList:
            # Going through all players

            player.TakeDamage(self.Damage) # Applying the damage to the player

        Enemy.EventNumber += 1 # Incrementing the pointer to the next event

        if Enemy.EventNumber == len(Enemy.EventList):
            # If the enemy has reached the end of its action list
            Enemy.hasEventList = False


    



class Enemy:

    """
    This class is the enemy of the simulation. Contains some global effect that will apply to the entire group and keeps track of the total damage done
    """

    def __init__(self):


        self.EffectList = [] # List of all effect on the boss. These are effects applied by the players

        self.TotalPotency = 0
        self.TotalDamage = 0

        self.buffList = [] # List of all buffs the boss gives when a player attacks them

        # Buff that can be applied directly on the boss
        self.ChainStratagem = False # +10% crit rate
        self.WanderingMinuet = False # +2% crit rate
        self.BattleVoice = False # +20% direct hit
        self.ArmyPaeon = False # + 3% direct hit

        self.EventList = [] # List of all EnemyEvent object this boss will perform through the simulation
        self.EventNumber = 0 # Current index of the EvenList action.
        self.hasEventList = False # By default an enemy has nothing to do
        # Timer
        self.CastingTimer = 0

        # Currently Casting Action
        self.CastingAction = None
        self.IsCasting = False # If the Enemy is casting

        # Fight the Enemy is in
        self.CurrentFight = None

    def setEventList(self, newEventList, Fight):
        """
        This function gives the Enemy an event list. This will result in a crash
        if the list is empty.

        Args:
            newEventList (List[EnemyEvent]): List of the Events to perform
            Fight (Fight) : Fight object in which the Enemy will perform this eventList
        """

        self.hasEventList = True # Let the Fight know this Enemy has an EventList

        self.EventList = deepcopy(newEventList)
        self.CurrentFight = Fight


    def UpdateTimer(self, time):
        """This function updates the Timer values of the Enemy object

        Args:
            time (float): value by which we update the timer
        """
        if self.IsCasting : # Only decrements if the enemy is currently casting
            self.CastingTimer = max(0, self.CastingTimer - time)

            if self.CastingTimer <= 0 : # If reaches the end of the cast
                self.CastingAction.cast(self) # Cast the action
                self.IsCasting = False





