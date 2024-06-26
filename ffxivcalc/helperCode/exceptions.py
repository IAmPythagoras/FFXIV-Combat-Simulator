class MateriaOverflow(Exception):
    """
    This exception is raised when trying to add a Materia to a gear that has reached its limit.
    """
    def __init__(self):
        self.message = "This gear piece cannot receive anymore Materias."

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

class InvalidFunctionParameter(Exception):
    """
    This exception is raised when a function's parameter is invalid.
    """
    def __init__(self, funcName : str, paramName : str, info : str):
        self.message = "The parameter " + paramName + " in the function " + funcName + " is invalid. Info " + info

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class InvalidStatRequest(Exception):
    """
    This exception is raised when the user does an invalid request of stat of a gear piece
    """
    pass

class InvalidGearSpace(Exception):
    """
    This exception is raised when the GearSpace is invalid.
    """
    def __init__(self, missingKey : str):
        self.message = "The GearSpace is missing gear piece of type " + missingKey

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

class MultiValuedWeaponDelay(Exception):
    """This exception is raised when weapons in a gear space have different weapon delay value
    """

    def __init__(self, weaponDelay : int, newWeaponDelay : int):
        self.message = f"The GearSpace has at least two weapons with different 'weaponDelay' value. Please make sure these values are identical : ( {weaponDelay} != {newWeaponDelay} )"

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

class InvalidFoodSpace(Exception):
    """
    This exception is raised when the FoodSpace is invalid.
    """
    def __init__(self):
        self.message = "The FoodSpace cannot be empty."

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

class InvalidMateriaSpace(Exception):
    """
    This exception is raised when the MateriaSpace is invalid.
    """
    def __init__(self):
        self.message = "The size of the MateriaSpace must be at least 3."

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
class InvalidTankBusterTargetNumber(Exception):
    """
    This exception is raised when an event is defined as a tank buster
    but has an invalid number of targets. Tank buster's number of targets
    must be 1 or 2. This error will be raised only if the Event has its "experimental"
    flag set to false (false by default). It must be, in any case, a positive value.

    Attributes:
        nTBTarget (int) : number of targets of the TB

    """

    def __init__(self, nTBTarget : int, id : int):
        self.nTBTarget = nTBTarget
        self.message = "targets for the tank buster with id " + str(id) + " is not in the valid range of 1 or 2."

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.nTBTarget} {self.message}'

class InvalidTarget(Exception):
    """
    This exception is raised when a non valid target is given as input to an action

    e.g: If an action cannot target the player casting it
         If the targetID is not an existing player

    Attributes:
        ActionName (str) : Name of the action which is given non valid target
        Caster (object) : The player object of the caster of the action.
        Target (object) : What was passed as target. Will display it as a string.
        InvalidID (bool) : If the given target ID is not a valid ID.
        TargetID (int) : ID of the target. Only used if InvalidID is True.
    """

    def __init__(self, ActionName : str, Caster, Target, InvalidID : bool, TargetID : int):
        self.Actionname = ActionName
        self.Target = str(Target)
        self.InvalidID = InvalidID
        self.message = "Player with ID "+str(Caster.playerID)+" has an invalid target. The given target for " + ActionName + " is not valid. Given target : "
        self.message_2 = "" if not InvalidID else " TargetID " + str(TargetID) + " is invalid." 

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message} {self.Target} {self.message_2}'
    
    def __repr__(self):
        return str(self)


class InvalidMitigation(Exception):
    """This exception is raised when a non valid mitigation object is being constructed.
    Such examples would be MagicMit and PhysicalMit being both True or a MitPercent value out of the
    acceptable range of (0,1).

    Args:
        InvalidRange (bool): Type of the Error. True -> MitPercent OOR, False -> MagicMit and PhysicalMit == True
        PercentMit (float) : Value of the PercentMit given
    """

    def __init__(self, InvalidRange = False, PercentMit : float = 0):
        self.PercentMit = PercentMit

        self.message = "A mitigation that is both only for Physical and for Magic damage was being constructed" if not InvalidRange else "The given PercentMit value " + str(self.PercentMit) + " is not within the valid range of (0,1)."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class InvalidFileName(Exception):
    """This exception is raised when given an invalid file name

    fileName : str
    """
    def __init__(self, fileName : str):

        self.message = "Invalid file name" + fileName
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class ActionNotFound(Exception):#Exception called if an action isn't found in the dictionnary
    pass
class JobNotFound(Exception):#Exception called if a Job isn't found
    pass

class playerIDNotFound(Exception):#Exception called if the player isn't found with the ID given by using the Fight.playerForID function.
    pass

class emptyEventList(Exception):
    # Exception is called if trying to give an enemy an empty event list.
    pass

class invalidFFLogsFightId(Exception):
    # Exception is called when the users asks to retrieve a fight from a fight list with a wrong id.
    def __init__(self, fight_id : str):

        self.message = "The provided fight id is invalid. Provided id : " + fight_id
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class invalidFFLogsQuery(Exception):
    # Exception is called when the users does an invalid query to fflogs
    def __init__(self, message : str):

        self.message = "Invalid FFLogs query. The query returned with this error message : " + message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class outDatedFFLogsCode(Exception):
    # Exception is raised when the user imports the FFLogsAPIRequest module.
    def __init__(self):

        self.message = "The module 'ffxivcalc.Request.FFLogsAPIRequest' is no longer up to date. Use 'ffxivcalc.Request.FFLogs_api' instead."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class outDatedAPICode(Exception):
    # Expcetion is raised when the user tries to import the API module.
    def __init__(self):

        self.message = "The module 'ffxivcalc.API' is outdated and has been deactivated, please do not import it. If you still want to use it add a try/except block (not recommend)."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
    
class deactivatedModuleCodeParser(Exception):
    # Expcetion is raised when the user tries to import the codeParser module.
    def __init__(self):

        self.message = "The module 'ffxivcalc.codeParser' is outdated and has been deactivated, please do not import it. If you still want to use it add a try/except block (not recommend)."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'
