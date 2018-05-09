#!/usr/bin/env python
# -*- coding: utf-8 -*- 

__author__ = "Kyle Blocksom, Nicole Nuñez, and Paul Burke"
__credits__ = ["Michael Castellana", "Reid Delaney"]
__version__ = "1.0"
__email__ = "kblockso@cisco.com, ninunez@cisco.com, paulburk@cisco.com"
__status__ = "Development"

"""

WARNING:
This script is meant for educational purposes only.
Any use of these scripts and tools is at
your own risk. There is no guarantee that
they have been thoroughly tested in a
comparable environment and we are not
responsible for any damage or data loss
incurred with their use.

DESCRIPTION:
APIC-EM/Spark Integration

Take query from Spark and map this to a REST API call.
Display queried information in consumable/readable manner using Spark.

"""

import requests, json # Imports necessary standard packages
from APIC import apic # Imports 'apic' class from 'APIC.py' for APIC-EM methods
from SPARK import spark # Imports 'spark' class from 'SPARK.py' for Spark methods
from itty import * # Imports itty, which facilitates ngrok communication

# Global variables
APIC = 'devnetapi.cisco.com/sandbox/apic_em' # APIC-EM IP address
USERNAME = 'devnetuser' # APIC-EM username
PASSWORD = 'Cisco123!' # APIC-EM password

# Invoke getTicket method to generate unique service ticket,
# necessary for making any API calls to APIC-EM Controller
newTicket = apic().getTicket(APIC, USERNAME, PASSWORD)

# Main function 
@post('/') # The code within 'index(request)' is executed whenever POST API is sent to ngrok server
def index(request):

    # Manipulates POST to retreive necessary information from SPARK using GET
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
        
        # Help function
        if '/help' in in_message:
            msg = ("You asked for help? Let me explain what I can do:\n\n"
                   "I am APIC-EM Bot, and I can help you interact with your favorite Campus Network Controller via Spark! For instance:"
                   "\n- Send '/devices' to see information about active network devices."
                   "\n- Send '/hosts' to see information about attached hosts."
                   "\n- Send '/vlans' to see information about active VLANs.\n\n"
                   "Contact paulburk@cisco.com for support, questions, or friendly feedback.")

        # Available query option: getVlans method from apic class
        elif '/vlans' in in_message:
            response = apic().getVlans(APIC, newTicket)
            string = 'Here are the active VLANs on your network:\n'
            msg = string + response

        # vailable query option: getDevices method from apic class
        elif '/devices' in in_message:
            response = apic().getDevices(APIC, newTicket)
            string = 'Here are the active devices on your network:\n'
            msg = string + response

        # Available query option: getVlans method from apic class + Spark removes redundant spaces
        # For sake of proper table spacing, '&nbsp;' is used to hard code spacing
        elif '/hosts' in in_message:
            response = apic().getHosts(APIC, newTicket)
            string = 'Here are the attached hosts on your network:'
            msg = string + response

        else:
            # Message returned in case apic-em bot does not understand query
            msg = "Uh oh! Looks like I didn't quite understand that. Try asking for '/help' to see what I can do!"            
    
    # Posts bot response to Spark room
    if msg != "":
        print (msg)
        spark().sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg}, bearer)
    return "true"

# Global Variables
bot_email = "apic-embot@sparkbot.io"
bot_name = "APIC-EM Bot"
bearer = "ZTkwMTFhZTctMjFkMy00ZjRiLWFmNzQtMjZkMjRkYTQxYjM1ZjRlNTg1ZDUtZGIz"

run_itty(server='wsgiref', host='0.0.0.0', port=8080)