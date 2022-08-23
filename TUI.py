import os
from FFLogsAPIRequest import getAbilityList

from UI_backend import AskInput, ImportFightBackend, SaveFight, SimulateFightBackend


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
        "(If you have any question refer to the Help option in the main menu)" + "\n" +
        "The program does not check if the fight is valid, and will simply reuslt in a crash if it is not."
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
        "===================== CREDITS =====================" + "\n" + 
        "This program was made mainly by myself, but I was helped by a lot of friends" + "\n" +
        "and other people without whomst this project would not have been possible." + "\n" +
        "I listed here all those that helped with a short description of what they did." + "\n" +
        "I personally thank everyone here for the help they brought :)" + "\n" +
        "I will put their discord IDs in case you wish to contact them." + "\n" +
        "==============================================================================" + "\n" +
        "Pythagoras#6312 -> That's me! Did most of it" + "\n" +
        "ne0dym#7837 -> Helped me with code for Dark Knight" + "\n" +
        "Bri-kun#6539 -> Helped me with networking code and other FFLogsAPI related stuff" + "\n" +
        "javaJake#0001 -> Helped me with theoretical damage computation stuff" + "\n" +
        "Saint Germain#0280 -> Helped a bit with Monk code" + "\n" +
        "apollo#3810 -> Put me in contact with javajake and also provided some background code for working with FFLogsAPI" + "\n" +
        "Ikuni#2735 -> Helped by verifying and correcting some scalar values in the damage formulas" + "\n" +
        "\n" +
        "I also give my thanks to The Balance, which provided me with a lot of knowleadge about the different" + "\n" +
        "jobs so I could implement them and also gave me access to ressources like the Blackmage gear comparison" + "\n" +
        "spreadsheet which I used a lot when trying to better understand how damage computation work in this game." + "\n" +
        "=============================================================================="
    )

    input("Press Enter to go back to the Main Menu")


def MainMenu():
    os.system('CLS') #clearing HUD
    #Welcome Message
    print(
    "===================== DPS CALCULATOR PROGRAM =====================" + "\n" + 
    "MAIN MENU (input what you want and press ENTER)" + "\n" + 
    "======================================" + "\n" + 
    "1- Simulate fight in memory" + "\n" + 
    "2- Import fight from FFLogs" + "\n" + 
    "3- Create a fight"  + "\n" + 
    "4- Credits" + "\n" + 
    "5- Exit" + "\n" + 
    "======================================"
    )
    user_input = AskInput(5)

    if user_input == "1": SimulateFightMemory()
    elif user_input == "2" : ImportFight()
    elif user_input == "3" : CreateFight()
    elif user_input == "4" : Credits()
    elif user_input == "5" : exit() #Closes program
    

#This python file will serve as a GUI for the time I do not have an actual GUI
if __name__ == "__main__" : 
    while True : MainMenu() #Draws Main Menu


