import requests, json

requests.packages.urllib3.disable_warnings()

class apic:

    def getTicket(self, ip, username, password):
        url = "https://" + ip + "/api/v1/ticket"
        header = {"Content-Type": "application/json"}
        body = {"username": username,"password": password}
    
        response = requests.post(url, data=json.dumps(body), headers=header).json()
    
        ticket = response["response"]["serviceTicket"]
    
        return ticket

    def getVlans(self, ip, ticket):
        url = "https://" + ip + "/api/v1/vlan/vlan-names"
        header = {"Content-Type": "application/json", "X-Auth-Token": ticket}
    
        response = requests.get(url, headers=header).json()
    
        return response
