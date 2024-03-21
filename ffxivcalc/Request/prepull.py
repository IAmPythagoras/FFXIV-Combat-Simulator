"""
This code was written by Apollo (apollo.van.waddleburg on discord) and adapted to fit the needs of the sim.
"""

"""Defines utilities for determining important prepull buffs from fflogs."""
import logging
from typing import List

import pandas as pd

from ffxivcalc.Request import custom_columns

LOG = logging.getLogger(__name__)

# TODO: export into a configurable and accessable format
ALL = {
    "Medicated": 30,
    "Swiftcast": 10,
}

WAR = {
    "Inner Release": 15,
}

PLD = {
    "Fight or Flight": 20,
}

DRK = {
    "Delirium": 15,
    "Blood Weapon": 15,
    "Blackest Night": 7,
}

GNB = {
    "No Mercy": 20,
}

RPR = {
    "Arcane Circle": 20,
}

MNK = {
    "Riddle of Fire": 20,
    "Riddle of Wind": 15,
    "Brotherhood": 15,
}

DRG = {
    "Life Surge": 5,
    "Lance Charge": 20,
    "Battle Litany": 15,
    "Right Eye": 20,
    "Left Eye": 20,
}

NIN = {
    "Kassatsu": 15,
}

SAM = {
    "Meikyo Shisui": 15,
}

BRD = {
    "Battle Voice": 15,
}

DNC = {
    "Standard Finish": 30,
    "Technical Finish": 20,
    "Devilment": 20,
    # "Flourish":
}

MCH = {}

RDM = {
    "Acceleration": 20,
    "Dualcast": 5,
    "Embolden": 20,
}

BLM = {
    "Triplecast": 10,
    "Sharpcast": 30,
    "Ley Lines": 30,
}

SMN = {
    "Searing Light": 30,
}

WHM = {
    "Presence of Mind": 15,
}

AST = {
    "the Arrow": 15,
    "the Balance": 15,
    "the Ewer": 15,
    "the Spire": 15,
    "the Spear": 15,
    "the Bole": 15,
    "Divination": 15,
    "Earthly Dominance": 10,
    "Giant Dominance": 20,
}

SCH = {}

SGE = {
    "Eukrasia": 60,  # has no duration, 30 is fine.
}


POTENTIAL_PREPULL_BUFFS = {
    **ALL,
    **AST,
    **BLM,
    **BRD,
    **DNC,
    **DRG,
    **DRK,
    **GNB,
    **MCH,
    **MNK,
    **NIN,
    **RPR,
    **PLD,
    **SAM,
    **SGE,
    **SCH,
    **SMN,
    **WAR,
    **WHM,
}


def prepull_aura_frame(fight_events: pd.DataFrame) -> pd.DataFrame:
    """Builds a frame depicting prepull auras."""
    output = []
    combatantinfo = fight_events[
        fight_events[custom_columns.TYPE] == "combatantinfo"
    ]
    for (
        fight_time,
        source_id,
        source_name,
        source_type,
        source_subtype,
        auras,
    ) in zip(
        combatantinfo[custom_columns.FIGHT_TIME],
        combatantinfo[custom_columns.SOURCE_ID],
        combatantinfo[custom_columns.SOURCE_NAME],
        combatantinfo[custom_columns.SOURCE_TYPE],
        combatantinfo[custom_columns.SOURCE_SUBTYPE],
        combatantinfo["auras"],
    ):
        for aura in auras:
            output.append(
                {
                    custom_columns.FIGHT_TIME: fight_time,
                    custom_columns.SOURCE_ID: source_id,
                    custom_columns.SOURCE_NAME: source_name,
                    custom_columns.SOURCE_TYPE: source_type,
                    custom_columns.SOURCE_SUBTYPE: source_subtype,
                    **aura,
                }
            )

    return pd.DataFrame(output)


def infer_prepull_buff_casts(fight_events: pd.DataFrame) -> pd.DataFrame:
    """Infers all prepull buffs applications into a DF with all relevant data.

    Specifically, does the following:
        - Looks at the combatant info row to get starting buffs
        - For each one, looks for when the buff falls off in combat
        - From this, inferences the original application time
    """
    # Get the specific subframe for particular events.
    outputs: List[pd.DataFrame] = []

    # Get a quick subframe for the first refresh or removal of a buff
    buff_removal_or_refresh = (
        fight_events[
            (
                fight_events[custom_columns.TYPE].isin(
                    [custom_columns.REMOVE_BUFF, "refreshbuff"]
                )
            )
        ]
        .sort_values(by=[custom_columns.FIGHT_TIME], axis=0)
        .dropna(how="all", axis=1)
        .reset_index(drop=True)
    )

    # groupby each player, build outputs per player
    for player_name, info_data in fight_events[
        fight_events[custom_columns.TYPE] == "combatantinfo"
    ].groupby(by=custom_columns.SOURCE_NAME):
        LOG.debug(f"Finding auras for {player_name}")
        # while info data should be a single row, just loop through it for safety.
        for auras in info_data["auras"]:
            for aura in auras:
                # Check aura-names
                duration = POTENTIAL_PREPULL_BUFFS.get(aura["name"])
                if duration is None:
                    LOG.debug(f"Skipping {aura}, not tracking.")
                    continue
                LOG.debug(f"Processing auras {aura}.")

                # get the earliest removal or refresh of the buff
                specific_buff_removal_or_refresh = buff_removal_or_refresh[
                    (
                        buff_removal_or_refresh[custom_columns.TARGET_NAME]
                        == player_name
                    )
                    & (
                        buff_removal_or_refresh[custom_columns.ABILITY_NAME]
                        == aura["name"]
                    )
                ]

                if specific_buff_removal_or_refresh.empty:
                    LOG.warning(f"Unable to find removal event for {aura}")
                    continue

                earliest_buff_reference = specific_buff_removal_or_refresh.head(
                    1
                ).copy(deep=True)
                # Inference the original usage, via subtracting the fight-time
                earliest_buff_reference.iloc[
                    0,
                    earliest_buff_reference.columns.get_loc(
                        custom_columns.FIGHT_TIME
                    ),
                ] -= duration
                earliest_buff_reference.iloc[
                    0,
                    earliest_buff_reference.columns.get_loc(
                        custom_columns.TYPE
                    ),
                ] = custom_columns.ESTIMATED_APPLY_BUFF
                outputs.append(earliest_buff_reference)

    if not outputs:
        return pd.DataFrame()

    return (
        pd.concat(outputs, axis=0)
        .round({custom_columns.FIGHT_TIME: 3})
        .sort_values(by=[custom_columns.FIGHT_TIME], axis=0)
        .dropna(how="all", axis=1)
        .reset_index(drop=True)
    )