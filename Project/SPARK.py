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
