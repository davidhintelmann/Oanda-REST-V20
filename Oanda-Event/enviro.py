import json, os
from pathlib import Path

token_path = Path(__file__).parents[0]
id_path = os.path.join(token_path,'res/ids.json')
token_path = os.path.join(token_path,'res/oanda_api_key.json')

ENVIRONMENTS = {
    "streaming":{
        "real":"stream-fxtrade.oanda.com",
        "practice":"stream-fxpractice.oanda.com",
        "sandbox":"stream-sandbox.oanda.com"
    },
    "api":{
        "real":"api-fxtrade.oanda.com",
        "practice":"api-fxpractice.oanda.com",
        "sandbox":"api-sandbox.oanda.com"
    }
}

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]

def GrabToken(path=token_path):
    with open(path) as token_file:
        token = json.load(token_file)
        return token['token']

def GrabID(path=id_path):
    with open(path) as id_file:
        ID_num = json.load(id_file)
        return ID_num['id']
