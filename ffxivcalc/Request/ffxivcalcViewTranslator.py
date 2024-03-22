"""
This code was written by Apollo (apollo.van.waddleburg on discord) and adapted to fit the needs of the sim.
"""

"""Defines views that integrate with ffxivcalc.

{
    "data": {
        "fightInfo": {
            "RequirementOn": true,
            "IgnoreMana": false,
            "fightDuration": "500"
        },
        "PlayerList": [
            {
                "JobName": "Samurai",
                "PlayerName": "SussyPlayer",
                "playerID": "0",
                "weaponDelay": "2.64",
                "stat": {
                    "MainStat": "3367",
                    "WD": "132",
                    "Det": "1736",
                    "Ten": "400",
                    "SS": "400",
                    "SkS": "400",
                    "Crit": "2587",
                    "DH": "1602"
                },
                "actionList": [
                ],
                "etro_gearset_url": "",
                "Auras": []
            }
        ]
    },
    "mode": false,
    "TeamCompBonus": true,
    "MaxPotencyPlentifulHarvest": false,
    "nRandomIterations": 0
}
"""
import functools
import logging
import os.path
from typing import Iterator, Dict, Union, Set, List

import pandas as pd
#import yaml
from ffxivcalc.Jobs import ActionEnum

from ffxivcalc.Request.etro_request import get_gearset_data
from ffxivcalc.GearSolver.Solver import getBaseStat
from ffxivcalc.Request import custom_columns
from ffxivcalc.Request import prepull

LOG = logging.getLogger(__name__)

_KEEP_TARGET_ACTION = [
    "Oblation",
    "TheBlackestNight",
    "HeartOfCorundum",
    "Bole",
    "Arrow",
    "Ewer",
    "Spear",
    "Spire",
    "Balance"
]

def ffxiv_sim_view(event_data: pd.DataFrame, max_time : float = 0) -> Iterator:
    casts_by_players_view = event_data[
        (event_data["type"] == "cast")
        & (event_data[custom_columns.SOURCE_TYPE] == "Player")
        | (event_data.index == event_data['abilityGameID'].dropna().index[0])
        | ((event_data.index == event_data[event_data['type'] == 'applybuff'].index[0]) & (event_data['fight_time'] != event_data[event_data['type'] == 'cast'].iloc[0]['fight_time']) & (event_data['fight_time'] < 0) )
    ]

    if max_time > 0:
        casts_by_players_view = casts_by_players_view[
            event_data["fight_time"] <= max_time
        ]
    
    # If first damage event then cast is not present and only calculated damage is.
    # The first 'applybuff' event is also not casted. So we add the first.

    casts_by_players_view = casts_by_players_view.astype(
        {
            custom_columns.SOURCE_ID: int,
            custom_columns.TARGET_ID: int,
            custom_columns.ABILITY_ID: int,
        }
    )
    fight_duration = (
        casts_by_players_view[custom_columns.FIGHT_TIME].max() + 10.0
    )
    player_ids = set(casts_by_players_view[custom_columns.SOURCE_ID].unique())
    player_list = []
    prepull_auras = prepull.prepull_aura_frame(fight_events=event_data)
    # prepull_estimated_casts = prepull.infer_prepull_buff_casts(fight_events=event_data)
    for (
        player_name,
        player_id,
        job_name,
    ), group in casts_by_players_view.groupby(
        by=[
            custom_columns.SOURCE_NAME,
            custom_columns.SOURCE_ID,
            custom_columns.SOURCE_SUBTYPE,
        ]
    ):
        actions = build_action_set(
            player_events=group,
            job_name=job_name,
            player_ids=player_ids,
        )

        # Removing target : 0
        for event in actions:
            if not (event['actionName'] in _KEEP_TARGET_ACTION) and (event['targetID'] == 0 or event['targetID'] == player_id):
                del event['targetID']

        # TODO: prepull_casts
        auras = build_aura_list(
            player_auras=prepull_auras[
                prepull_auras[custom_columns.SOURCE_NAME] == player_name
            ]
        )
        #etro_gearset_url = "url"#get_default_etro_url(job_name=job_name)
        #etro_stats = get_gearset_data(etro_gearset_url)

        etro_stats = getBaseStat(IsTank=False) #TODO make that work

        player_data = {
            "JobName": job_name,
            "PlayerName": player_name,
            "playerID": int(player_id),
            "weaponDelay": 3.0,#etro_stats.job.auto_speed,
            "stat": {
                "MainStat": etro_stats["MainStat"],
                "WD": etro_stats["WD"],
                "Det": etro_stats["Det"],
                "Ten": etro_stats["Ten"],
                "SS": etro_stats["SS"],
                "SkS": etro_stats["SkS"],
                "Crit": etro_stats["Crit"],
                "DH": etro_stats["DH"],
                "Piety" : etro_stats["Piety"]
            },
            "actionList": actions,
            "etro_gearset_url": "",
            "Auras": auras,
        }
        player_list.append(player_data)

    yield "ffxiv_sim.json", {
        "data": {
            "fightInfo": {
                "RequirementOn": True,
                "IgnoreMana": False,
                "fightDuration": fight_duration,
            },
            "PlayerList": player_list,
        },
        "mode": False,
        "TeamCompBonus": True,
        "MaxPotencyPlentifulHarvest": False,
        "nRandomIterations": 0,
    }


