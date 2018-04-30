import requests #imports necessary standard packages


class spark: #this creates the spark class

    
    def getMessage(self, userToken, roomId):

        URL = "https://api.ciscospark.com/v1/messages"
        ACCESS_TOKEN = userToken #"ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx" Access token is for Nicole's "Best" bot (Best@sparkbot@io)
        HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
        PARAMS = {"roomId" : roomId} #"Y2lzY29zcGFyazovL3VzL1JPT00vMmE3OTVlM2YtZjkwNS0zMGE3LTg4NTAtOGFkODY5N2IzOWM2" sample room ID

        response = requests.get(url=URL, headers=HEADERS, params=PARAMS)

        return response.text



    def postMessage(self, userToken, roomId, text):

        URL = "https://api.ciscospark.com/v1/messages"
        ACCESS_TOKEN = userToken #"ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx" #Access token is for "Best" bot Best@sparkbot@io; this the the Spark account user that will send the message
        HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
        #Sends "perfect" to ninunez@cisco.com
        #PAYLOAD = {"toPersonEmail" : "ninunez@cisco.com", "text" : "perfect"}
        PAYLOAD = {"roomId" : roomId, "text" : text}

        response = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)

        return response.text
