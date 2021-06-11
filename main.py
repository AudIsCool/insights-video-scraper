#Get QL stuff
import json
import os
import graphql

import urllib.request
import traceback

"""
    Get the user's team
"""
print("[ -- Getting your teams -- ]")
rawTeamList = graphql.getAllTeams()

#Filter to names and ids
teamList = []
for teams in rawTeamList["data"]["queryTeams"]["teamEdges"]: 
    teamList.append({
        "id": teams["team"]["id"],
        "name": teams["team"]["name"]
    })


#Get what team they want
print("[ -- Select the team you'd like to look into -- ]")

index = 0
for teams in teamList: 
    print("\t[{}] {}".format(index, teams["name"]))
    index += 1

teamIndex = -1
while teamIndex == -1:
    teamIndex = int(input("[Number of the team you want]: "))

    if teamIndex < 0 or teamIndex > (len(teamList) - 1):
        teamIndex = -1

        print("[ -- The chosen team must be a number between 0 and {}".format((len(teamList) - 1)))


"""
    Get the user's channel
"""
chosenTeam = teamList[teamIndex]
print("[ -- Getting channels for {} -- ]".format(chosenTeam["name"]))

#Get channels
rawChannelList = graphql.getChannels(chosenTeam["id"])

channelList = []
for channels in rawChannelList["data"]["team"]["queryDivisions"]["divisions"]:
    channelList.append({
        "id" : channels["id"],
        "name": channels["name"]
    })


print("[ -- Select the the channel to open  -- ]")
index = 0
for channels in channelList: 
    print("\t[{}] {}".format(index, channels["name"]))
    index += 1


channelIndex = -1
while channelIndex == -1:
    channelIndex = int(input("[Number of the team you want]: "))

    if channelIndex < 0 or channelIndex > (len(channelList) - 1):
        channelIndex = -1

        print("[ -- The chosen channel must be a number between 0 and {}".format((len(channelList) - 1)))


#Done
chosenChannel = channelList[channelIndex]

"""
    Get the vods in channel 
"""
print("[ -- Getting your vods for channel {} -- ]".format(chosenChannel["name"]))
rawVods = graphql.getVods(chosenChannel["id"])


vodList = rawVods["data"]["directory"]["queryVideos"]["videos"]

#Print them out
print("[ -- Select the vods you'd like to download :D -- ]")
index = 0
for channels in vodList: 
    print("\t[{}] {}".format(index, channels["name"]))
    index += 1


print("\n[ -- List out your vods to download, in a comma seperated list like below -- ]")
print("[Vods to take in]: 1,2,3,6,4\n")

#Get input
validInput = False 

inputInts = None

#Get vod list
while validInput != True:
    inputStr = str(input("[Vods to take in]: ")) #Just so we can allow people to add random spaces 

    #Strip spaces, and split
    while inputStr.find(" ") != -1:
        inputStr = inputStr.replace(" ", "")

    #Split
    stringList = inputStr.split(",")

    #Convert to int
    validIntList = True
    intList = []


    for nums in stringList: 
        try: 
            intList.append(int(nums))  
        
        except: 
            print(
                "[ -- {} was not a valid number between 0 and {} --]"
                .format(nums, (len(vodList) - 1) )
            )
            
            validIntList = False
            break


    #Assuming we have our intlist, valid, if not repeat
    if validIntList: 
        validInput = True
        inputInts = intList


#Make the download folder we need
if os.path.isdir("./downloads") != True:
    os.mkdir("./downloads")

#Grab vod list
for vodInts in inputInts: 
    #Get vod
    vod = vodList[vodInts]
    vodName = "./downloads/{}.mp4".format(vod["name"])

    #If it's remote
    if "streamUrl" not in vod or vod["streamUrl"] == None:
        print("{} | {} couldn't be downloaded since it's a remote video".format(vodInts, vod["name"]))


    #If not, download
    else: 
        print("[*] Downloading {} | {} ".format(vodInts, vod["name"]))

        try: 
            file = urllib.request.urlopen(vod["streamUrl"]) 
            fileSize = file.headers.get("Content-Length")
            
            downloaded = 0
            updateInterval = 0

            #Download loop
            while 1: 
                #Read Data
                data = file.read(4096)
                downloadString = "\t[*] Downloaded {}% of {} GB".format(round(downloaded / float(fileSize), 4), str(int(fileSize) / 100000000))

                #If we're done here
                if not data: 
                    print(downloadString, flush=True, end='\r')
                    break 
                
                #Handle download info
                downloaded += len(data)
                updateInterval += len(data)

                if updateInterval > 1000000:
                    updateInterval = 0
                    print(downloadString, flush=True, end='\r')

                #Write the data to the file
                with open(vodName, "ab") as fileToWrite: 
                    fileToWrite.write(data)

            #If we fully finished
            print("[*] Done downloading {} | {} ".format(vodInts, vod["name"]))

        except Exception as error: 
            print("[-] Had error downloading {}, said \n{}".format(vodName, traceback.print_exc()))
    



print("[ -- Done probably idk -- ]")


