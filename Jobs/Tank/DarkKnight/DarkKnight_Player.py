#########################################
########## DARK KNIGHT PLAYER ###########
#########################################
from Jobs.Tank.Tank_Player import Tank
from Jobs.Base_Player import ManaRegenCheck
class DarkKnight(Tank):
    #A class for Dark Knight Players containing all effects and cooldowns relevant to the job.

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)
        self.EffectCDList.append(ManaRegenCheck) #mana regen
        #Special
        self.DarksideTimer = 0          #Darkside Gauge, starts at 0 with a max duration of 60s.
        self.Blood = 0                  #Blood Gauge, starts at 0 with a max of 100 units.
        self.EsteemPointer = None

        #Stacks and Ability timers
        self.BloodWeaponStacks = 0
        self.BloodWeaponTimer = 0       #Duration of Blood Weapon buff.
        self.DeliriumStacks = 0         #Stacks of Delirium.
        self.DeliriumTimer = 0          #Duration of Delirium stacks.
        self.SaltedEarthTimer = 0       #Salted Earth duration, required to use Salt and Darkness.
        self.ShadowbringerCharges = 2   #Charges of Shadowbringer
        self.PlungeCharges = 2          #Charges of Plunge
        self.DarkArts = False           #Dark Arts Gauge, activates when TBN breaks.
        self.OblationStack = 2
        #Cooldowns for all abilities, starting at 0 and adjusted by Apply.

        self.BloodWeaponCD = 0          #60s
        self.DeliriumCD = 0             #60s
        self.EdgeShadowCD = 0           #1s     Shares a CD with FloodShadow.
        self.CarveSpitCD = 0            #60s    Shares a CD with AbyssalDrain.
        self.AbyssalDrainCD = 0         #60s    Shares a CD with CarveSpit.
        self.SaltedEarthCD = 0          #90s
        self.SaltDarknessCD = 0         #15s
        self.ShadowbringerCD = 0        #60s charge
        self.LivingShadowCD = 0         #120s
        self.PlungeCD = 0               #30s charge
        self.LivingDeadCD = 0  
        self.DarkMindCD = 0
        self.DarkMissionaryCD = 0
        self.OblationCD = 0
        #DOT
        self.SaltedEarthDOT = None
        #JobMod
        self.JobMod = 105

    def updateCD(self, time):
        super().updateCD(time)
        if (self.BloodWeaponCD > 0) : self.BloodWeaponCD = max(0,self.BloodWeaponCD - time)
        if (self.DeliriumCD > 0) :self.DeliriumCD = max(0,self.DeliriumCD - time)
        if (self.EdgeShadowCD > 0) :self.EdgeShadowCD = max(0,self.EdgeShadowCD - time)
        if (self.CarveSpitCD > 0) :self.CarveSpitCD = max(0,self.CarveSpitCD - time)
        if (self.AbyssalDrainCD > 0) :self.AbyssalDrainCD = max(0,self.AbyssalDrainCD - time)
        if (self.SaltedEarthCD > 0) :self.SaltedEarthCD = max(0,self.SaltedEarthCD - time)
        if (self.SaltDarknessCD > 0) :self.SaltDarknessCD = max(0,self.SaltDarknessCD - time)
        if (self.ShadowbringerCD > 0) :self.ShadowbringerCD = max(0,self.ShadowbringerCD - time)
        if (self.LivingShadowCD > 0) :self.LivingShadowCD = max(0,self.LivingShadowCD - time)
        if (self.PlungeCD > 0) :self.PlungeCD = max(0,self.PlungeCD - time)
        if (self.LivingDeadCD > 0) :self.LivingDeadCD = max(0,self.LivingDeadCD - time)
        if (self.DarkMindCD > 0) :self.DarkMindCD = max(0,self.DarkMindCD - time)
        if (self.DarkMissionaryCD > 0) :self.DarkMissionaryCD = max(0,self.DarkMissionaryCD - time)
        if (self.OblationCD > 0) :self.OblationCD = max(0,self.OblationCD - time)

    def updateTimer(self, time):
        super().updateTimer(time)

        if (self.DarksideTimer > 0) : self.DarksideTimer = max(0,self.DarksideTimer - time)
        if (self.BloodWeaponTimer > 0) : self.BloodWeaponTimer = max(0,self.BloodWeaponTimer - time)
        if (self.DeliriumTimer > 0) : self.DeliriumTimer = max(0,self.DeliriumTimer - time)
        if (self.SaltedEarthTimer > 0) : self.SaltedEarthTimer = max(0, self.SaltedEarthTimer-time)


class Esteem(Tank):
    #A class for Living Shadow pet, summoned by Living Shadow.

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight,Master):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight,Master.Stat)

        self.Blood = 0
        self.Master = Master
        self.JobMod = 100

        self.f_WD = Master.f_WD
        self.f_DET = Master.f_DET
        self.f_TEN = Master.f_TEN
        self.f_SPD = Master.f_SPD
        self.CritRate = Master.CritRate
        self.CritMult = Master.CritMult
        self.DHRate = Master.DHRate

    def updateCD(self, time):
        pass

    def updateTimer(self, time):
        super().updateTimer(time)
        