# Hard ignore on these events.
_IGNORE_IDS = {
    3, # Sprint
    7, # Autos
    8, # Autos
    33218, # Techbuff event
    27524, # Pneuma heal
    1000048 # Well fed
    }

_WAIT_OGCD = {
    "actionName": "WaitAbility",
    "waitTime": "0.65",
}

# Run replacements when these IDs are seen
_ID_REPLACEMENTS = {
    3: _WAIT_OGCD,  # Sprint
    3593: _WAIT_OGCD,
    16538: _WAIT_OGCD,  # Fey Illumn
    # 16558: "Horoscope",  # Activation?
    18873: "Ten",
    18877: "Chi",
    18881: "Jin",
}

# Run name replacements when these names are scene (other names have spaces removed by default)
_NAME_REPLACEMENTS = {
    "Medicated": "Potion",
    "Quadruple Technical Finish": "TechnicalFinish",
    "Double Standard Finish": "StandardFinish",
    "Braver": "MeleeLB1",
    "Bladedance": "MeleeLB2",
    "Chimatsuri": "MeleeLB3",
    **{
        lb_name: "MeleeLB3"
        for lb_name in [
            "Chimatsuri",
            "Final Heaven",
            "Doom of the Living",
            "Dragonsong Dive",
            "The End",
        ]
    },
}


def build_action_set(
    player_events,
    job_name: str,
    player_ids: Set[int],
) -> List[Dict]:
    """Builds an action set from a player's events."""
    x = 1
    return [
        {
            custom_columns.FIGHT_TIME: fight_time,
            custom_columns.ABILITY_ID: int(ability_id),
            **safe_check_ability_name( # This means it unpacks the returning dictionnary.
                ability_id=ability_id,
                ability_name=ability_name,
                job_name=job_name,
            ),
            # TargetID = 0 implies boss.
            custom_columns.TARGET_ID: (
                target_id if (target_id in player_ids) else 0
            ),
        }
        for fight_time, ability_id, ability_name, target_id in zip(
            player_events[custom_columns.FIGHT_TIME],
            player_events[custom_columns.ABILITY_ID],
            player_events[custom_columns.ABILITY_NAME],
            player_events[custom_columns.TARGET_ID],
        )
        if int(ability_id) not in _IGNORE_IDS  # Ignore autos, double tech
    ]


def safe_check_ability_name(
    ability_id: int, ability_name: str, job_name: str
) -> Dict[str, str]:
    """Handles conversion from ability ID to ffxiv-calc name + params."""
    output = _get_ffxiv_calc_ability_name(
        ability_id=ability_id,
        ability_name=ability_name,
        job_name=job_name,
    )
    return (
        output
        if isinstance(output, dict)
        else {
            "actionName": output,
        }
    )

_NAME_IGNORE = [
    "Well fed"
]


@functools.cache
def _get_ffxiv_calc_ability_name(
    ability_id: int, ability_name: str, job_name: str
) -> Union[Dict[str, str], str]:
    """Inner helper to handle all the edge-cases."""
    if ability_name in _NAME_IGNORE:
        return None
    if ability_name in _NAME_REPLACEMENTS:
        return _NAME_REPLACEMENTS[ability_name]
    if ability_id in _ID_REPLACEMENTS:
        return _ID_REPLACEMENTS[ability_id]
    cls_enum, job_enum = SOURCE_SUBTYPE_TO_ENUMS[job_name]
    name_from_id = ActionEnum.name_for_id(
        id=ability_id,
        cls=cls_enum,
        job_cls=job_enum,
    )

    if name_from_id != "Unknown":
        return name_from_id

    # Check name (with no whitespace) isn't mapped to another id
    ability_name_trimmed = ability_name.replace(" ", "")
    id_from_name = ActionEnum.id_for_name(
        name=ability_name_trimmed,
        cls=cls_enum,
        job_cls=job_enum,
    )

    if id_from_name != -1:
        LOG.debug(
            f"Ability {ability_id} corrected to {id_from_name} ({ability_name_trimmed})"
        )
        return ability_name_trimmed

    LOG.debug(f"Unmatched ID {ability_id} ({ability_name}): Assuming wait OGCD")
    return _WAIT_OGCD


