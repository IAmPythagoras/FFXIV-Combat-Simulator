"""Defines and documents all custom columns in the data."""

# Not custom, but used a lot so recorded
ABILITY_ID = "abilityGameID"
TYPE = "type"
CAST = "cast"
DAMAGE = "damage"
APPLY_BUFF = "applybuff"
APPLY_DEBUFF = "applydebuff"
REFRESH_BUFF = "refreshbuff"
REMOVE_BUFF = "removebuff"
REMOVE_DEBUFF = "removedebuff"
PREPARE = "calculateddamage"
PLAYER = "Player"
PET = "Pet"

# Human readable name for abilities
ABILITY_NAME = "ability_name"


# Human readable source name for actors
SOURCE_NAME = "source_name"
SOURCE_TYPE = "source_type"
SOURCE_SUBTYPE = "source_subtype"
SOURCE_PET_ACTOR = "source_pet_actor"
SOURCE_ID = "sourceID"

# Human readable target name for actors
TARGET_NAME = "target_name"
TARGET_TYPE = "target_type"
TARGET_SUBTYPE = "target_subtype"
TARGET_PET_ACTOR = "target_pet_actor"
TARGET_ID = "targetID"

# Fight time, based on lb update tick to reset gauge
FIGHT_TIME = "fight_time"
SNAPSHOT = "snapshot"

# Bonus percent, estimate the value of combos
# 1 - basePotency/bonusPotency = bonusPercent
BONUS_PERCENT = "bonusPercent"

# Log hittype (crit, normal, etc)
LOG_HIT_TYPE = "hitType"
LOG_DHIT = "directHit"

# Special name added in for an assumed prepull apply
ESTIMATED_APPLY_BUFF = "estimatedapplybuff"

# Special name for "correct" card, other buffs
CARD_MATCHES_JOB = "card_matches_job"
RADIANT_CODA = "radiant_codas"

# Potency data and ability details
POTENCY = "ability_potency"
ABILITY_DAMAGE_TYPE = "ability_damage_type"  # See types below
DIRECT_DAMAGE = "direct_damage"
DOT = "dot"
AUTO = "auto"
GUARANTEED_CRIT = "guaranteed_crit"
GUARANTEED_DHIT = "guaranteed_dhit"
POSITIONAL = "positional"
SPECIAL_FORMULA = "special_formula"
GROUND_BASED = "ground_based"
ABILITY_TYPE = "ability_type"
GCD = "GCD"
OGCD = "OGCD"
LOCK_05 = "0.5 Lock"
LOCK_10 = "1.0 Lock"
LOCK_15 = "1.5 Lock"


# GCD and Weave tracking info
WEAVE = "weave"
GCD_ROLL = "gcd_roll"
NUM_WEAVES = "num_weaves"

# Buff related stuff
LOG_MULTIPLIER = "multiplier"
DAMAGE_MULTIPLIER = "damage_multiplier"
CRIT_BONUS = "crit_bonus"
DHIT_BONUS = "dhit_bonus"
MAIN_STAT_BONUS = "main_stat_bonus"
DOT_APPLICATION = "dot_application"
CAST_TIME = "cast_time"  # Defines the buff snapshot
LIMITED = "limited"  # a limited buff to specific types.
# Defines buff multipliers in a serial format as string
ACTIVE_BUFF_MULTIPLIERS = "active_buff_multipliers"
COMPLETE_DAMAGE_MULTIPLIER = "complete_damage_multiplier"
AVERAGED_MULTIPLIER = "averaged_multiplier"
CRIT_CHANCE = "crit_rate"
CRIT_MULT = "crit_multiplier"
CRIT_MOD = "crit_mod"
DHIT_CHANCE = "dhit_rate"
DHIT_MOD = "dhit_mod"
PERSONAL_DAMAGE_MULTIPLIER = "personal_damage_multiplier"  # This is all self buffs, reduce to get raw damage
RAW_DAMAGE_VARIANCE = "raw_damage_variance"  # variance without personal buffs
DAMAGE_VARIANCE = "damage_variance"  # variance with personal buffs

# Event types
HIT_TYPE = "hit_type"
CRIT = "crit"
DHIT = "direct_hit"
DCRIT = "direct_crit"
BASE = "base_hit"
AVERAGED = "averaged"
TICK = "tick"  # Helpful for determining tracking simulated dots
SIMULATED_DOT = "simulated_dot"

# Simmed Data
EXPECTED_DAMAGE = "expected_damage"
RAW_DAMAGE = "raw_damage"
BASE_DAMAGE = "base_damage"
AMOUNT = "amount"
LOG_DAMAGE = "unmitigatedAmount"  # amount column is affected by overkill
LOG_DOT_SIMULATED_DAMAGE = "finalizedAmount"  # Simmed dot damage
LATENT_VALUE = "latent_value"

# Damage taken types
DAMAGE_TYPE = "damage_type"
PHYSICAL = "physical"
MAGICAL = "magical"
DARKNESS = "darkness"
UNKNOWN = "unknown"

# Mitigation mods
PHYSICAL_MITIGATION = "Physical Mitigation"
MAGICAL_MITIGATION = "Magical Mitigation"
ADJUSTED_LOG_DAMAGE = (
    "unmitigatedBossAmount"  # amount column is affected by overkill
)

# Mappings (target_subtype)
JOB = "Job"

TARGET_SUBTYPE_TO_JOB_MELEE = {
    "DarkKnight": "DRK",
    "Gunbreaker": "GNB",
    "Paladin": "PLD",
    "Warrior": "WAR",
    "Ninja": "NIN",
    "Samurai": "SAM",
    "Reaper": "RPR",
    "Monk": "MNK",
    "Dragoon": "DRG",
}

TARGET_SUBTYPE_TO_JOB = {
    **TARGET_SUBTYPE_TO_JOB_MELEE,
    "Dancer": "DNC",
    "Bard": "BRD",
    "Machinist": "MCH",
    "RedMage": "RDM",
    "BlackMage": "BLM",
    "Summoner": "SMN",
    "Astrologian": "AST",
    "Scholar": "SCH",
    "Sage": "SGE",
    "WhiteMage": "WHM",
}

# ('type')
TYPE_TO_DAMAGE_TYPE = {
    "1": PHYSICAL,
    "32": DARKNESS,
    "64": MAGICAL,
    "128": PHYSICAL,
    "1024": MAGICAL,
}