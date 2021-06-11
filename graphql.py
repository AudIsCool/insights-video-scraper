import os
import json
import requests

#Insights info
insightsGQL = "https://insights.gg/graphql"

#Insert your cookie info here
SESSION_COOKIE = os.environ.get("SESSION_COOKIE")
TOKEN_COOKIE = os.environ.get("TOKEN_COOKIE")

#Check to see if cookies vars are there
if SESSION_COOKIE == None or TOKEN_COOKIE == None: 
    raise ValueError("SESSION_COOKIE or TOKEN_COOKIE missing from env vars D:")


#Fetch GQL 
graphQlContainer = None

try: 
    with open("graphql.json", "r") as file: 
        graphQlContainer = json.loads(str(file.read()))

except Exception as error: 
    raise ValueError("graphql.json was either missing or improperly formatted.\n{}".format(error))



#setup fancy requests
def getAllTeams():
    return request("GetTeamsQuery", {
        "limit": 1000
    })
    
def getChannels(teamId):
    return request("GetTeamDivisionsQuery", {
        "teamId": teamId,
        "limit": 1000
    })


def getFolders(channelId): 
    return request("GetTeamDivisionsQuery", {
        "directoryId": channelId,
        "limit": 1000
    })

def getVods(channelId): 
        return request("GetTeamDirectoryVideosQuery", {
        "directoryId": channelId,
        "limit": 1000
    })


#Layout base request
def request(requestName, variables):
    #Get request
    requestJson = graphQlContainer[requestName]

    #Insert variables
    requestJson["variables"] = variables

    #Set cookies
    cookieDict = {
        "__akshon__sessionv2": SESSION_COOKIE,
        "__akshon__token": TOKEN_COOKIE
    }

    #Send request
    gqlResposne = requests.post(
        insightsGQL,

        cookies = cookieDict,
        json = requestJson
    )

    if gqlResposne.status_code == 200: 
        return gqlResposne.json()
    
    else: 
        raise RuntimeError(
            "Failed to get {} with variables {}, said \n {}"
            .format(requestName, json.dumps(variables, indent=4), gqlResposne.content)
        )

