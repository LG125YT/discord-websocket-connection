import json
import requests
from websockets.sync.client import connect
import fake_useragent

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random

token = "TOKEN HERE"
base_url = "https://hummus.sys42.net/api/v6"

def sendMessage(channelID, message): #send message function
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json',
        'User-Agent': agent
        }
    data = json.dumps({'content': message,
                            'tts': False})
    requests.post(url=f"{base_url}/channels/{channelID}/messages",headers=headers,data=data)

def kick(guildID, userID): #kick a person
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json',
        'User-Agent': agent
        }
    requests.delete(url=f"{base_url}/guilds/{guildID}/members/{userID}", headers=headers)

def nick(guildID,userID, nick): #set a person's nickname
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json',
        'User-Agent': agent
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    requests.patch(url=f"{base_url}/guilds/{guildID}/members/{userID}",headers=headers,data=data)

def check(content,channelID, memberID, guildID, data): #here is where all commands go
    args = content.split() #makes arguments a thing, uses normal list format to split args

    if args[0] == "!test": #command detection and response to command
        sendMessage(channelID, "test")

    if args[0] == "!nick":
        if len(args) > 2:
            id = data['d']['mentions'][0]['id']
            i = 0
            name = args[2]
            for word in args:
                if i > 2:
                    name = name + " " + word
                i += 1
            nick(guildID,id,name)
            sendMessage(channelID,f"Nicked <@{id}> to '{str(name)}'")
        else:
            sendMessage(channelID,"**__Error:__ Please ping a user and specify a nickname for the user. To Clear a nickname, specify 'None'.**")

    if args[0] == "!kick":
        if len(args) > 1:
            id = data['d']['mentions'][0]['id']
            kick(guildID,id)
            sendMessage(channelID,f"Successfully kicked <@{id}>")
        else:
            sendMessage(channelID, "**__Error:__ Please ping someone to kick them.**")

def main(): #websocket connections and reconnections
    with connect("wss://hummus-gateway.sys42.net/?encoding=json&v=6",user_agent_header=agent) as websocket:
        print("restarting...")
        true = True
        websocket.send(json.dumps({
                'op': 2,
                'd': {
                    'token': token,
                }
            }))
        while true:
            try:
                message = json.loads(websocket.recv())
                print(f"Received: {message}")
                if message['t'] == "MESSAGE_CREATE":
                    check(message['d']['content'],message['d']['channel_id'],message['d']['author']['id'], message['d']['guild_id'], message)
            except Exception as e: #if the server is not configured to constantly ping the bot so the websocket doesn't shut down, this reconnects the bot.
                 websocket.close()
                 print(f"""closing...
                       reason: {e}""")
                 true = False
while True: #runs forever
    main()
