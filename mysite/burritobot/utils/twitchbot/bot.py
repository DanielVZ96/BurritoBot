import websockets
import asyncio
import database_utils
import super_commands

global TOKEN
global COMMAND_PREFIX
global CHANNEL
global NICK
global RESPONSE_COUNT
TOKEN = database_utils.get_access_token('../../../db.sqlite3')
COMMAND_PREFIX = '¿'
CHANNEL = 'wolhaiksong19'
NICK = 'burritosr'


async def twitch_bot(token, channel):
    async with websockets.connect('wss://irc-ws.chat.twitch.tv:443', ssl=True) as websocket:
        print('PASS oauth:{}'.format(token.strip()))
        print('NICK {}'.format(NICK))
        await websocket.send('PASS oauth:{}'.format(token.strip()))
        await websocket.send('NICK {}'.format(NICK))
        await websocket.send('JOIN #{}'.format(channel))
        global connection
        connection = True
        while connection == True:
            buffer = await websocket.recv()
            print(buffer)
            lines = buffer.split('\n')
            for line in lines:
                line = line.strip()
                await check_ping(websocket, line)
                msg = await get_chat_message(line)
                if msg:
                    author = msg[1]
                    msg = msg[0]
                    print('message: ' + msg, 'author: ' + author, sep='\n')
                    await check_commands(websocket, msg, author, channel)




async def check_ping(websocket, line):
    if line == 'PING :tmi.twitch.tv':
        print('PONGED')
        await websocket.send('PONG :tmi.twitch.tv')


async def get_chat_message(line):
    msg = line.split(':')
    if len(msg) >= 2 and 'PRIVMSG' in msg[1]:
        return (msg[2:][0] , msg[1].split('!')[0])
    else:
        return False


async def check_commands(websocket, msg, author, channel):
    id = database_utils.get_id_from_channel(channel)
    if msg[0] == COMMAND_PREFIX:
        response = database_utils.get_response('../../../db.sqlite3', msg[1:], id)
        if response:
            await websocket.send('PRIVMSG #{} :{}'.format(channel, response))
        elif msg[1:].split(" ")[0] in super_commands.existing_commands():
            response = super_commands.super_command(msg[1:])
            if response:
                print(response)
                await websocket.send('PRIVMSG #{} :{}'.format(channel, response))





if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(twitch_bot(TOKEN, CHANNEL))






