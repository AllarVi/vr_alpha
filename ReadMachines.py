__author__ = 'Erko'

def readMachines(fileToBeRead):
    print "\nReading the machines into a list."
    text_file = open("Resources/" + fileToBeRead, "r")

    machinesList = [machinesList.strip(', \n') for machinesList in text_file.readlines()]
    print machinesList

    text_file.close()
    return machinesList


readMachines("machines.txt")