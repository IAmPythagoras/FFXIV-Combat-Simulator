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
        self.playerID = 0
        self.hasPotion = False

    def setPlayerID(self,newID : int ):
        self.playerID = newID

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

    def setHasPotion(self):
        """This function sets the value of the field hasPotion to True
        """
        self.hasPotion = True

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

        if self.hasPotion : crititalDH += " Pot"

        return self.Name + " ; " + str(self.Potency) + " ; " + str(self.Damage) + " " + crititalDH + " ; " + " ; " + str(self.TimeStamp) + " ; " + percentBuffStr + " ; " + dhBuffStr + " ; " + critBuffStr

class SimulationRecord:

    def __init__(self):
        self.pageList = []
        self.idList = []

    def addPage(self, newPage : page):
        self.pageList.append(newPage)

    def __str__(self):
        rString = ""
        specId = len(self.idList) == 0

        for pages in self.pageList:
            if specId or (pages.playerID in self.idList) : rString += str(pages) + "\n"

        return rString

    def saveRecordText(self, idList : list = []):
        """
        This function saves the record as a text file.
        """

        self.idList = idList

        f = open("SimulationRecord.txt", "w")
        f.write(str(self))
        f.close()

    def saveRecord(self,idList : list = []):
        """
        This function saves the record as a plot (pdf).
        """

        colName = ["Name", "Potency", "Damage", "", "Time","Buff", "DH Buff", "Crit Buff"]
        haList = ["left","right","right","center","right","left","center","center"]

        posOffSet = [1.3,0.8,0.1,0.5,0.2,4.8,2]
                             # Generating pos list
        curPos = 0
        pos = [0]
        for offset in posOffSet:
            curPos += offset
            pos.append(curPos)
        nrows = len(self.pageList)
        ncols = len(colName)
                             # This works well. Found by just using a configuration that looked good
                             # and using the ratio of nrows to height.
        height = ((160/538) * nrows)

        fig = plt.figure(figsize=(14,height), dpi=300)
        ax = plt.subplot(111)
        ax.set_xlim(0, int(1.5*ncols))
        ax.set_ylim(0, 5*(nrows+1))
        ax.set_axis_off()
        offset = 0
        size = 6

        for y in range(nrows-1,-1,-1):
            curPercentCount = 0
            percentBuffStr = ""
            dhBuffStr = ""
            critBuffStr = ""

            for buffs in self.pageList[nrows-y-1].PercentBuffList:
                curPercentCount += 1
                percentBuffStr += str(buffs) + ("\n" if curPercentCount%4 == 0 else " ")

            if self.pageList[nrows-y-1].hasPotion : percentBuffStr += "Potion "

            for buffs in self.pageList[nrows-y-1].DHBuffList:
                dhBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%) "
            for buffs in self.pageList[nrows-y-1].CritBuffList:
                critBuffStr += buffs[0] + "(" + str(int(buffs[1]*100)) + "%) "

                             # Removing last character which is a \n
            percentBuffStr = percentBuffStr[:-1]
            dhBuffStr = dhBuffStr[:-1]
            critBuffStr = critBuffStr[:-1]
            yPos = 5*(y+1)-2
            
            ax.annotate(
                xy=(pos[0],yPos),
                text=self.pageList[nrows-y-1].Name,
                ha=haList[0],
                fontsize=size+1
            )
            ax.annotate(
                xy=(pos[1],yPos),
                text=self.pageList[nrows-y-1].Potency,
                ha=haList[1],
                fontsize=size+1
            )
            ax.annotate(
                xy=(pos[2],yPos),
                text=self.pageList[nrows-y-1].Damage,
                ha=haList[2],
                fontsize=size+1
            )
            crititalDH = ""
            if self.pageList[nrows-y-1].autoCrit : crititalDH += "!"
            if self.pageList[nrows-y-1].autoDH : crititalDH += "!"
            ax.annotate(
                xy=(pos[3],yPos),
                text=crititalDH,
                ha=haList[3],
                fontsize=8,
                weight="bold"
            )
            ax.annotate(
                xy=(pos[4],yPos),
                text=self.pageList[nrows-y-1].TimeStamp,
                ha=haList[4],
                fontsize=size
            )
            ax.annotate(
                xy=(pos[5],yPos),
                text=percentBuffStr,
                ha=haList[5],
                fontsize=size if curPercentCount <= 4 else 5
            )
            ax.annotate(
                xy=(pos[6],yPos),
                text=dhBuffStr,
                ha=haList[6],
                fontsize=6
            )
            ax.annotate(
                xy=(pos[7],yPos),
                text=critBuffStr,
                ha=haList[7],
                fontsize=6
            )

        for j, name in enumerate(colName):
            ax.annotate(
                xy=(pos[j], 5*(nrows+1)),
                text=name,
                weight='bold',
                ha=haList[j]
            )

        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [5*(nrows+1)-1, 5*(nrows+1)-1], lw=1.5, color='black', marker='', zorder=4)
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='black', marker='', zorder=4)
        for x in range(1, 5*(nrows),5):
            ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x+1, x+1], lw=1.15, color='gray', ls=':', zorder=3 , marker='')

        plt.savefig(
        'SimulationRecord.pdf',
        dpi=700,
        bbox_inches='tight'
        )



