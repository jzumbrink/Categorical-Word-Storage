import discord, json

client = discord.Client()

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())


@client.event
async def on_message(msg):
    if msg.author.id == client.user.id or not msg.content.startswith(config['prefix']):
        return

    await msg.channel.send("Hi")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * 15)


client.run(config['token'])
