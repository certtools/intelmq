import json
import requests




url= "https://cloud-app.logbeat.ai/v1/blocks"
r = requests.get(url)
data = json.loads(r.content)

for value in data:
    print(value["c"])

