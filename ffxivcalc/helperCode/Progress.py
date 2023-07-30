class ProgressBar:
    """
    This class can be used to represent a progress bar that the user will see.
    You cannot use the __init__ method of the class, you must use the class method init()
    in order to get an iter(ProgressBar). To increment it simply use next(ProgressBar) and it will
    display itself.
    total : int -> total number of iterations
    name : str -> Name of the progress bar
    """
    def __init__(self):
        self.total = 0
        self.currentProgress = 0
        self.name = ""


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
        bar = "❚" * int(percent) + "-" * (100-int(percent))
        print("\r"+ self.name +" |"+bar+"| " + ((str(percent) + " %") if self.currentProgress > 0 else ""), end="\r")
        if self.total - self.currentProgress == 0:print()
        return self
    
    def complete(self):
        """
        This function will terminate the progress bar
        """
        self.currentProgress = self.total-1
        next(self)
    
    @classmethod
    def init(self, total : int, name : str):
        """
        This class method returns an iterator of the progress bar.
        """
        newProgressBar = ProgressBar()
        newProgressBar.total = total
        newProgressBar.name = name
        iterator = iter(newProgressBar)
        next(iterator)
        return iterator