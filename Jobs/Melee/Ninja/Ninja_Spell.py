from Jobs.Base_Spell import empty
from Jobs.Melee.Melee_Spell import NinjaSpell
from Jobs.Melee.Ninja.Ninja_Spell import ArmorCrush
Lock = 0.75

#Apply
def ApplySpinningEdge(Player, Enemy):
    Player.AddNinki(5)
    
    if not (SpinningEdgeCombo in Player.EffectList): Player.EffectList.append(SpinningEdgeCombo)


#Effect

def SpinningEdgeCombo(Player, Spell):
    if Spell.id == GustSlash.id:
        Spell.Potency += 160
        Player.AddNinki(5)
        Player.EffectToRemove.append(SpinningEdgeCombo)
        Player.EffectList.append(GustSlashCombo)

def GustSlashCombo(Player, Spell):
    if Spell.id == AeolianEdge.id:
        Spell.Potency += 240
        Player.AddNinki(15)
        Player.EffectToRemove.append(GustSlashCombo)
    elif Spell.id == ArmorCrush.id:
        Spell.Potency += 220
        Player.AddNinki(15)
        Player.AddHuton(30)
        Player.EffectToRemove.append(GustSlashCombo)



#GCD
SpinningEdge = NinjaSpell(1, True, Lock, 2.5, 220, ApplySpinningEdge, [], True )
GustSlash = NinjaSpell(2, True, Lock, 2.5, 160, empty, [], True)
AeolianEdge = NinjaSpell(3, True, Lock, 2.5, 200, empty, [], True)
ArmorCrush = NinjaSpell(4, True, Lock, 2.5, 200, empty, [], True)


#oGCD
DreamWithinADream = NinjaSpell(5, False, Lock, 0, 3*150, ApplyDreamWithinADream, [DreamWithinADreamRequirement], False)