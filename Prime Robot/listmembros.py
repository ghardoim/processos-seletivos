from urllib.parse import quote
from os import getenv
import requests as rq

def sucess_api_result(status_code):
    return 200 <= status_code <= 300

crAPI = "https://api.clashroyale.com/v1"
header = {
    "Authorization": f"Bearer {getenv('apitoken')}"
}

clan_name = "The Resistance"
id_brasil = 57000038
tag_filter = "#9V2Y"

resp = rq.get(f"{crAPI}/clans?name={quote(clan_name)}&locationId={id_brasil}", headers = header)
if not sucess_api_result(resp.status_code):
    print(f"{resp.json()['message']}")
    exit(1)

clans = [ clan for clan in resp.json()["items"] if clan["tag"].startswith(tag_filter) ]
if not clans:
    print("Nenhum clã encontrado.")
    exit(1)

for clan in clans:
    resp = rq.get(f"{crAPI}/clans/{quote(clan['tag'])}/members", headers = header)
    
    if not sucess_api_result(resp.status_code):
        print(f"{resp.json()['message']}")
        continue

    for membro in resp.json()["items"]:
        print(f"| nome({membro['name']}) | level({membro['expLevel']}) | troféus({membro['trophies']}) | papel({membro['role']}) |")
