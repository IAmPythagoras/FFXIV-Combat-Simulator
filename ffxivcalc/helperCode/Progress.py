from time import time
from ffxivcalc.helperCode.helper_math import roundDown

class ProgressBar:
    """
    This class can be used to represent a progress bar that the user will see.
    You cannot use the __init__ method of the class, you must use the class method init()
    in order to get an iter(ProgressBar). To increment it simply use next(ProgressBar) and it will
    display itself.
    total : int -> total number of iterations
    name : str -> Name of the progress bar
    currentState : str -> Last generated frame of the progress bar
    extraBuffer : -> place to write the PB too
    """
    def __init__(self):
        self.total = 0
        self.currentProgress = 0
        self.name = ""
        self.currentState = ""
        self.extraBuffer = None
        self.showBar = True
        
                             # Timing related fields
        self.iterationAverage = 0 
        self.sumIterations = 0
        self.lastIterTime = 0
        self.lenLoadBar = 0

    def getCurrentState(self):
        return self.currentState
    
    def setShowBar(self, val):
        self.showBar = val

    def setExtraBuffer(self, buff):
        self.extraBuffer = buff

    def __iter__(self):
        self.currentProgress = -1
        self.name = self.name
        return self

    def __next__(self):
        """
        This function updates the progress of the bar and updates the display of the bar.
        """
        self.currentProgress += 1
        percent = int((self.currentProgress/self.total)*1000)/10


        curTimeIteration = time() - self.lastIterTime
        self.lastIterTime = time()
        self.sumIterations += curTimeIteration
        self.iterationAverage = round(self.sumIterations/self.currentProgress,1) if self.currentProgress > 0 else self.sumIterations

        predictedTime = round(self.iterationAverage * (self.total-self.currentProgress),1)

        bar = "❚" * int(percent) + "-" * (100-int(percent))

        loadBar = "\r"+ self.name +" |"+bar+"| " + ((str(percent) + " %") if self.currentProgress > 0 else "") + " ETA : " + str(predictedTime) + "s"
        self.currentState = loadBar
        if self.extraBuffer != None: self.extraBuffer['pb'] = loadBar
        

                             # This will remove characters that are not supposed to be there anymore
        if len(loadBar) > self.lenLoadBar: self.lenLoadBar = len(loadBar)
        for i in range(len(loadBar), self.lenLoadBar): loadBar += " "
                             # only print on screen if showBar is true
        if self.showBar: print(loadBar, end="\r")
        if (self.total - self.currentProgress == 0) and self.showBar:print()
        return self
    
    def complete(self):
        """
        This function will terminate the progress bar
        """
        self.currentProgress = self.total-1
        next(self)

    def setName(self, newName : str):
        """Sets the name of the progress bar to the newly given name
        """
        self.name = newName
    
    @classmethod
    def init(self, total : int, name : str, showBar : bool = True, extraBuffer = None):
        """
        This class method returns an iterator of the progress bar.

        total : int -> Total amount of iterations
        name : string -> name of loading bar (that is displayed)
        showBar : bool -> If true displays the progress bar using print()
        extraBuffer -> Dictionnary in which the pb view will be written at the key 'pb'
        """
        newProgressBar = ProgressBar()
        newProgressBar.total = total
        newProgressBar.name = name
        newProgressBar.lastIterTime = time()
        iterator = iter(newProgressBar)
        iterator.setExtraBuffer(extraBuffer)
        iterator.setShowBar(showBar)
        next(iterator)
        return iterator
    

if __name__ == "__main__":
    pass