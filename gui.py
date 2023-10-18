import tkinter as tk
import requests
import json
import os
from pathlib import Path
import time

def create_bot():
    name = ntext.get()
    token = ttext.get()
    created = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'authorization': token
    }
    while created < int(a.get()):
        response = requests.post('https://discord.com/api/v9/applications', headers=headers, json={"name": f'{name}{created+1}'})
        if response.status_code == 201:
            rlabel.config(text="created application")
            bot_data = response.json()
            bot_id = bot_data.get('id', None)
            print(bot_id)
            r = requests.post(f'https://discord.com/api/v9/applications/{bot_id}/bot/reset', headers=headers)
            rlabel.config(text="Bot created!")
            bot_token = r.json().get('token', None)
            print(f'{name}{created+1}s token is {bot_token}')
            req = requests.patch(f'https://discord.com/api/v9/applications/{bot_id}', headers=headers, json={"bot_public":"true","bot_require_code_grant":"false","flags":565248})
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


window = tk.Tk()
window.title("Bot Creator")
window.geometry("500x500")
window.resizable(False, False)
#window.configure(bg="black")
lb1 = tk.Label(window, text="Bot(s) Name:")
lb1.place(x=10, y=100)
ntext = tk.Entry(window, width=50)
ntext.place(x=100, y=100)
file = Path("default_token.txt")
if file.is_file():
    ttext = tk.Entry(window, width=50)
    t = open("default_token.txt", "r")
    ttext.insert(0, t.read())
    tlabel = tk.Label(window, text="Token:")
    ttext.config(state="readonly")
    ttext.place(x=100, y=150)
    tlabel.place(x=10, y=150)
else:
    ttext = tk.Entry(window, width=50)
    tlabel = tk.Label(window, text="Token:")
    ttext.place(x=100, y=150)
    tlabel.place(x=10, y=150)
a = tk.Entry(window, width=50)
a.place(x=100, y=200)
alabel = tk.Label(window, text="Amount:",)
alabel.place(x=10, y=200)
btn = tk.Button(window, text="Create", command=create_bot)
btnxpos = (500 - btn.winfo_reqwidth()) // 2
btn.place(x=btnxpos, y=250)
rlabel = tk.Label(window, text="Press create to start creating bots.")
rxpos = (500 - rlabel.winfo_reqwidth()) // 2
rlabel.place(x=rxpos, y=300)

#token = tk.StringVar()
window.mainloop()
