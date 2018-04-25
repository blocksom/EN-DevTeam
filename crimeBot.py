"""
Date: 01 / 29 / 2018
Title: crimeBot
Author: Kyle T. Blocksom
Description: SparkBot capable of executing different crime-related commands

"""

from itty import *
import urllib2
import json

count = 0

# GET username and message from Spark Room at 'url' 
def sendSparkGET(url):
    # This class is an abstraction of a URL request
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    # Add another header to the request
    request.add_header("Authorization", "Bearer "+bearer)
    # Open the URL url
    contents = urllib2.urlopen(request).read()
    return contents

# POST message to Spark Room specified by 'url'      
def sendSparkPOST(url, data):
    # This class is an abstraction of a URL request
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    # Add another header to the request
    request.add_header("Authorization", "Bearer "+bearer)
    # Open the URL url.
    contents = urllib2.urlopen(request).read()
    return contents
    
# Main function 
@post('/')
def index(request):
    global count
    # Deserialize 'request.body' to a Python object
    webhook = json.loads(request.body)
    print webhook['data']['id']
    # method call
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)

    # Initialize incoming message to NULL
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        # Decode incoming message and sender's username
        in_message = result.get('text', '').lower()
        username = result.get('personEmail', '').lower()
        in_message = in_message.replace(bot_name, '')

        # Condition checks
        if 'crimestoppers' in in_message or "whoareyou" in in_message:
            msg = "We're crime stoppers! Nice to meet you " + username
        elif 'statement' in in_message:
            message = result.get('text').split('statement')[1].strip(" ")
            if len(message) > 0:
                msg = "You reported: '{0}'".format(message)
            else:
                msg = "Your report was empty..."
        elif 'signal' in in_message:
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": crime_signal})
        elif 'report' in in_message:
            city = result.get('text').split('report')[1].replace(" ", "")
            crime_report = "https://spotcrime.com/{0}".format(city)
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": crime_report}) 
        elif 'help' in in_message:
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": helper}) 
    if msg != None:
        print msg
        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

# Global Variables
bot_email = "kyleBot@sparkbot.io"
bot_name = "crimeBot"
bearer = "OGFiMTZhZDctMjZhNC00Yzc1LWEwODYtOGVkMTk0YzBkZGZkNGRhZTlkZjAtMDcz"
crime_signal  = "https://78.media.tumblr.com/tumblr_m4y3gp1IuB1r5lshvo1_500.gif"
helper = "Hello! We are the crime stoppers bot. How can we help?\n\nOur commands include:\n\nhelp: shows command details\ncrimestoppers -or- whoareyou: personalized crimestoppers introduction\nstatement: write a report and have it read back to you\nsignal: receive the crimestoppers signal\nreport [city]: receive crime report for specified city\n"

run_itty(server='wsgiref', host='0.0.0.0', port=8080)
