"""Fetches log data from a fflogs URL."""
import logging
import os
from typing import Dict, List, Tuple, Iterator, Optional

import requests
import dataclasses
import python_graphql_client
import pandas as pd

from ffxivcalc.Request import custom_columns
from ffxivcalc.Request import game_data
from ffxivcalc.helperCode.exceptions import invalidFFLogsFightId, invalidFFLogsQuery

LOG = logging.getLogger(__name__)


def get_auth_token() -> str:
    """Fetches an auth token via https://www.fflogs.com/oauth/token.

    See https://www.fflogs.com/api/docs/

    And https://www.fflogs.com/v2-api-docs/ff/report.doc.html

    Requires FFLOGS_CLIENT_ID and FFLOGS_CLIENT_SECRET set as environment variables.
    These can be obtained here: https://www.fflogs.com/api/clients/

    :returns: Auth token for FFLogs APIv2
    """
    LOG.debug(f"Fetching fflogs auth token")
    x = requests.post(
        url="https://www.fflogs.com/oauth/token",
        data={"grant_type": "client_credentials"},
        auth=(
            os.environ["FFLOGS_CLIENT_ID"],
            os.environ["FFLOGS_CLIENT_SECRET"],
        ),
    )

    x.raise_for_status()
    return x.json()["access_token"]

def get_fflog_events_dataframe(data: List) -> pd.DataFrame:
    """Converts fflog events into a dataframe with timestamp set."""
    event_data = pd.DataFrame(data)

    # Run lb-update hard sync to ensure damage taken instances are consistent
    potential_start_times = [
        event_data[event_data[custom_columns.TYPE] == custom_columns.DAMAGE][
            "timestamp"
        ].min()
    ]
    if event_data[custom_columns.TYPE].isin(["limitbreakupdate"]).any():
        potential_start_times.append(
            event_data[event_data[custom_columns.TYPE] == "limitbreakupdate"][
                "timestamp"
            ].min()
        )

    start_timestamp = min(potential_start_times)

    event_data.insert(
        0,
        custom_columns.FIGHT_TIME,
        ((event_data["timestamp"] - start_timestamp) / 1000.0).round(4),
    )
    del event_data["timestamp"]
    return event_data

