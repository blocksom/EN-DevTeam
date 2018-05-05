import requests
from SPARK import spark



bot_token = "ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx" #Nicole's bot token #the only parameter that must be statically defined
bot_message = "POST MESSAGE HERE"

room_id = spark().getRoom(bot_token)

get_message = spark().getMessage(bot_token, room_id)

post_message = spark().postMessage(bot_token, room_id, bot_message)





