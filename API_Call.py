import requests, json #imports necessary standard packages
from APIC import apic #imports 'apic' class from 'APIC.py' for APIC-EM methods

requests.packages.urllib3.disable_warnings()

# Defines global variables
APIC = 'devnetapi.cisco.com/sandbox/apic_em'
USERNAME = 'devnetuser'
PASSWORD = 'Cisco123!'

# This calls on the getTicket method to generate a unique service ticket,
# necessary for making any API calls to the APIC-EM
newTicket = apic().getTicket(APIC, USERNAME, PASSWORD)

# This will later live under a lengthy 'if' statement depending on what
# request the user has made in the body of their Spark message, but presently
# it's an example of an API call and returns the json response
msg = apic().getVlans(APIC, newTicket)
print(msg)
print(type(msg["response"]))
