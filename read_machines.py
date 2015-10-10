__author__ = 'Erko'

def readMachines(fileToBeRead):
    text_file = open("Resources/" + fileToBeRead, "r")

    machinesList = [machinesList.strip().split(',') for machinesList in text_file.readlines()]

    text_file.close()
    return machinesList