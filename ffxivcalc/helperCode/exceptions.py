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

    Attributes:
        ActionName (str) : Name of the action which is given non valid target
        Target (object) : What was passed as target. Will display it as a string.
    """

    def __init__(self, ActionName : str, Target):
        self.Actionname = ActionName
        self.Target = str(Target)
        self.message = "The given target for " + ActionName + " is not valid. Given target"

        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message} {self.Target}'