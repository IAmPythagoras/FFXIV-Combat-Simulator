#########################################
########## MONK PLAYER ###############
#########################################

from Jobs.Melee.Melee_Player import Melee

class Monk(Melee):

    def __init__(self, GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat):
        super().__init__(GCDTimer, ActionSet, PrePullSet, EffectList, CurrentFight, Stat)

        #Gauge
        self.FifthChakra= 0 #5 meditation chakras for forbidden chakra, steel peak, howling fist, and enlightenment

        #Stacks
        self.RiddleOfEarth = 0
        self.LunarNadi = 0
        self.SolarNadi = 0        

        #Forms
        self.OpoOpoForm = False #if in opo-opo and have leaden fist active, use bootshine else dragon kick
        self.RaptorForm = False #if disciplined fist at 7s or more use true strike else twin snakes
        self.CoeurlForm = False #if demonlish has 4s or less use demolish else snap punch

        #Buffs
        self.LeadenFist = False  #guaranteed critical hit in opo-opo form for from dragon kick
        self.DisciplinedFist = False #increases damage dealt by 15% for 15s from twin snakes
        self.ShadowOfTheDestroyer = False #guaranteed critical hit in opo-opo form from shadow of the destroyer
        self.RiddleOfFire = False   #increases damage dealt by 15% for 20s
        self.RiddleOfEarth = False  #reduces auto-attack delay by 50% for 15s
        self.RiddleOfWind = False   #grants 3 stacks, each stack reduced damage taken by 20%
        self.Brotherhood = False    #increases damage dealt by 5% for 15s
        self.MeditativeBrotherhood = False  #20% chance open chakra when party members under this effect land weaponskill or cast spell under this effect
        self.Anatman = False    #extends duration of Disciplined Fist and current form to maximum and halts expiration
        self.PerfectBalance = False #for GCD executed skills to open elixir field, celestial revolution, rising phoenix, phantom rush
 

        #Timer
        self.DemolishTimer = 0   #demolish dot 18s
        self.DisciplinedFistTimer = 0   #twin snakes 15s

        #DOT
        self.Demolish = None
