"""
This file contains the parser will translate code in a way the simulator can use.


The language contains the following :

SET fieldName Value -> This will set the given fieldName to a given value. Type checking is done on the value that was previously there
                                                                           and an error will be thrown if type does not match.
FORCESET fieldName Value -> Same as SET, but does not do type check and forces a new value on the field.

Every command must be delimited by a ; . Invalid text within ; will be ignored.
"""

from copy import deepcopy


class commandNotFound(Exception):
    # Expcetion is raised when the user tries to use an invalid command
    def __init__(self, cmd : str):

        self.message = f"The command '{cmd}' is invalid or not recognized."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

class fieldNotFound(Exception):
    # Expcetion is raised when the user tries to modify an invalid or nonexistant field on an object.
    def __init__(self, field : str, str_obj : str):

        self.message = f"The field '{field}' is invalid or not recognized for the object {str_obj}."
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message}'

commandList = ["SET", "FORCESET"]

commandExpectedInputAmount = {"SET" : 2, "FORCESET" : 2}

class parser:

    def __init__(self):
        pass

    def cleanCommandComponent(self, commandComponent : list) -> bool:
        """
        This command cleans up the given commandComponent and returns True if the command is valid.
        """
                             # Removing empty parts that might have been caused by missinputs
        commandComponent = self.filterEmpty(commandComponent)

                             # Check if initial entry is a valid command in commandList
        if not (commandComponent[0] in commandList) : return commandComponent,False

        return commandComponent, len(commandComponent[1:]) == commandExpectedInputAmount[commandComponent[0]]

    def filterEmpty(self, input):
        """
        This command filters the empty index of a list.
        """

        def emptyInput(s : str) -> bool:
            return len(s) != 0

        newInput = []

        for x in filter(emptyInput, input): newInput.append(x)

        return newInput

    def parseString(self, code : str) -> dict:
        """
        This function returns a dictionnary with the name of every fields as key and the value we want to set
        this field as. This does not type check and simply reads and output.
        """
                             # This list contains all command formatted in a way the simulator can understand.
        commandListCompiled = []

                             # Seperating by semi-colons (;)
        commandList = code.split(";")
        
        commandList = self.filterEmpty(commandList)

        for command in commandList:
            commandComponent = command.split(" ")
            commandComponent, valid = self.cleanCommandComponent(commandComponent)
            if not valid: raise commandNotFound(commandComponent[0])

                             # This is a list containing all information of the command in order.
            commandListFormat = []

            for i in range(commandExpectedInputAmount[commandComponent[0]]):
                commandListFormat.append(commandComponent[i+1])

            commandListCompiled.append({commandComponent[0] : deepcopy(commandListFormat)})

        return commandListCompiled
    

mainParser = parser()

def executeCode(sourceCode : str, targetObject):
    """
    This function receives as input sourceCode in the style defined above and
    applies the code to the targetobject.
    """

    commandList = mainParser.parseString(sourceCode)

    possibleFieldName = targetObject.__dict__.keys()

    for command in commandList:

        commandName = list(command.keys())[0]

        match commandName:
            case "FORCESET":
                fieldName = command["FORCESET"][0]
                if fieldName in possibleFieldName: 
                    targetObject.__dict__[fieldName] = command["FORCESET"][1]
            case "SET":
                fieldName = command["SET"][0]
                if fieldName in possibleFieldName: 
                    match targetObject.__dict__[fieldName]:
                        case int() : targetObject.__dict__[fieldName] = int(command["SET"][1])
                        case float() : targetObject.__dict__[fieldName] = float(command["SET"][1])
                        case str() : targetObject.__dict__[fieldName] = str(command["SET"][1])
                        case bool() : targetObject.__dict__[fieldName] = bool(command["SET"][1])
                else : raise fieldNotFound(fieldName, str(targetObject))

            





    