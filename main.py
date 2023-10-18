import requests
import json
import os
from pathlib import Path
import time

name = input("What do you want the name of the bots to be? >")
token = input("What is your token? >")
a = input("How many bots do you want to make? >")
created = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'authorization': token
}

while created < int(a):
    response = requests.post('https://discord.com/api/v9/applications', headers=headers, json={"name": f'{name}{created}'})
    if response.status_code == 201:
        print("created application")
        bot_data = response.json()
        bot_id = bot_data.get('id', None)
        print(bot_id)
        r = requests.post(f'https://discord.com/api/v9/applications/{bot_id}/bot/reset', headers=headers)
        print("Bot created!")
        bot_token = r.json().get('token', None)
        print(f'{name}{created}s token is {bot_token}')
        req = requests.patch(f'https://discord.com/api/v9/applications/{bot_id}', headers=headers, json={"bot_public":"true","bot_require_code_grant":"false","flags":565248})
        file = Path("savedtokens.txt")
        if file.is_file():
            f = open("savedtokens.txt", "a")
            f.write(f'{name}{created}:{bot_token}:https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=8&scope=bot' + '\n')
        else:
            f = open("savedtokens.txt", "x")
            f.write(f'{name}{created}:{bot_token}:https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=8&scope=bot' + '\n')   
    elif response.status_code == 401:
        print("Error: 401 Unauthorized, are you sure your token is correct?")
    elif response.status_code == 429:
        print("Error: 429 Too Many Requests, waiting 30 seconds...")
        time.sleep(30)
    else:
        print("Error: " + str(response.status_code))
    created += 1
    time.sleep(5)
else:
    print("Done!")
