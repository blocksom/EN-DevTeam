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

Leverage Spark API to display queried APIC-EM information.

"""

import json, urllib2 #imports necessary standard packages

class spark: #this creates the spark class

    # GET username and message from Spark Room at 'url' 
    def sendSparkGET(self, url, bearer):
        request = urllib2.Request(url,
                                  headers={"Accept" : "application/json",
                                           "Content-Type":"application/json"})
        request.add_header("Authorization", "Bearer "+bearer)
        contents = urllib2.urlopen(request).read()
        return contents

    # POST message to Spark Room specified by 'url'      
    def sendSparkPOST(self, url, data, bearer):
        request = urllib2.Request(url, json.dumps(data),
                                  headers={"Accept" : "application/json",
                                           "Content-Type":"application/json"})
        request.add_header("Authorization", "Bearer "+bearer)
        contents = urllib2.urlopen(request).read()
        return contents