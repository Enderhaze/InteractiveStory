from location import LocationClass
from items import ItemsClass
import json
from types import SimpleNamespace
import time
import sys

def slowType(text, sleepTime = 0.07):
    for l in text + '\n':
      sys.stdout.write(l)
      sys.stdout.flush()
      time.sleep(sleepTime)
    print("")

dataFile = open("data.json")
data = json.load(dataFile, object_hook=lambda d: SimpleNamespace(**d))
dataFile.close()

itemsDict = {}
for item in data.Items:
    name = item.name
    desc = item.desc
    takeable = item.takeable
    actions = item.actions
    newItem = ItemsClass(name, desc, takeable, actions)
    itemsDict[name] = newItem

locationDict = {}
for location in data.Location:
    name = location.name
    desc = location.desc
    items = location.items
    places = location.places
    locationPlace = LocationClass(name, desc, items, 0, places)
    locationDict[name] = locationPlace


inventory = []
 
clock = 0

slowType("This game is still a work in progress, so not everything is complete yet. \nYou can still explore places and learn about the world I'm building, but there isn't much else you can do. \nI hope you enjoy your time playing this game!")
slowType("This is also an (almost) open response game, meaning that there isn't going to be two choices given to you for you to choose from. You can do basically whatever you want, as long as there is a command for it.")
slowType("Command list: move to [place] - the place is an area you can move to. Specific places are linked to the area, so you have to remember where you moved to get back to previous places. \ntake [item] - Items are specific to area, doing this will put an item in your inventory. \ndrop [item] - Same as take, but instead you remove the item from your inventory. \n[action] [item] - Saying an action you want to do for an item, like 'examine sword'. Actions are specific for each item. \ninventory - Print out your inventory. \nitems - Print out the items in the area. \nlook - Print out the description of the place again. \ncommands - Print out the commands list. \nquit - Quit the game.")

slowType("Flowers wave in the light spring breeze as the sun dips below the horizon.") 
slowType("Wiping your hands on your trousers, you heave a sigh of relief as you look at the last piece of the statue you were carving.") 
slowType("Finally, after years of gathering resources and excruciating work, you finished.") 
slowType("You walk back towards your house and reach the front door.")
slowType("To the left of you, there's a path leading into a forest. You remember that you have a garden at the back of your house.")

#storing the location of where you are
locationStorage = locationDict["clearing"]
    
while True:
    userInput = input(">>> ")
    words = userInput.lower().split()
    if words[0] == "move":
        newLocation = words[2]
        #change locations
        if locationStorage.name == newLocation:
            slowType("You're already here or something like that")
            continue
        foundLocation = None
        for place in locationStorage.places:
            if place == newLocation:
                foundLocation = place
                locationStorage = locationDict[place]
                break
        if foundLocation == None:
            slowType("I do not recognize the input")
        else:
            slowType("You are now at the " + locationStorage.name)
            if locationStorage.timesVisited == 0:
                slowType(locationStorage.desc)
            locationStorage.timesVisited += 1

            clock += 1

    elif words[0] == "take":
        #take an item
        takeItem = words[1]

        foundItem = None
        for item in locationStorage.items:
            if item == takeItem:
                foundItem = itemsDict[item]
                break
        if foundItem == None:
            slowType("I do not recognize the input")
        elif not foundItem.takeable:
            slowType("You can't take this item")
        else:
            locationStorage.items.remove(takeItem)
            inventory.append(foundItem)
            slowType("You picked up the " + foundItem.name)
            slowType("You have a " +
            ", ".join([item.name for item in inventory])
            + " in your inventory")
            clock += 1

    elif words[0] == "drop":
        #drop an item
        dropItem = words[1]

        foundItem = None

        for item in inventory.items:
            if item == dropItem:
                foundItem = itemsDict[item]
                break
        if foundItem == None:
            slowType("I do not recognize the input")
        else:
            locationStorage.items.append(dropItem)
            inventory.remove(foundItem)
            slowType("You have dropped the " + foundItem.name)
            if inventory == []:
                slowType("You have nothing in your inventory")
            
            else:
                slowType("You have a " +
                ", ".join([item.name for item in inventory])
                + " in your inventory")
            clock += 1

    elif words[0] == "look":
        #slowType out the description of the current location again
            slowType(locationStorage.desc)

    elif words[0] == "items":
            slowType("There's a " 
            ", ".join([item.name for item in locationStorage.items])
            + " here")

    elif words[0] == "inventory":
            #slowType inventory
            if inventory == []:
                slowType("You have nothing in your inventory")
            
            else:
                slowType("You have " +
                ", ".join([item.name for item in inventory])
                + " in your inventory")

    elif words[0] == "commands":
        #print the command list
        slowType("Command list: move to [place] - the place is an area you can move to. Specific places are linked to the area, so you have to remember where you moved to get back to previous places. \ntake [item] - Items are specific to area, doing this will put an item in your inventory. \ndrop [item] - Same as take, but instead you remove the item from your inventory. \n[action] [item] - Saying an action you want to do for an item, like 'examine sword'. Actions are specific for each item. \ninventory - Print out your inventory. \nitems - Print out the items in the area. \nlook - Print out the description of the place again. \ncommands - Print out the commands list. \nquit - Quit the game.")

    elif words[0] == "talk":
        #talk to npc
        pass
               
    elif words[0] == "quit":
        break

    else:
        actionItem = words[1]
        action = words[0]

        foundItem = None
        for item in locationStorage.items:
            if item.name == actionItem:
                foundItem = item
                break
        if foundItem == None:
            slowType("I do not recognize the input")
        elif action in foundItem.actions:
            action = foundItem.actions[action]
            slowType(action)

            clock += 1
        else:
            slowType(f"You can't {action} the {actionItem}")

    if clock == 50:
        if locationDict["forest"]:
            slowType("The forest has gone to sleep.")
        if locationDict["clearing"]:
            slowType("Glowing orbs swirl around in the pale light.")
    if clock == 165:
        slowType("The moon begins it's descent. \nYou can start to see hints of orange on the east horizon. \nIt is almost dawn.")
    if clock == 200:
        if locationDict["garden"].timesVisited == 0:
            slowType("As the sun rises in the sky, everything around you turns to stone. \nSlowly, the stone creeps towards you... \nCloser... \nAnd closer... \nAnd closer it creeps until it starts covering your legs. \nThe stone slowly moves up your body until you are incased in it. \nEverything turns to black as the last bit of light fades. \nYou wake up with a start in a clearing. \nFlowers wave in the light spring breeze as the sun dips below the horizon. \nWiping your hands on your trousers, you heave a sigh of relief as you look at the last piece of the statue you were carving. \nBut...strange. There seems to be another one. \nDid you carve one and forget? \nShrugging your shoulders, you walk back towards your house and reach the front door. \nTo the left of you, there's a path leading into a forest. You remember that you have a garden at the back of your house.")
        else:
            slowType("You stand at the edge of the clearing you started in. \nYou see the sun starting it's ascent, the water glittering in the first few rays of light. \nYou take a deep breath...and smash the glass.")
            slowType("The End", 1)