import websockets
import asyncio
import database_utils
import super_commands

global NICK
global COMMAND_PREFIX
global db_location
global RUNNING

NICK = 'burritosr'
COMMAND_PREFIX = '!'
db_location = '../../../db.sqlite3'
RUNNING = []


async def twitch_bot(token, channel):
    try:
        async with websockets.connect('wss://irc-ws.chat.twitch.tv:443', ssl=True) as websocket:
            print('PASS oauth:{}'.format(token.strip()))
            print('NICK {}'.format(NICK))
            await websocket.send('PASS oauth:{}'.format(token.strip()))
            await websocket.send('NICK {}'.format(NICK))
            await websocket.send('JOIN #{}'.format(channel))
            global connection
            connection = True
            mute = False
            while connection:
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
                        if msg[1:].split(" ")[0] == 'mute':
                            mute = not mute
                        else:
                            await check_commands(websocket, msg, channel, author)
    except Exception as e:
        print('SOMETHING OCCURRED, BOT RESTARTING\nError: {}'.format(e))
        await twitch_bot(token, channel)


async def check_ping(websocket, line):
    if line == 'PING :tmi.twitch.tv':
        print('PONGED')
        await websocket.send('PONG :tmi.twitch.tv')


async def get_chat_message(line):
    msg = line.split(':')
    if len(msg) >= 2 and 'PRIVMSG' in msg[1]:
        return msg[2:][0] , msg[1].split('!')[0]
    else:
        return False


async def check_commands(websocket, msg, channel, author):
    id = database_utils.get_id_from_channel(db_location, channel)
    if msg[0] == COMMAND_PREFIX:
        response = database_utils.get_response(db_location, msg[1:], id)
        if response:
            await websocket.send('PRIVMSG #{} :{}'.format(channel, response))
        elif msg[1:].split(" ")[0] in super_commands.existing_commands(id):
            response = super_commands.super_command(msg[1:], id)
            if response:
                print(response)
                await websocket.send('PRIVMSG #{} :{}'.format(channel, response))


async def _token_channel_pairs():
    user_ids = database_utils.get_user_list(db_location)
    token_channel_pairs = [(database_utils.get_access_token(db_location, i), database_utils.get_channel_from_id(db_location, i)) for i in user_ids]
    return token_channel_pairs


async def main():
    token_channel_pairs = await _token_channel_pairs()
    bots = []
    for token,channel in token_channel_pairs:
        bots.append(asyncio.ensure_future(twitch_bot(token,channel)))
        RUNNING.append(channel)
    await asyncio.gather(*bots)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()