@dataclasses.dataclass(frozen=True, repr=False)
class FFLogClientV2:
    """Base class for setting up an FFLogsClient."""

    client: python_graphql_client.GraphqlClient = dataclasses.field(
        default_factory=lambda: (
            python_graphql_client.GraphqlClient(
                endpoint="https://www.fflogs.com/api/v2/client",
                headers={"Authorization": f"Bearer {get_auth_token()}"},
            )
        )
    )

    # Caches outcomes from https://www.fflogs.com/v2-api-docs/ff/reportability.doc.html
    # Maps IDs to ability data
    # Structure:
    # {
    #     log_code: {
    #         ability_id (str): ability_data (dict)
    #         ...
    #     },
    #     ...
    # }
    ability_id_cache: Dict = dataclasses.field(default_factory=dict)

    # Caches outcomes from https://www.fflogs.com/v2-api-docs/ff/reportactor.doc.html
    # Maps ids to actor data
    actor_cache: Dict = dataclasses.field(default_factory=dict)

    def get_fights_enriched(self, code: str, fight_type: str) -> Dict:
        """Fetches the high level fights from a log. Contains more info than normal.

        Output contains info from both report and the fights.
        """
        LOG.debug(f"Fetching fflogs reportData:report:fights via {code}")
        data = self.client.execute(
            query="""query reportData($code: String!, $kills: KillType!){
                  reportData
                  {
                    report(code: $code){
                      endTime
                      startTime
                      guild{
                        name
                      }
                      fights(killType: $kills){
                        encounterID
                        startTime
                        endTime
                        name
                        kill
                        standardComposition
                        combatTime
                        id
                      }
                    }
                  }
                }
                """,
            variables={
                "code": code,
                "kills": fight_type,
            },
        )
        self._check_if_valid_query(data)
        return data["data"]["reportData"]["report"]

    def _check_if_valid_query(self,query : Dict):
        """Checks the validity of the returned query. If a query is invalid it contains the key 'message' with a message. An error
        will be raised an the message displayed to the user."""

        if 'errors' in query.keys():
            raise invalidFFLogsQuery(query['errors'][0]['message'])

    def _check_valid_fight_id(self,fightList : List[Dict], fight_id : str) -> bool:
        """Checks if the given id is within the retrieved fight list. Raises invalidFFLogsFightId if not valid."""

        if not fight_id in [
            str(fight['id']) for fight in fightList
        ]:
            raise invalidFFLogsFightId(fight_id)

    def get_fights(self, code: str,fight_type: str = "Kills") -> List[Dict]:
        """Fetches the high level fights from a log."""
        LOG.debug(f"Fetching fflogs reportData:report:fights via {code}")
        data = self.client.execute(
            query="""query reportData($code: String!, $kills: KillType!){
                  reportData
                  {
                    report(code: $code){
                      fights(killType: $kills){
                        id
                        encounterID
                        startTime
                        endTime
                        name
                        kill
                        standardComposition
                        combatTime
                      }
                    }
                  }
                }
                """,
            variables={
                "code": code,
                "kills": fight_type
            },
        )
        self._check_if_valid_query(data)

        return data["data"]["reportData"]["report"]["fights"]

    def get_abilities(self, code: str) -> List[Dict]:
        """Fetches the high level fights from a log."""
        LOG.debug(f"Fetching fflogs reportData:report:fights via {code}")
        data = self.client.execute(
            query="""query reportData($code: String!){
                  reportData
                  {
                    report(code: $code){
                      masterData{
                        abilities{
                          gameID
                          name
                          type
                        }
                      }
                    }
                  }
                }
                """,
            variables={
                "code": code,
            },
        )
        self._check_if_valid_query(data)

        return data["data"]["reportData"]["report"]["masterData"]["abilities"]

    def stream_fight_events(
        self, code: str, fight_type: str = "Kills", fight_id : str = ""
    ) -> Iterator:
        """Streams fight event data

        Structure:
            yield fight_name, [{events...}]
        """
        self._populate_caches(code=code)

        fightList = self.get_fights(code=code,fight_type=fight_type)

        if len(fight_id) != 0: self._check_valid_fight_id(fightList, fight_id)

        for fight in fightList:
            if fight_id != "" and str(fight["id"]) != fight_id : continue
            yield (
                fight["name"],
                self._process_fight_data(
                    data=self.get_raw_events_from_fight(
                        code=code,
                        fight=fight,
                        fight_type=fight_type,
                    ),
                    code=code,
                ),
            )

    def _process_fight_data(self, data: Iterator, code: str) -> List:
        """Applies actor and ability name replacement."""
        return [
            self._process_raw_event(data=raw_data_event, code=code)
            for raw_data_event in data
        ]

    def _process_raw_event(self, data: Dict, code: str) -> Dict:
        if "extraAbilityGameID" in data:
            data["abilityGameID"] = data["extraAbilityGameID"]
            
        if "abilityGameID" in data:
            data[custom_columns.ABILITY_NAME] = self._get_ability(
                data["abilityGameID"], code=code
            )

        if "sourceID" in data:
            data[custom_columns.SOURCE_NAME] = self._get_actor_name(
                data["sourceID"], code=code
            )
            source_actor = self._get_actor(data["sourceID"], code=code)
            if source_actor:
                data[custom_columns.SOURCE_TYPE] = source_actor["type"]
                data[custom_columns.SOURCE_SUBTYPE] = source_actor["subType"]
                if source_actor["petOwner"]:
                    data[
                        custom_columns.SOURCE_PET_ACTOR
                    ] = self._get_actor_name(
                        source_actor["petOwner"], code=code
                    )

        if "targetID" in data:
            data[custom_columns.TARGET_NAME] = self._get_actor_name(
                data["targetID"], code=code
            )
            target_actor = self._get_actor(data["targetID"], code=code)
            if target_actor:
                data[custom_columns.TARGET_TYPE] = target_actor["type"]
                data[custom_columns.TARGET_SUBTYPE] = target_actor["subType"]
                if target_actor["petOwner"]:
                    data[
                        custom_columns.TARGET_PET_ACTOR
                    ] = self._get_actor_name(
                        target_actor["petOwner"], code=code
                    )

        return data

    def _get_ability(self, ability_id: str, code: str) -> str:
        if code not in self.ability_id_cache:
            self._populate_caches(code)

        return (
            "UNKNOWN"
            if ability_id not in self.ability_id_cache[code]
            else (self.ability_id_cache[code][ability_id]["name"])
        )

    def _get_actor(self, actor_id: str, code: str) -> Optional[Dict]:
        """Gets the full actor data."""
        if code not in self.actor_cache:
            self._populate_caches(code)

        return self.actor_cache[code].get(actor_id)

    def _get_actor_name(self, actor_id: str, code: str) -> Optional[str]:
        """Gets the full actor name. Adjusts pet names to include owner."""
        actor: Optional[Dict] = self._get_actor(actor_id=actor_id, code=code)
        if actor is None:
            return None

        if not actor["petOwner"]:
            return actor["name"]

        pet_owner: Optional[Dict] = self._get_actor(
            actor_id=actor["petOwner"], code=code
        )["name"]

        return f"{actor['name']} ({pet_owner})"

    def _populate_caches(self, code: str) -> None:
        LOG.debug(f"Fetching fflogs reportData:report:masterData via {code}")
        log_data = self.client.execute(
            query="""query reportData($code: String!){
                          reportData
                          {
                            report(code: $code){
                              masterData{
                                abilities {
                                  gameID
                                  name
                                  type
                                }
                                actors {
                                  id
                                  name
                                  petOwner
                                  subType
                                  type
                                }
                              }
                            }
                          }
                        }
                        """,
            variables={"code": code},
        )
        self._check_if_valid_query(log_data)

        log_data = log_data["data"]["reportData"]["report"]["masterData"]

        self.ability_id_cache[code] = {
            ability["gameID"]: ability for ability in log_data["abilities"]
        }

        self.actor_cache[code] = {
            actor["id"]: actor for actor in log_data["actors"]
        }

        LOG.debug(f"Stored actor and ability ids.")

        self._update_id_data()

        return

    def _update_id_data(self):
        """Updates the current database csv of ability ids."""
        # flatten the dictionary to remove codes
        updates = {}
        for ids_to_abilities in self.ability_id_cache.values():
            updates = {
                **updates,
                **{
                    ability["gameID"]: ability
                    for ability in ids_to_abilities.values()
                },
            }
        game_data.update_ability_ids_to_names(updates)

    def get_raw_events_from_fight(
        self, code: str, fight: Dict, fight_type: str = "Kills"
    ) -> Iterator:
        """Gets the raw events from fight."""
        next_timestamp = start_time = fight["startTime"]
        end_time = fight["endTime"]
        LOG.debug(
            f"Fetching fflogs reportData:report:events via {code} [{start_time}, {end_time}]"
        )

        # Pretty animation

        percent_complete = (
            "{:5.2f}%".format(
                (float(next_timestamp) - float(start_time))
                / (float(end_time) - float(start_time))
                * 100.0
            )
            if (float(end_time) > float(start_time))
            else "100%"
        )
        animation: str = f"Loading {fight['name']} ({percent_complete})"
        while next_timestamp is not None and int(next_timestamp) < int(
            end_time
        ):
            # Pretty animation
            print(animation, end="\r")
            page_data, next_timestamp = self._get_events_from_fight(
                code=code,
                start_time=next_timestamp,
                end_time=end_time,
                fight_type=fight_type,
            )

            for event_data in page_data:
                yield event_data

            percent_complete = "{:5.2f}%".format(
                (float(next_timestamp or end_time) - float(start_time))
                / (float(end_time) - float(start_time))
                * 100.0
            )
            animation: str = f"Loading {fight['name']} ({percent_complete})"
        print(f"{animation}: DONE")

    def _get_events_from_fight(
        self,
        code: str,
        start_time: str,
        end_time: str,
        fight_type: str = "Kills",
    ) -> Tuple:
        """Inner function for the timestamp management."""
        raw_data = self.client.execute(
            query="""query reportData($code: String!, $startTime: Float!, $endTime: Float!, $kills: KillType!, $limit: Int!){
                          reportData
                          {
                            report(code: $code){
                              events(killType: $kills, startTime: $startTime, endTime: $endTime, limit: $limit){
                                data
                                nextPageTimestamp
                              }
                            }
                          }
                        }
                        """,
            variables={
                "code": code,
                "startTime": start_time,
                "endTime": end_time,
                "kills": fight_type,
                "limit": 10000,
            },
        )

        self._check_if_valid_query(raw_data)
        raw_data = raw_data["data"]["reportData"]["report"]["events"]

        return raw_data["data"], raw_data["nextPageTimestamp"]