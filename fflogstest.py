from ffxivcalc.helperCode.helper_backend import RestoreFightObject

from ffxivcalc.Request.FFLogs_api import getSingleFightData

data = getSingleFightData("9b8e6c18-39d6-4ae0-91c7-e9221e699769", "u0j8e1aIygCejB6HiBJFJcr0RB1MSIkVkLdgxDox", "YbDaH9C6dNVJAh8T",
                          "67", showProgress=True)
RestoreFightObject(data)