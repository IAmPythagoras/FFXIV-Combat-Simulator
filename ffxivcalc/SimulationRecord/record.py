"""
This file contains the class SimulationRecord. This class contains a list of events to be recapped. 
For now events are defined as an action that deals damage. It will be recorded with some information.
the SimulationRecord object will then be able to output an array that contains the information of the whole fight in a clear way.

A SimulationRecord contains a list of page which are defined as individual events. There are multiple subclasses of page each defining a specific
event. maybe not? have to think. Ima keep it simple for now

This is supposed to be an alternative to logs. Making something that has still a good amount of information but is easier to read.
"""

import matplotlib.pyplot as plt

class page:
    """
    This contains the information of one individual event.
    Potency (int) : Potency of the action
    Damage (int) : Total Damage of the action
    TimeStamp (float) : TimeStamp of the action (when it applies damage)
    PercentBuffList (list[buff]) : List of Percent Buff.
    DHBuffList (list) : List of DH buff
    CritBuffList (list) : List of Crit buff
    """

    def __init__(self):
        self.Name = "Unnamed"
        self.Potency = 0
        self.Damage = 0
        self.TimeStamp = 0.0
        self.autoCrit = False
        self.autoDH = False
        self.PercentBuffList = []
        self.DHBuffList = []
        self.CritBuffList = []

    def setName(self, name : str):
        self.Name = name

    def setPotency(self, newPotency : int):
        self.Potency = newPotency

    def setDamage(self, newDamage : int):
        self.Damage = newDamage

    def setTimeStamp(self, newTimeStamp : float):
        self.TimeStamp = newTimeStamp

    def setAutoCrit(self, value : bool):
        self.autoCrit = value

    def setAutoDH(self, value : bool):
        self.autoDH = value

    def addPercentBuff(self, newEntry):
        self.PercentBuffList.append(newEntry)

    def addDHBuffList(self, newEntry):
        self.DHBuffList.append(newEntry)

    def addCritBuffList(self, newEntry):
        self.CritBuffList.append(newEntry)

    def __str__(self) -> str:

        percentBuffStr = ""
        dhBuffStr = ""
        critBuffStr = ""
        
        for buffs in self.PercentBuffList:
            percentBuffStr += str(buffs)
        for buffs in self.DHBuffList:
            dhBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%)"
        for buffs in self.CritBuffList:
            critBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%)"

        crititalDH = ""

        if self.autoCrit : crititalDH += "!"
        if self.autoDH : crititalDH += "!"

        return self.Name + " ; " + str(self.Potency) + " ; " + str(self.Damage) + " ; " + " ; " + str(self.TimeStamp) + " ; " + percentBuffStr + " ; " + dhBuffStr + " ; " + critBuffStr + " ; " + crititalDH

class SimulationRecord:

    def __init__(self):
        self.pageList = []

    def addPage(self, newPage : page):
        self.pageList.append(newPage)

    def __str__(self):
        rString = ""

        for pages in self.pageList:
            rString += str(pages) + "\n"

        return rString

    def saveRecordText(self):
        """
        This function saves the record as a text file.
        """
        f = open("SimulationRecord.txt", "w")
        f.write(str(self))
        f.close()

    def saveRecord(self):
        """
        This function saves the record as a plot.
        """

        colName = ["Name", "Potency", "Damage", "Buff", "DH Buff", "Crit Buff", "Hit Type"]
        nrows = len(self.pageList)
        ncols = len(colName)

        fig = plt.figure(figsize=(3,100), dpi=200)
        ax = plt.subplot(111)
        ax.set_xlim(0, ncols)
        ax.set_ylim(0, nrows)
        ax.set_axis_off()

        for y in range(nrows):
            percentBuffStr = ""
            dhBuffStr = ""
            critBuffStr = ""
            for buffs in self.pageList[y].PercentBuffList:
                percentBuffStr += str(buffs) + "\n"
            for buffs in self.pageList[y].DHBuffList:
                dhBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%)\n"
            for buffs in self.pageList[y].CritBuffList:
                critBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%)\n"
            ax.annotate(
                xy=(0.5,y),
                text=self.pageList[y].Potency,
                ha='center'
            )
            ax.annotate(
                xy=(1,y),
                text=self.pageList[y].Damage,
                ha='center'
            )
            ax.annotate(
                xy=(1.5,y),
                text=percentBuffStr,
                ha='center'
            )
            ax.annotate(
                xy=(2,y),
                text=dhBuffStr,
                ha='center'
            )
            ax.annotate(
                xy=(2.5,y),
                text=critBuffStr,
                ha='center'
            )
            crititalDH = ""
            if self.pageList[y].autoCrit : crititalDH += "!"
            if self.pageList[y].autoDH : crititalDH += "!"
            ax.annotate(
                xy=(3,y),
                text=crititalDH,
                ha='center'
            )

        fig.show()
        input()



