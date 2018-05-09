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

Leverage APIC-EM API to perform defined set of queries.

"""

import requests, json # Imports necessary standard libraries

class apic: # Creates the apic class

    # Generates API Post call to generate unique service ticket
    # necessary for making any APIC-EM Get requests
    def getTicket(self, ip, username, password):

        # JSON inputs for API Post call
        url = "https://" + ip + "/api/v1/ticket"
        header = {"Content-Type": "application/json"}
        body = {"username": username,"password": password}

        # Sets 'response' variable to JSON formmated output of API call
        # leveraging 'post' method of requests library
        response = requests.post(url, data=json.dumps(body), headers=header).json()

        # Parses response into relevant value (i.e tservice icket)
        ticket = response["response"]["serviceTicket"]
        
        return ticket

    # Ggenerates API Get call to receive network VLANs
    def getVlans(self, ip, ticket):

        # Generates API Get call, leveraging service ticket as authentication
        url = "https://" + ip + "/api/v1/vlan/vlan-names"
        header = {"Content-Type": "application/json", "X-Auth-Token": ticket}

        # Sets 'response' variable to JSON formmated output of API call
        # leveraging 'get' method of requests library 
        # and formatting text into consumable bullet points
        response = requests.get(url, headers=header)
        parsed = json.loads(response.text)
        apicList = parsed['response']
        msg = ''
        for obj in apicList:
                msg+='\n- '+obj
        return msg

    # Generates API Get call to receive network devices
    def getDevices(self, ip, ticket):

        # Generates API Get call, leveraging service ticket as authentication
        url = "https://" + ip + "/api/v1/topology/custom"
        header = {"Content-Type": "application/json", "X-Auth-Token": ticket}

        # Sets 'response' variable to JSON formmated output of API call
        # leveraging 'get' method of requests library 
        # and formatting text into consumable bullet points
        response = requests.get(url, headers=header)
        parsed = json.loads(response.text)
        apicList = parsed['response']['nodes']
        msg = ''
        for obj in apicList:
            if obj['nodeType'] == "device":
                msg+='\n\n'+'**'+obj['label']+'**: \n- Platform: '+obj['deviceType']+'  \n- IP: '+obj['ip']
        return msg

    # Generates API Get call to receive network hosts
    def getHosts(self, ip, ticket):

        # Generates API Get call, leveraging service ticket as authentication
        url = "https://" + ip + "/api/v1/host"
        header = {"Content-Type": "application/json", "X-Auth-Token": ticket}

        # Sets 'response' variable to JSON formmated output of API call
        # leveraging 'get' method of requests library 
        # and formatting text into consumable table
        response = requests.get(url, headers=header)
        parsed = json.loads(response.text)
        apicList = parsed['response']

        msg = '   \n'+'%25s%25s%25s%25s' % ('MAC Address', 'IP Address', 'VLAN', 'Connection')
        for obj in apicList:
            msg+='  \n'+'%25s%25s%25s%25s' % (obj['hostMac'], obj['hostIp'], obj['vlanId'], obj['hostType'])
        return msg
    
    # Remove duplicate elements
    def removeDup(self, duplicate):
       final_list = []

       # Iterate through list and build new list of unique objects
       for num in duplicate:
          if num not in final_list:
             final_list.append(num)

       return final_list