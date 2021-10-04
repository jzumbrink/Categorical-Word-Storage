import discord, json
from data import add_data, get_random_result

client = discord.Client()

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())


@client.event
async def on_message(msg):
    if msg.author.id == client.user.id or not msg.content.startswith(config['prefix']):
        return

    msg_content = msg.content[len(config['prefix']):].split()
    command = msg_content[0].lower()

    if command in ['s', 'l', 'f'] and len(msg_content) == 2:
        add_data(command, msg_content[1])

    if command == 'g' and len(msg_content) == 2 and len(msg_content[1]) == 1 and msg_content[1].isalpha():
        print(get_random_result(msg_content[1]))




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * 15)


client.run(config['token'])
