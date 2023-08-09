import json
import requests
from websockets.sync.client import connect

token = "TOKEN HERE"
base_url = "https://hummus.sys42.net/api/v6"

def sendMessage(channelID, message): #send message function
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
        }
    data = json.dumps({'content': message,
                            'tts': False})
    requests.post(url=f"{base_url}/channels/{channelID}/messages",headers=headers,data=data)

def check(content,channelID, memberID, guildID): #here is where all commands go
    args = content.split() #makes arguments a thing, uses normal list format to split args

    if args[0] == "!test": #command detection and response to command
        sendMessage(channelID, "test")

def main(): #websocket connections and reconnections
    with connect("wss://hummus-gateway.sys42.net/?encoding=json&v=6") as websocket:
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
                    check(message['d']['content'],message['d']['channel_id'],message['d']['author']['id'], message['d']['guild_id'])
            except Exception as e: #if the server is not configured to constantly ping the bot so the websocket doesn't shut down, this reconnects the bot.
                 websocket.close()
                 print(f"""closing...
                       reason: {e}""")
                 true = False
while True: #runs forever
    main()
