import requests
from SPARK import spark


example_post = spark().postMessage("ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx", "Y2lzY29zcGFyazovL3VzL1JPT00vMmE3OTVlM2YtZjkwNS0zMGE3LTg4NTAtOGFkODY5N2IzOWM2", "MAGIC")

example_get = spark().getMessage("ZWE3NzEwNTEtMDVkZC00MmI2LTg5NGEtOTcyZGM4ZWJmNDliZGNiMjA2ZGUtYmQx", "Y2lzY29zcGFyazovL3VzL1JPT00vMmE3OTVlM2YtZjkwNS0zMGE3LTg4NTAtOGFkODY5N2IzOWM2")

print (example_get)