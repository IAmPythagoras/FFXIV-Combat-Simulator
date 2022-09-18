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
        self.ExpectedChakraGate = 5 #This is a random value, so we will keep track of Expected, used value and maximum value
        self.MaxChakraGate = 5 #This is the one used to see if an action is even possible
        self.UsedChakraGate = 0 #Number of used Chakra Gates

        #Timer
        self.LeadenFistTimer = 0
        self.DisciplinedFistTimer = 0
        self.DemolishDOTTimer = 0
        self.BrotherhoodTimer = 0 #Brotherhood effectTimer
        self.RiddleOfFireTimer = 0
        self.RiddleOfWindTimer = 0
        
        #CD
        self.ThunderclapCD = 0
        self.MantraCD = 0
        self.PerfectBalanceCD = 0
        self.BrotherhoodCD = 0
        self.RiddleOfEarthCD = 0
        self.RiddleOfFireCD = 0
        self.RiddleOfWindCD = 0

        #DOT
        self.DemolishDOT = None

        #Stack
        self.ThunderclapStack = 3
        self.PerfectBalanceStack = 2
        self.RiddleOfEarthStack = 3
        self.PerfectBalanceEffectStack = 0

        #Guaranteed Crit
        self.GuaranteedCrit = False #Flag used to know if ability is a guaranteed crit

        self.UsedFormlessStack = False #Will remove effect at the end if set to true
        #JobMod
        self.JobMod = 110

    def updateCD(self, time):
        super().updateCD(time)
        if (self.ThunderclapCD > 0) : self.ThunderclapCD = max(0,self.ThunderclapCD - time)
        if (self.MantraCD > 0) : self.MantraCD = max(0,self.MantraCD - time)
        if (self.PerfectBalanceCD > 0) : self.PerfectBalanceCD = max(0,self.PerfectBalanceCD - time)
        if (self.BrotherhoodCD > 0) : self.BrotherhoodCD = max(0,self.BrotherhoodCD - time)
        if (self.RiddleOfEarthCD > 0) : self.RiddleOfEarthCD = max(0,self.RiddleOfEarthCD - time)
        if (self.RiddleOfFireCD > 0) : self.RiddleOfFireCD = max(0,self.RiddleOfFireCD - time)
        if (self.RiddleOfWindCD > 0) : self.RiddleOfWindCD = max(0,self.RiddleOfWindCD - time)


    def updateTimer(self, time):
        super().updateTimer(time)
        if (self.LeadenFistTimer  > 0) : self.LeadenFistTimer  = max(0,self.LeadenFistTimer - time)
        if (self.DisciplinedFistTimer  > 0) : self.DisciplinedFistTimer  = max(0,self.DisciplinedFistTimer - time)
        if (self.DemolishDOTTimer  > 0) : self.DemolishDOTTimer  = max(0,self.DemolishDOTTimer - time)
        if (self.BrotherhoodTimer  > 0) : self.BrotherhoodTimer  = max(0,self.BrotherhoodTimer - time)
        if (self.RiddleOfFireTimer  > 0) : self.RiddleOfFireTimer  = max(0,self.RiddleOfFireTimer - time)
        if (self.RiddleOfWindTimer  > 0) : self.RiddleOfWindTimer  = max(0,self.RiddleOfWindTimer - time)


    def OpenChakra(self):
        self.MaxChakraGate = min(5, self.MaxChakraGate)

    def addBeastChakra(self, type):
        for i in range(1,4):
            if self.MasterGauge[i] == 0: #Means its empty so we fill it out
                self.MasterGauge[i] = type
                return
        #If get here the whole thing is already filled, so nothing happens

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


