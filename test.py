from itty import *
import urllib2
import json

# GET username and message from Spark Room at 'url' 
def sendSparkGET(url):
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

# POST message to Spark Room specified by 'url'      
def sendSparkPOST(url, data):
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
    
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
        if '/help' in in_message:
            msg = ("You asked for help? Let me explain what I can do:\n\n"
                   "I am APIC-EM Bot, and I can help you interact with your SDN Controller via Spark!\n"
                   "For instance, send '/vlans' to see information about active VLANs.\n\n"
                   "Contact paulburk@cisco.com for support, questions, or friendly feedback.")

        elif '/vlans' in in_message:
            msg = "VLAN info..."
        else:
            #Message returned in the case of apic-em bot not understanding query
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

run_itty(server='wsgiref', host='0.0.0.0', port=8080)
