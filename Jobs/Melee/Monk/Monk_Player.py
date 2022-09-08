#########################################
##########  MONK PLAYER   ###############
#########################################

from Jobs.Melee.Melee_Player import Melee

class Monk(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.CurrentForm = 0 #0 -> Nothing, 1 -> Opo-opo, 2 -> Raptor, 3 -> Coeurl, 4 -> Formless
        #After each execution of a relevant GCD, the form will be changed here.
        # Does action -> Changes form by Apply and adds FormChangeCheck -> Checks if any combo effect -> Effect removes itself
        # FormChangeCheck -> Changes form according to self.CurrentForm -> FormChangeCheck removes itself
        self.MasterGauge = [False,0,0,0,False]
        # This array will represent the master gauge
        # [Lunar Nadi, Chakra1, Chakra2, Chakra3, Solar Nadi]
        # For nadis, False -> closed, True -> open.
        # For chakras , 0 -> Empty, 1 -> Opo-opo, 2-> Raptor, 3-> Coeurl
        self.FormlessFistStack = 0 #Number of formless actions the player can do
        self.ExpectedChakraGate = 0 #This is a random value, so we will keep track of Expected, used value and maximum value
        self.MaxChakraGate = 0 #This is the one used to see if an action is even possible
        self.UsedChakraGate = 0 #Number of used Chakra Gates

        #Timer
        self.LeadenFistTimer = 0
        self.DisciplinedFistTimer = 0
        self.DemolishDOTTimer = 0
        self.BrotherhoodTimer = 0 #Brotherhood effectTimer
        
        #CD
        self.ThunderclapCD = 0
        self.MantraCD = 0
        self.PerfectBalanceCD = 0
        self.BrotherhoodCD = 0

        #DOT
        self.DemolishDOT = None

        #Stack
        self.ThunderclapStack = 3
        self.PerfectBalanceStack = 2

        #Guaranteed Crit
        self.GuaranteedCrit = False #Flag used to know if ability is a guaranteed crit


        #JobMod
        self.JobMod = 110

    def updateCD(self, time):
        if (self.PerfectBalanceCD > 0) : self.PerfectBalanceCD = max(0,self.PerfectBalanceCD - time)
        if (self.RiddleOfFireCD > 0) : self.RiddleOfFireCD = max(0,self.RiddleOfFireCD - time)
        if (self.RiddleOfWindCD > 0) : self.RiddleOfWindCD = max(0,self.RiddleOfWindCD - time)
        if (self.RiddleOfEarthCD > 0) : self.RiddleOfEarthCD = max(0,self.RiddleOfEarthCD - time)
        if (self.BrotherhoodCD > 0) : self.BrotherhoodCD  = max(0,self.BrotherhoodCD  - time)
        if (self.ThunderclapCD > 0) : self.ThunderclapCD = max(0,self.ThunderclapCD - time)
        if (self.MantraCD > 0) : self.MantraCD = max(0,self.MantraCD - time)
        if (self.AnatmanCD > 0) : self.AnatmanCD  = max(0,self.AnatmanCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.DemolishDOTTimer  > 0) : self.DemolishDOTTimer  = max(0,self.DemolishDOTTimer - time)
        if (self.DisciplinedFistTimer > 0) : self.DisciplinedFistTimer = max(0,self.DisciplinedFistTimer - time)
        if (self.LeadenFistTimer > 0) : self.LeadenFistTimer = max(0,self.LeadenFistTimer - time)
        if (self.RiddleOfWindTimer > 0) : self.RiddleOfWindTimer = max(0,self.RiddleOfWindTimer - time)
        if (self.RiddleOfFireTimer > 0) : self.RiddleOfFireTimer = max(0,self.RiddleOfFireTimer - time)
        if (self.BrotherhoodTimer > 0) : self.BrotherhoodTimer = max(0,self.BrotherhoodTimer - time)
        if (self.PerfectBalanceTimer > 0) : self.PerfectBalanceTimer = max(0,self.PerfectBalanceTimer - time)
        if (self.ThunderclapTimer > 0) : self.ThunderclapTimer = max(0,self.ThunderclapTimer - time)
        if (self.MantraTimer > 0) : self.MantraTimer = max(0,self.MantraTimer - time)
        if (self.AnatmanTimer > 0) : self.AnatmanTimer = max(0,self.AnatmanTimer - time)

    def OpenChakra(self):
        self.MaxChakraGate = min(5, self.MaxChakraGate)

    def BeastChakraType(self):
        #Returns number of BeastChakra
        OpoOpo = False
        Raptor = False
        Coeurl = False

        number_chakra = 0

        for i in self.MasterGauge[1:4]:
            if not OpoOpo and i == 1: 
                OpoOpo = True
                number_chakra += 1
            elif not Raptor and i == 2:
                Raptor = True
                number_chakra += 1
            elif not Coeurl and i == 3: 
                Coeurl = True
                number_chakra += 1

        return number_chakra

    def ResetMasterGauge(self):
        self.MasterGauge[1:4] = [0,0,0] #Reset Chakra

        


"""
        #Gauge
        self.FifthChakra = 0 #5 meditation chakras for forbidden chakra, steel peak, howling fist, and enlightenment
        self.OpoOpoSkillUsed = 0 
        self.RaptorSkillUsed = 0 
        self.CoeurlSkillUsed = 0       
        # self.ElixirField = False   #masterful blitz
        # self.CelestialRevolution = False   #masterful blitz
        # self.RisingPhoenix = False #masterful blitz
        # self.PhantomRush = False   #masterful blitz

        #Stacks
        self.RiddleOfEarth = 0  #three stacks
        self.LunarNadi = 0
        self.SolarNadi = 0
        self.Thunderclap = 0 #three charges
        self.PerfectBalance = 0 #three stacks       

        #Forms
        self.OpoOpoForm = False #if in opo-opo and have leaden fist active, use bootshine else dragon kick
        self.RaptorForm = False #if disciplined fist at 7s or more use true strike else twin snakes
        self.CoeurlForm = False #if demonlish has 4s or less use demolish else snap punch
        self.FormShift = False
        self.FormlessFist = False   #allows execution of weaponskills that requires certain form without being in that form
        self.Bootshine = False  #grants raptor form
        self.TrueStrike = False #grants coeurl, only can be executed in raptor
        self.SnapPunch = False  #grants opo-opo form, only can be executed in coeurl
        self.TwinSnakes = False #grants coeurl form, can only be executed in raptor
        self.ArmOfTheDestroyer = False  #changes form to raptor
        self.Demolish = False   #changes form to opo-opo, can only be executed in coeurl
        self.Rockbreaker = False    #changes form to opo-opo, can only be executed in coeurl
        self.FourPointFury = False  #changes form to coeurl, can only be executed in raptor
        self.DragonKick = False #changes form to raptor

        #Buffs
        self.LeadenFist = False  #guaranteed critical hit in opo-opo form for from dragon kick
        self.DisciplinedFist = False #increases damage dealt by 15% for 15s from twin snakes
        self.ShadowOfTheDestroyer = False #guaranteed critical hit in opo-opo form from shadow of the destroyer
        self.RiddleOfFire = False   #increases damage dealt by 15% for 20s
        self.RiddleOfEarth = False  #grants 3 stacks, each stack reduced damage taken by 20%
        self.RiddleOfWind = False   #reduces auto-attack delay by 50% for 15s
        self.Brotherhood = False    #increases damage dealt by 5% for 15s
        self.MeditativeBrotherhood = False  #20% chance open chakra when party members under this effect land weaponskill or cast spell under this effect
        self.Anatman = False    #extends duration of Disciplined Fist and current form to maximum and halts expiration
        self.PerfectBalance = False #for GCD executed skills to open elixir field, celestial revolution, rising phoenix, phantom rush

        #Next Crit
        self.NextCrit = False #leadenfist
 
        #Timer
        self.DemolishDOTTimer = 0   #demolish dot 18s
        self.DisciplinedFistTimer = 0   #twin snakes 15s
        self.LeadenFistTimer = 0 #dragon kick grants guaranteed next crit 30s
        self.RiddleOfWindTimer = 0
        self.RiddleOfFireTimer = 0
        self.BrotherhoodTimer = 0
        self.PerfectBalanceTimer = 0
        self.ThunderclapTimer = 0
        self.MantraTimer = 0
        self.AnatmanTimer = 0

        #DOT
        self.DemolishDOT = None

        #CD
        self.PerfectBalanceCD = 0
        self.RiddleOfFireCD = 0
        self.RiddleOfWindCD = 0
        self.RiddleOfEarthCD = 0
        self.BrotherhoodCD = 0
        self.ThunderclapCD = 0
        self.MantraCD = 0
        self.AnatmanCD = 0

+++++

def ForbiddenChakraRequirement(Player, Spell):
    return Player.FifthChakra == -1

def ElixerFieldRequirement(Player, Spell):  #must use three of the same form skills and grants lunar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 3 or Player.RaptorSkillUsed == 3 or Player.CoeurlSkillUsed == 3

def RisingPhoenixRequirement(Player, Spell):    #must use three different form skills is aoe and unlocks solar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 1 and Player.RaptorSkillUsed == 1 and Player.CoeurlSkillUsed == 1

def CelestialRevolutionRequirement(Player, Spell):    #must use 2 gcds if same form and last is different form skills is aoe and unlocks solar nadi
    return Player.PerfectBalance == 0 and Player.OpoOpoSkillUsed == 2 and Player.RaptorSkillUsed == 1 \
                                        or Player.OpoOpoSkillUsed == 2 and Player.CoeurlSkillUsed == 1 \
                                            or Player.RaptorSkillUsed == 2 and Player.OpoOpoSkillUsed == 1 \
                                                or Player.RaptorSkillUsed == 2 and Player.CoeurlSkillUsed == 1 \
                                                    or Player.CoeurlSkillUsed == 2 and Player.RaptorSkillUsed == 1 \
                                                        or Player.CoeurlSkillUsed == 2 and Player.OpoOpoSkillUsed == 1

def PhantomRushRequirement(Player, Spell):    #must use three different form skills is aoe and unlocks solar nadi
    return Player.SolarNadi == -1 and Player.LunarNadi == -1
                                    
def CoeurlFormRequirement(Player, Spell):
    return Player.PerfectBalance > 0 or Player.TrueStrike or Player.TwinSnakes or Player.FourPointFury

def RaptorFormRequirement(Player, Spell):
    return Player.PerfectBalance > 0 or Player.Bootshine or Player.ArmOfTheDestroyer or Player.DragonKick or Player.ShadowOfTheDestroyer



"""