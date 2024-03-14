"""Defines accessors for defined game data (potency, buffs, etc)."""
import logging
import operator
import os
import pprint
from typing import Dict, Optional

import numpy as np
import pandas as pd

from ffxivcalc.Request import custom_columns

LOG = logging.getLogger(__name__)

DATA_FOLDER = os.path.join(os.getcwd(), "fflogtest")

def _read_csv(path: str) -> pd.DataFrame:
    """Reads a csv, uses file update and size to cache."""
    return pd.read_csv(path, index_col=[0])


def buffs() -> pd.DataFrame:
    buffs = _read_csv(os.path.join(DATA_FOLDER, "misc", "buffs.csv"))
    buffs[custom_columns.DAMAGE_MULTIPLIER] = buffs[
        custom_columns.DAMAGE_MULTIPLIER
    ].fillna(1.0)
    buffs[custom_columns.CRIT_BONUS] = buffs[custom_columns.CRIT_BONUS].fillna(
        0.0
    )
    buffs[custom_columns.DHIT_BONUS] = buffs[custom_columns.DHIT_BONUS].fillna(
        0.0
    )
    buffs[custom_columns.MAIN_STAT_BONUS] = buffs[
        custom_columns.MAIN_STAT_BONUS
    ].fillna(0)
    return buffs


def dots() -> pd.DataFrame:
    """Gets dot data."""
    dots = _read_csv(os.path.join(DATA_FOLDER, "misc", "dots.csv"))
    if custom_columns.GROUND_BASED not in dots.columns:
        dots[custom_columns.GROUND_BASED] = False
    dots[custom_columns.GROUND_BASED] = dots[
        custom_columns.GROUND_BASED
    ].fillna(False)
    return dots


def abilities(job_name: str) -> Optional[pd.DataFrame]:
    """Outputs abilities by job.

    Columns abilityGameID,ability_name,ability_potency,ability_type,GCD,source_type
    """
    fpath = os.path.join(DATA_FOLDER, "abilities", f"{job_name}.csv")
    if job_name is not None and os.path.exists(fpath):
        data = _read_csv(fpath)

        # handle source_type column
        if custom_columns.SOURCE_TYPE not in data.columns:
            data[custom_columns.SOURCE_TYPE] = "Player"
        data[custom_columns.SOURCE_TYPE] = data[
            custom_columns.SOURCE_TYPE
        ].fillna("Player")

        if custom_columns.GUARANTEED_CRIT not in data.columns:
            data[custom_columns.GUARANTEED_CRIT] = False
        data[custom_columns.GUARANTEED_CRIT] = data[
            custom_columns.GUARANTEED_CRIT
        ].fillna(False)

        if custom_columns.GUARANTEED_DHIT not in data.columns:
            data[custom_columns.GUARANTEED_DHIT] = False
        data[custom_columns.GUARANTEED_DHIT] = data[
            custom_columns.GUARANTEED_DHIT
        ].fillna(False)

        if custom_columns.POSITIONAL not in data.columns:
            data[custom_columns.POSITIONAL] = False
        data[custom_columns.POSITIONAL] = data[
            custom_columns.POSITIONAL
        ].fillna(False)

        if custom_columns.SPECIAL_FORMULA not in data.columns:
            data[custom_columns.SPECIAL_FORMULA] = False
        data[custom_columns.SPECIAL_FORMULA] = data[
            custom_columns.SPECIAL_FORMULA
        ].fillna(False)

        if custom_columns.GCD in data.columns:
            # Do a fix
            data[custom_columns.ABILITY_TYPE] = np.where(
                data[custom_columns.GCD].isna(),
                "",
                np.where(
                    data[custom_columns.GCD],
                    custom_columns.GCD,
                    custom_columns.OGCD,
                ),
            )
            data = data.drop(columns=[custom_columns.GCD])
            data.to_csv(
                os.path.join(DATA_FOLDER, "abilities", f"{job_name}.csv")
            )

        return data

    return None


def clean_name(name: str):
    """handles name formatting bs, hissatsu being the worst."""
    try:
        if isinstance(name, dict):
            return name["name"]

        if "Hissatsu:" in name:
            return (
                name[name.find("Hissatsu:") :]
                .split(",")[0]
                .strip()
                .replace('"', "")
                .replace("'", "")
            )

        if "Kaeshi:" in name:
            return (
                name[name.find("Kaeshi:") :]
                .split(",")[0]
                .strip()
                .replace('"', "")
                .replace("'", "")
            )

        if name.startswith("{"):
            return [
                p.split(":")[1].strip().replace('"', "").replace("'", "")
                for p in name.split(",")
                if "name" in p
            ][0]
        return name
    except Exception:
        print(name)
        raise


def clean_names(ids_to_names: Dict):
    return {ids: clean_name(value) for ids, value in ids_to_names.items()}


def ability_ids_to_names() -> Dict:
    """Fetches the ability ids to names table."""
    path = os.path.join(DATA_FOLDER, "fflogs_metadata", "id_to_name.csv")
    if not os.path.exists(path):
        return {}

    # Do an inner function that is cached to avoid too much usage
    data = _read_csv(path)
    return {
        int(ability_id): ability_name
        for ability_id, ability_name in zip(
            data[custom_columns.ABILITY_ID], data[custom_columns.ABILITY_NAME]
        )
    }


def update_ability_ids_to_names(updates: Dict) -> None:
    """Updates the ability ids to names table."""
    cur = ability_ids_to_names()
    new = {**cur, **clean_names(updates)}

    if cur == new:
        LOG.info("Skipping ID update, no new abilities found.")
        return

    LOG.info(f"Updating data with newly found ability id <--> name mappings")
    LOG.info(
        pprint.pformat(
            {
                new_id: new_name
                for new_id, new_name in new.items()
                if new_id in updates and new_id not in cur
            }
        )
    )

    new_csv = [
        {
            custom_columns.ABILITY_ID: ability_id,
            custom_columns.ABILITY_NAME: ability,
        }
        for ability_id, ability in sorted(
            new.items(), key=operator.itemgetter(0)
        )
    ]

    pd.DataFrame(new_csv).to_csv(
        os.path.join(DATA_FOLDER, "fflogs_metadata", "id_to_name.csv")
    )


def get_lb_damage_data() -> Optional[pd.DataFrame]:
    """Gets lb damage data."""
    path = os.path.join(DATA_FOLDER, "lb", "lb.csv")

    if not os.path.exists(path):
        return None
    data = _read_csv(path)

    return data


def update_lb_data(data: pd.DataFrame) -> None:
    cur = get_lb_damage_data()
    important_shit = data[
        [custom_columns.ABILITY_NAME, custom_columns.LOG_DAMAGE]
    ]
    if cur is None:
        pd.DataFrame(important_shit).to_csv(
            os.path.join(DATA_FOLDER, "lb", "lb.csv")
        )
        return

    pd.concat([cur, important_shit]).to_csv(
        os.path.join(DATA_FOLDER, "lb", "lb.csv")
    )