"""
This file contains the logic of the Gear Solver.

The algorithm requires one Fight Object that will be used to compute the DPS. The algorithm will use
the pre-baked simulation in order to quickly simulate the DPS given some gear configuration.
One list of Gear from which to search, the space of materias that are available, etc.

For now the BiS Solver will only work if the Fight has one player variable, meaning it can only solve the BiS for one player.

"""

def BiSSolver(Fight, GearSpace : dict, PlayerIndex : int):
    """
    Finds the BiS of the player given a Gear search space and a Fight.
    Fight -> Fight object.
    GearSpace : dict -> Dictionnary filled with the different gear pieces the algorithm can search through.
    PlayerIndex : int -> Index of the player for which the user wants to optimize the gearset. Must be the index of the player
                         in the Fight.PlayerList.
    """

    