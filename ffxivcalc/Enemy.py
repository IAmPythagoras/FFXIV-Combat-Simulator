
from copy import deepcopy
from ffxivcalc.helperCode.helper_math import roundDown

# Exception
from ffxivcalc.helperCode.exceptions import InvalidTankBusterTargetNumber

class EnemyEvent:
    """
    This class represents an action or event the boss can take. Such events can be raidwide, a mechanic, untargetable, an enrage, etc.
    """

    def __init__(self, id, CastTime : float, Damage : int, RaidWide=True, nTBTarget=0, IsPhysical = False, Experimental = False) -> None:
        """Constructor the of the EnemyEvent class

        Args:
            id (int): id of the event.
            CastTime (float): casting time of the event.
            Damage (int): Damage the players receive when the action is used.
            RaidWide (bool) : True if the Event is a raidwide. Default value is true
            nTBTarget (int) : Number of targets of a tank buster. Only needed if RaidWide is false. Must be 1 or 2 if Experimental is false
            IsPhysical (bool) : True if the damage of that event is physical. By default false (hence magical by default)
            Experimental (bool) : False if we do not wish to overrule the automatic checking for a valid action.
        """

        if not Experimental and not RaidWide and (nTBTarget != 1 and nTBTarget != 2) or nTBTarget < 0 :
            # If a tankbuster but invalid number of targets and not experimental
            raise InvalidTankBusterTargetNumber(nTBTarget, id)

        self.CastTime = CastTime
        self.id = id
        self.Damage = Damage
        self.RaidWide = RaidWide
        self.nTBTarget = nTBTarget
        self.IsPhysical = IsPhysical
        self.target = [] # Empty list. The targets will be computed in begin_cast()



    def begin_cast(self, Enemy) -> None:
        """
        This function will begin the casting of an action by the enemy.

        Enemy (Enemy) : Enemy object casting the Event

        """

        Enemy.CastingTimer = self.CastTime
        Enemy.CastingAction = deepcopy(self)
        Enemy.IsCasting = True

    def cast(self, Enemy, RaidWide=True) -> None:
        """This function will cast and apply damage/effect on all the players

        Args:
            Enemy (Enemy): Enemy casting the action
        """

        # Finds targets

        self.target = Enemy.CurrentFight.PlayerList if self.RaidWide else Enemy.CurrentFight.GetEnemityList(self.nTBTarget)
        # If the event is a raidwide the target is all players.
        # If it is not it targets the players with the most enemity up to the number of targets
        # Will do damage on all target

        # Computes new damage because mitigation on the Enemy
        # Does not differentiate between magical and physical for now
        curr_mit = 1
        if Enemy.Addle > 0: 
            if self.IsPhysical : curr_mit = round(0.95 * curr_mit, 2) # 5% physical mit
            else : curr_mit = round(0.9 * curr_mit, 2) # 10% magic mit
        if Enemy.Feint  > 0: 
            if self.IsPhysical : curr_mit = round(0.9 * curr_mit, 2) # 10% physical mit
            else : curr_mit = round(0.95 * curr_mit, 2) # 5% magic mit
        if Enemy.Reprisal  > 0: curr_mit = round(0.9 * curr_mit, 2) # Flat 10% mit

        self.Damage *= curr_mit # Updating the new damage based on global mit



        for player in self.target:
            # Going through all players
            # Mit according to their own personnal mit
            if self.IsPhysical : player_damage = self.Damage * player.PhysicalMitigation # Only applies physical mit
            else : player_damage = self.Damage * player.MagicMitigation # Only applies magic mit
            player_damage = round(player_damage, 0) # Rounding down to lowest integer
            player.TakeDamage(player_damage, not self.IsPhysical) # Applying the damage to the player

        Enemy.EventNumber += 1 # Incrementing the pointer to the next event

        if Enemy.EventNumber == len(Enemy.EventList):
            # If the enemy has reached the end of its action list
            Enemy.hasEventList = False



class EnemyDOT(EnemyEvent):
    """
    This class is any DOT applied by the enemy on the players. It will do damage over time on the players.
    """

    def __init__(self, id, DOTDamage : int, DOTDuration):
        """
        Creates a DOTDamage object.

        DOTDamage (int) : Damage every application of the DOT
        DOTDuration (float) : Duration of the DOT.
        """
        self.id = id
        self.DOTDamage = DOTDamage
        self.DOTDuration = DOTDuration

        self.DOTStateTimer = 3 # The DOT will be applied every 3 seconds

    def updateState(self, time : float, player):
        """
        Update the states of the DOT. Applies damag if neeeded.

        time (float) : time by which the DOT is updated.
        player (Player) : player object on which the DOT is applied.

        """
        # Updating timers
        self.DOTStateTimer -= time
        self.DOTDuration -= time

        if self.DOTStateTimer <= 0: # Apply damage
            player.TakeDamage(self.DOTDamage)
            self.DOTStateTimer = 3

        if self.DOTDuration <= 0:
            # DOT is finished
            player.EnemyDOT.remove(self)


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

        # Mitigation buff
        self.Addle = False # 10% magical, 5% physical
        self.Feint = False # 10% physical, 5% magical
        self.Reprisal = False # 10% true mitigation
        

        self.EventList = [] # List of all EnemyEvent object this boss will perform through the simulation
        self.EventNumber = 0 # Current index of the EvenList action.
        self.hasEventList = False # By default an enemy has nothing to do
        # Timer
        self.CastingTimer = 0
        self.AddleTimer = 0
        self.FeintTimer = 0
        self.ReprisalTimer = 0

        # Currently Casting Action
        self.CastingAction = None
        self.IsCasting = False # If the Enemy is casting

        # Fight the Enemy is in
        self.CurrentFight = None

    def setEventList(self, newEventList) -> None:
        """
        This function gives the Enemy an event list. This will result in a crash
        if the list is empty.

        Args:
            newEventList (List[EnemyEvent]): List of the Events to perform
        """

        self.hasEventList = True # Let the Fight know this Enemy has an EventList

        self.EventList = deepcopy(newEventList)


    def UpdateTimer(self, time : float) -> None:
        """This function updates the Timer values of the Enemy object

        Args:
            time (float): value by which we update the timer
        """

        if self.AddleTimer > 0 : 
            self.AddleTimer = max(0, self.AddleTimer - time)
            if self.AddleTimer == 0 : self.Addle = False
        if self.FeintTimer > 0 : 
            self.FeintTimer = max(0, self.FeintTimer - time)
            if self.FeintTimer == 0 : self.Feint = False
        if self.ReprisalTimer > 0 : 
            self.ReprisalTimer = max(0, self.ReprisalTimer - time)
            if self.ReprisalTimer == 0 : self.Reprisal = False

        if self.IsCasting : # Only decrements if the enemy is currently casting
            self.CastingTimer = max(0, self.CastingTimer - time)

            if self.CastingTimer <= 0 : # If reaches the end of the cast
                self.CastingAction.cast(self) # Cast the action
                self.IsCasting = False


def WaitEvent(time : float) -> EnemyEvent:
    """
    This function returns a EnemyEvent object which has no effect or damage and simply makes the Enemy way.

    time (float) : time in seconds we want the enemy to wait
    """

    return EnemyEvent(-212,time, 0)

MagicRaidWide = EnemyEvent(1, 2, 400)
PhysicalRaidWide = EnemyEvent(3, 2, 500, IsPhysical=True)
TankBuster = EnemyEvent(2, 2, 1000, RaidWide=False, nTBTarget=1)



