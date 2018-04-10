import requests, json #imports necessary standard packages

requests.packages.urllib3.disable_warnings()

class apic: #this creates the apic class

    # This method generates an API Post call to generate a unique service
    # ticket, necessary for making any APIC-EM Get requests
    def getTicket(self, ip, username, password):

        # These three variables define the necessary inputs to make an API
        # Post call
        url = "https://" + ip + "/api/v1/ticket"
        header = {"Content-Type": "application/json"}
        body = {"username": username,"password": password}

        # This sets the 'response' variable to the output of the API call,
        # formatted in json, leveraging the 'post' method of the requests
        # standard package
        response = requests.post(url, data=json.dumps(body), headers=header).json()

        # This parses the response into just the relevant value, the ticket
        ticket = response["response"]["serviceTicket"]
    
        return ticket

    # This method generates and API Get call to receive the VLANs operating
    # on the network
    def getVlans(self, ip, ticket):

        # These two variables define the necessary inputs to make an API
        # Get call, leveraging the service ticket as authentication
        url = "https://" + ip + "/api/v1/vlan/vlan-names"
        header = {"Content-Type": "application/json", "X-Auth-Token": ticket}

        # This sets the 'response' variable to the output of the API call,
        # formatted in json, leveraging the 'get' method of the requests
        # standard package
        response = requests.get(url, headers=header).json()
    
        return response
