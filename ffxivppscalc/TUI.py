import os
from SimulationInput import ExecuteMemoryCode
from UI_backend import AskInput, ImportFightBackend, MergeFightBackEnd, SaveFight, SimulateFightBackend


def SimulateFightMemory():
    os.system('CLS') #clearing HUD
    #This will simulate the fight in memory

    #We will first go through some options
    print(
        "===================== SIMULATOR ====================="
    )

    #Looking at all fights we have saved

    cur_dir = os.getcwd()

    #the saved directory should be in that same folder

    saved_dir = cur_dir + "\\saved"

    saved_fight = os.listdir(saved_dir)
    number_saved_fight = len(saved_fight)
    selected_fight = ""

    if number_saved_fight == 0: #No fight saved
        print("No saved fights were found. Hit any button to return to the main menu.")
        input("...")
        return
    else: #Saved fight
        print(
            "Select one of the saved fights : "+ "\n" + 
            "=========================================================="
            )
        for i in range(1,number_saved_fight+1):
            print(str(i) + " -> " + saved_fight[i-1])

        print("==========================================================")

        userInput = int(AskInput(number_saved_fight))

        selected_fight = saved_fight[userInput-1] #Selecting fight

    
    SimulateFightBackend(saved_dir + "\\" + selected_fight)

    

def ImportFight():
    os.system('CLS') #clearing HUD
    print(
        "===================== IMPORT FIGHT FROM FFLOGS =====================" + "\n" +
        "THIS IS VERY EXPERIMENTAL" + "\n" +
        "The program does not check if the fight is valid, and will simply result in a crash if it is not."
    )

    fightID = input("Please enter the fightID : ")
    fightNumber = input("Please enter the fight's number : ")

    print("Converting FFLogs fight into Event object...")

    Event = ImportFightBackend(fightID, fightNumber)

    userInput = input("What name do you wish to save this fight as : ")

    SaveFight(Event, 0, 1000, userInput)




def CreateFight():
    os.system('CLS') #clearing HUD

def Credits():
    os.system('CLS') #clearing HUD
    #This menu displays credits
    print(
        "=================================================== CREDITS =======================================================" + "\n" + 
        "This program was made mainly by myself, but I was helped by a lot of friends" + "\n" +
        "and other people without whom this project would not have been possible." + "\n" +
        "I listed here all those that helped with a short description of what they did." + "\n" +
        "I personally thank everyone here for the help they brought :)" + "\n" +
        "I will put their discord IDs in case you wish to contact them." + "\n" +
        "=================================================================================================================" + "\n" +
        "Pythagoras#6312 -> That's me! Did most of it" + "\n" +
        "ne0dym#7837 -> DarkKnight code and other revisions" + "\n" +
        "Bri-kun#6539 -> Networking code and other FFLogsAPI related stuff" + "\n" +
        "javaJake#0001 -> Theoretical damage computation" + "\n" +
        "Saint Germain#0280 -> Bit of Monk code" + "\n" +
        "apollo#3810 -> Put me in contact with javajake and also provided some background code for working with FFLogsAPI" + "\n" +
        "Ikuni#2735 -> Helped by verifying and correcting some scalar values in the damage formulas" + "\n" +
        "\n" +
        "I also give my thanks to The Balance, which provided me with a lot of knowleadge about the different" + "\n" +
        "jobs so I could implement them and also gave me access to resources like the Blackmage gear comparison" + "\n" +
        "spreadsheet which I used a lot when trying to better understand how damage computation work in this game." + "\n" +
        "================================================================================================================="
    )

    input("Press Enter to go back to the Main Menu : ")


def MergeFight():
    os.system('CLS') #clearing HUD
    print(
        "===================== MERGING TWO FIGHTS =====================" + "\n" 
    )

    cur_dir = os.getcwd()

    #the saved directory should be in that same folder

    saved_dir = cur_dir + "\\saved"

    saved_fight = os.listdir(saved_dir)
    number_saved_fight = len(saved_fight)
    parent_fight = ""
    child_fight = ""

    if number_saved_fight == 0: #No fight saved
        print("No saved fights were found. Hit any button to return to the main menu.")
        input("...")
        return
    else: #Saved fight
        print(
            "Select one of the saved fights as a parent (will merge into this one) : "+ "\n" + 
            "=========================================================="
            )
        for i in range(1,number_saved_fight+1):
            print(str(i) + " -> " + saved_fight[i-1])

        print("==========================================================")

        userInput = int(AskInput(number_saved_fight))

        parent_fight = saved_fight[userInput-1] #Selecting fight

    
        print(
            "Select one of the saved fights as a child (this one will be merged into) : "+ "\n" + 
            "=========================================================="
            )
        for i in range(1,number_saved_fight+1):
            print(str(i) + " -> " + saved_fight[i-1])

        print("==========================================================")

        userInput = int(AskInput(number_saved_fight))

        child_fight = saved_fight[userInput-1] #Selecting fight

        MergeFightBackEnd(saved_dir + "\\" + child_fight, saved_dir + "\\" + parent_fight, parent_fight)

        


def MainMenu():
    os.system('CLS') #clearing HUD
    #Welcome Message
    print(
    "===================== FFXIV Combat Simulator ======================" + "\n" + 
    "MAIN MENU (input what you want and press ENTER)" + "\n" + 
    "===================================================================" + "\n" + 
    "1- Simulate fight in code memory" + "\n" + 
    "2- Save fight in code memory"  + "\n" + 
    "3- Simulate a saved fight" + "\n" + 
    "4- Merge two saved fights" + "\n" + 
    "5- Import fight from FFLogs (Experimental)" + "\n" + 
    "6- Credits" + "\n" + 
    "7- Exit" + "\n" + 
    "==================================================================="
    )
    user_input = AskInput(7)

    if user_input == "1" : ExecuteMemoryCode(False) #Simulating
    elif user_input == "2": ExecuteMemoryCode(True) #Saving
    elif user_input == "3" : SimulateFightMemory()
    elif user_input == "4" : MergeFight() 
    elif user_input == "5" : ImportFight()
    elif user_input == "6" : Credits() #Closes program
    elif user_input == "7" : exit() #Closes program
    

#This python file will serve as a GUI for the time I do not have an actual GUI
if __name__ == "__main__" : 
    #working_dir = r" INSERT WORKING DIRECTORY HERE "
    #os.chdir(working_dir)
    while True : MainMenu() #Draws Main Menu

