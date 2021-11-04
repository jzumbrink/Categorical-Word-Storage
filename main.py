import discord
import json
from commands import *

client = discord.Client()

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    prefix = config['prefix']
    insertion_prefix = config['insertion-prefix']


@client.event
async def on_message(msg: discord.Message):
    if msg.author.id == client.user.id or not (msg.content.startswith(prefix) or msg.content.startswith(insertion_prefix)):
        return

    if msg.content.startswith(prefix):
        used_prefix = prefix
    else:
        used_prefix = insertion_prefix
    msg_content = msg.content[len(used_prefix):].split()
    command = msg_content[0].lower()

    if used_prefix == insertion_prefix:
        if len(msg_content) >= 2:
            await msg.channel.send(add_data(command, ' '.join(msg_content[1:]), msg.author.id))
        else:
            await msg.channel.send("Error")

    elif command == 'h' or command == 'help' and len(msg_content) == 1:
        await get_help_string(msg)

    elif (command == 'ga' or command == 'getall') and len(msg_content) == 3:
        await getall(msg_content, msg)

    elif command == 'remove' and len(msg_content) >= 3:
        await remove(msg_content, msg)

    elif command == 'rowcount':
        await rowcount(msg)

    elif command == 'myrowcount':
        await myrowcount(msg)

    elif command == 'mycat':
        await mycat(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * 15)


client.run(config['token'])
