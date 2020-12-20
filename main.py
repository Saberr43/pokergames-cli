import sys
import requests
import json
import difflib
# from difflib import get_close_matches 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printFail(msg):
    print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")

def printGood(msg):
    print(f"{bcolors.OKGREEN}{msg}{bcolors.ENDC}")

def printInfo(msg):
    print(f"{bcolors.INFO}{msg}{bcolors.ENDC}")

def getCloseMatchesICase(word, possibilities, *args, **kwargs):
    """ Case-insensitive version of difflib.get_close_matches """
    lword = word.lower()
    lpos = {p.lower(): p for p in possibilities}
    lmatches = difflib.get_close_matches(lword, lpos.keys(), *args, **kwargs)
    return [lpos[m] for m in lmatches]

def printVenueInfo(vn,gmsRunning):
    if len(gmsRunning) == 0:
        printInfo("No games currently running at " + vn["name"])
        return

    gamesDict = {}
    for cgm in gmsRunning["currentgames"]:
        if "numberoftables" in cgm: # if number is present in dict
            gamesDict.update({cgm["unparsedname"] : (cgm["numberoftables"],0)}) #{nameOfGame : (numberOfTables, waitlist=0)}, waitlist value will get added later

    if "waitlistgames" in gmsRunning: # if there is a waitlist
        for wlgm in gmsRunning["waitlistgames"]:
            if "numberofwaitlist" in wlgm: # if number is present in dict

                waitlistGameName = wlgm["unparsedname"]
                if waitlistGameName in gamesDict: # if the game is in our dict (the game has tables going)
                    gamesDict[waitlistGameName] = (gamesDict[waitlistGameName][0], wlgm["numberofwaitlist"])
                else: # else add a new entry in the gamesDict 
                    gamesDict.update({waitlistGameName : (0, wlgm["numberofwaitlist"])}) #{nameOfGame : (0, numberOfWaitlist)}, no tables running since the game name wasn't in the gameDict

    # print venue name
    print(f"{bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKGREEN}{vn['name']}: {vn['phone']}{bcolors.ENDC}\n")

    # print current games and waitlist values
    for gameKey in gamesDict:
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}{gameKey}:{bcolors.ENDC}")
        print(f"  {bcolors.INFO}tables:{gamesDict[gameKey][0]}")
        print(f"  {bcolors.INFO}waitlist:{gamesDict[gameKey][1]}")


def main():
    if len(sys.argv) > 1:
        nameArgs = sys.argv[1:]
        venueName = " ".join(nameArgs)

        response = requests.get("http://pokernotify.com/input_notif/venues/all")
        if response.status_code != 200:
            printFail("non-200 from api " + response.status_code)
            return

        venues = json.loads(response.text)

        apiVenueNames = []
        matchingVenue = None
        for vn in venues: 
            apiVenueNames.append(vn["name"])           
            if vn["name"].lower().strip() == venueName.lower():
                matchingVenue = vn

        if matchingVenue == None:
            printFail("No venues by the name '" + venueName + "' found, did you mean " + str(getCloseMatchesICase(venueName, apiVenueNames, 3, 0.4)) + "?")
            return
        
        gmsRunningResp = requests.post("http://pokernotify.com/input_notif/getcurrentgames", str(matchingVenue["venuerow"])) 
        if gmsRunningResp.status_code != 200:
            printFail("non-200 from api " + response.status_code)
            return

        gmsRunning = json.loads(gmsRunningResp.text)
        
        printVenueInfo(matchingVenue, gmsRunning)

    else:
        printInfo("Please pass in venue name")


if __name__ == "__main__":
    main()