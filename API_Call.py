import requests, json
from APIC import apic

requests.packages.urllib3.disable_warnings()

APIC = 'devnetapi.cisco.com/sandbox/apic_em'
USERNAME = 'devnetuser'
PASSWORD = 'Cisco123!'
    
newTicket = apic().getTicket(APIC, USERNAME, PASSWORD)

msg = apic().getVlans(APIC, newTicket)
print(msg)
print(type(msg["response"]))
