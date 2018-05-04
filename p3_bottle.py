import json, requests
import bottle
from bottle import *

def sendSparkGET(url):
    headers = {"Content-type" : "application/json; charset=utf-8",
               "Authorization" : "Bearer "+bearer}
    request = requests.get(url=url, headers=headers)

    return request.text

def sendSparkPOST(url, data):
    headers = {"Content-type" : "application/json; charset=utf-8",
               "Authorization" : "Bearer "+bearer}
    request = requests.post(url=url, json=data, headers=headers)

    return request.text

# Main function 
@post('/')
def index(request):
    webhook = json.loads(request.body)
    print (webhook['data']['id'])
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    print (result)
    msg = ""
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        username = result.get('personEmail', '').lower()
        in_message = in_message.replace(bot_name, '')
        
        #Help function
        if '\help' in in_message:
            msg = ("You asked for help? Let me explain what I can do:\n\n"
                   "I am APIC-EM Bot, and I can help you interact with your SDN Controller via Spark!\n"
                   "For instance, send '\vlans' to see information about active VLANs.\n\n"
                   "Contact paulburk@cisco.com for support, questions, or friendly feedback.")

        elif '\vlans' in in_message:
            msg = "VLAN info..."
        else:
            #Message returned in the case of tweetbot not understanding query
            msg = "Uh oh! Looks like I didn't quite understand that. Try asking for '\help' to see what I can do!"            
    
    #This posts the bot response to the room
    if msg != "":
        print (msg)
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

# Global Variables
bot_email = "apic-embot@sparkbot.io"
bot_name = "APIC-EM Bot"
bearer = "ZTkwMTFhZTctMjFkMy00ZjRiLWFmNzQtMjZkMjRkYTQxYjM1ZjRlNTg1ZDUtZGIz"

run(server='wsgiref', host='0.0.0.0', port=8080)