AURA_MAPPINGS = {
    "Sharpcast": "SharpCast",
    "Ley Lines": "Ley Lines",
    "Soulsow": "Soulsow",
    "Medicated": "Medicated",
    "Meikyo Shisui": "Meikyo Shisui",
    "Mudra": "Mudra",
    "Eukrasia": "Eukrasia",
    "Standard Step": "Standard Step",
    "Standard Finish": "Standard Finish",
    "Closed Position": "Closed Position",
    "Dance Partner": "Dance Partner",
    "Technical Step" : "Technical Step",
    "Triplecast" : "Triplecast",
    "Inner Release" : "Inner Release",
    "Fight or Flight" : "Fight or Flight",
    "Delirium" : "Delirium",
    "Blood Weapon" : "Blood Weapon",
    "Blackest Night" : "Blackest Night",
    "No Mercy" : "No Mercy",
    "Arcane Circle" : "Arcane Circle",
    "Riddle of Fire" : "Riddle of Fire",
    "Riddle of Wind" : "Riddle of Wind",
    "Life Surge" : "Life Surge",
    "Lance Charge" : "Lance Charge",
    "Battle Litany" : "Battle Litany",
    "Right Eye" : "Right Eye",
    "Left Eye" : "Left Eye",
    "Kassatsu" : "Kassatsu",
    "Battle Voice" : "Battle Voice",
    "Acceleration" : "Acceleration",
    "Embolden" : "Embolden",
    "Searing Light" : "Searing Light",
    "Presence of Mind" : "Presence of Mind",
    "Earthly Dominance" : "Earthly Dominance",
    "Arrow Drawn": "Arrow Drawn",
    "Balance Drawn": "Balance Drawn",
    "Ewer Drawn": "Ewer Drawn",
    "Spire Drawn": "Spire Drawn",
    "Spear Drawn": "Spear Drawn",
    "Bole Drawn": "Bole Drawn",
    "Royal Guard" : "Royal Guard",
    "Grit" : "Grit",
    "Iron Will" : "Iron Will",
    "Defiance" : "Defiance",
    "Reassembled" : "Reassembled"
}


def build_aura_list(player_auras: pd.DataFrame) -> List[str]:
    """Builds a list of pre-defined mapped auras."""
    if player_auras.empty:
        return []
    return [
        AURA_MAPPINGS[aura]
        for aura, job_name in zip(
            player_auras["name"], player_auras["source_subtype"]
        )
        if aura in AURA_MAPPINGS
        and not (
            # Ignore standard finish if job is not dancer
            aura == "Standard Finish"
            and job_name != "Dancer"
        )
    ]


SOURCE_SUBTYPE_TO_ENUMS = {
    "DarkKnight": (ActionEnum.TankActions, ActionEnum.DarkKnightActions),
    "Gunbreaker": (ActionEnum.TankActions, ActionEnum.GunbreakerActions),
    "Paladin": (ActionEnum.TankActions, ActionEnum.PaladinActions),
    "Warrior": (ActionEnum.TankActions, ActionEnum.WarriorActions),
    "Ninja": (ActionEnum.MeleeActions, ActionEnum.NinjaActions),
    "Samurai": (ActionEnum.MeleeActions, ActionEnum.SamuraiActions),
    "Reaper": (ActionEnum.MeleeActions, ActionEnum.ReaperActions),
    "Monk": (ActionEnum.MeleeActions, ActionEnum.MonkActions),
    "Dragoon": (ActionEnum.MeleeActions, ActionEnum.DragoonActions),
    "Dancer": (ActionEnum.RangedActions, ActionEnum.DancerActions),
    "Bard": (ActionEnum.RangedActions, ActionEnum.BardActions),
    "Machinist": (ActionEnum.RangedActions, ActionEnum.MachinistActions),
    "RedMage": (ActionEnum.CasterActions, ActionEnum.RedMageActions),
    "BlackMage": (ActionEnum.CasterActions, ActionEnum.BlackMageActions),
    "Summoner": (ActionEnum.CasterActions, ActionEnum.SummonerActions),
    "Astrologian": (ActionEnum.HealerActions, ActionEnum.AstrologianActions),
    "Scholar": (ActionEnum.HealerActions, ActionEnum.ScholarActions),
    "Sage": (ActionEnum.HealerActions, ActionEnum.SageActions),
    "WhiteMage": (ActionEnum.HealerActions, ActionEnum.WhiteMageActions),
}


#@functools.cache
#def get_yaml_schema(file_name: str) -> Dict:
#    with open(file_name, "r") as file:
#        return yaml.safe_load(file)


#def get_default_etro_url(job_name: str) -> str:
#    """Inner helper to handle all the edge-cases."""
#    return get_yaml_schema(
#        os.path.join("main", "calc", "comps", "default.yaml")
#    )["6.4"][custom_columns.TARGET_SUBTYPE_TO_JOB[job_name]]