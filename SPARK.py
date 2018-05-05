# The Spark class defines 3 basic methods that can be used to 1) retrive the last room that a specific Spark bot was added to, 2) retrive the last message in that room that the bot was 
# @mentioned in, and 3) post a message into that room on behalf of the bot

# Please direct any questions to ninunez@cisco.com

import requests #imports necessary standard packages

class spark: #this creates the spark class

    
    def getRoom(self, userToken):
        #Returns the room ID of only the last room that the bot was added to

        URL = "https://api.ciscospark.com/v1/rooms"
        ACCESS_TOKEN = userToken 
        HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
        PARAMS = {"type" : "group", "max" : "1"}

        response = requests.get(url=URL, headers=HEADERS, params=PARAMS)
        response = response.text

        #Finds location of beginning of room ID in response by searching for keyword
        beg = "id"
        location_beg = response.find(beg)
        length_beg = len(beg) #print (vit)
        beg = location_beg + length_beg + 3

        #Finds location of end of room ID in response by searching for keyword
        end = "title"
        location_end = response.find(end)
        end = location_end - 3

        #Saves room ID to variable
        roomId = response[beg : end]
        
        return roomId

    
    def getMessage(self, userToken, roomId):
        #Returns only the last message that the bot was @mentioned in

        URL = "https://api.ciscospark.com/v1/messages"

        ACCESS_TOKEN = userToken
        HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
        ROOMID = roomId
        PARAMS = {"roomId" : ROOMID, "max" : "1", "mentionedPeople" : "me"}

        response = requests.get(url=URL, headers=HEADERS, params=PARAMS)
        response = response.text

        #Finds location of beginning of room ID by searching for keyword
        beg = "text"
        location_beg = response.find(beg)
        length_beg = len(beg) #print (vit)
        beg = location_beg + length_beg + 3

        #Finds location of end of room ID by searching for keyword
        end = "personId"
        location_end = response.find(end)
        end = location_end - 3

        #saves room ID to variable
        message = response[beg : end]

        print (message)


    def postMessage(self, userToken, roomId, text):
        #Posts message on behalf of the bot

        URL = "https://api.ciscospark.com/v1/messages"
        ACCESS_TOKEN = userToken 
        HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
        PAYLOAD = {"roomId" : roomId, "text" : text}

        response = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)

