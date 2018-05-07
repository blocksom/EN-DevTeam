import requests, json #imports necessary standard packages
from APIC import apic #imports 'apic' class from 'APIC.py' for APIC-EM methods
from SPARK import spark
from itty import *

#requests.packages.urllib2.disable_warnings()

# Defines global variables
APIC = 'devnetapi.cisco.com/sandbox/apic_em'
USERNAME = 'devnetuser'
PASSWORD = 'Cisco123!'

# This calls on the getTicket method to generate a unique service ticket,
# necessary for making any API calls to the APIC-EM
newTicket = apic().getTicket(APIC, USERNAME, PASSWORD)

# Main function 
@post('/')
def index(request):
    webhook = json.loads(request.body)
    print (webhook['data']['id'])
    result = spark().sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']), bearer)
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
                   "I am APIC-EM Bot, and I can help you interact with your favorite Campus Network Controller via Spark! For instance:"
                   "\n- Send '/devices' to see information about active network devices."
                   "\n- Send '/hosts' to see information about attached hosts."
                   "\n- Send '/vlans' to see information about active VLANs.\n\n"
                   "Contact paulburk@cisco.com for support, questions, or friendly feedback.")

        elif '/vlans' in in_message:
            response = apic().getVlans(APIC, newTicket)
            string = 'Here are the active VLANs on your network:\n'
            msg = string + response
            
        elif '/devices' in in_message:
            response = apic().getDevices(APIC, newTicket)
            string = 'Here are the active devices on your network:\n'
            msg = string + response

        # I know this one looks weird, Spark removes redundant spaces, and I was playing around with &nbsp;
        elif '/hosts' in in_message:
            response = apic().getHosts(APIC, newTicket)
            string = 'Here are the attached hosts on your network:'
            string = string + '\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MAC Address&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;IP Address&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;VLAN&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Connection'
            msg = string + response

        else:
            # Message returned in the case of apic-em bot not understanding query
            msg = "Uh oh! Looks like I didn't quite understand that. Try asking for '/help' to see what I can do!"            
    
    # This posts the bot response to the room
    if msg != "":
        print (msg)
        spark().sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg}, bearer)
    return "true"

# This will later live under a lengthy 'if' statement depending on what
# request the user has made in the body of their Spark message, but presently
# it's an example of an API call and returns the json response

# Global Variables
bot_email = "apic-embot@sparkbot.io"
bot_name = "APIC-EM Bot"
bearer = "ZTkwMTFhZTctMjFkMy00ZjRiLWFmNzQtMjZkMjRkYTQxYjM1ZjRlNTg1ZDUtZGIz"

run_itty(server='wsgiref', host='0.0.0.0', port=8080)
