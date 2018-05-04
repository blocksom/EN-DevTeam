import requests

URL = "https://api.ciscospark.com/v1/rooms"

#Access token is for "Best" bot Best@sparkbot@io
ACCESS_TOKEN = "ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx"

HEADERS = {"Content-type" : "application/json; charset=utf-8", "Authorization" : "Bearer " + ACCESS_TOKEN}
PARAMS = {"type" : "group", "max" : "2"}

response = requests.get(url=URL, headers=HEADERS, params=PARAMS)

print(response.status_code)
print(response.text)
