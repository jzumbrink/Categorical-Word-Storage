import discord
import json
from data import *
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

    elif command == 'g' and len(msg_content) == 2 and len(msg_content[1]) == 1 and msg_content[1].isalpha():
        result = get_random_result(msg_content[1], msg.author.id)
        await msg.channel.send(f"Stadt: {result[0].label}\nLand: {result[1].label}\nFluss/Gewässer: {result[2].label}")

    elif (command == 'ga' or command == 'getall') and len(msg_content) == 3:
        result = get_all(msg_content[2], msg_content[1], msg.author.id)
        table_data = '\n'.join(map(lambda row: '- ' + row.label, result))
        answer = f"Results for the category \"{msg_content[1]}\"\n{table_data}"
        print(list(map(lambda row: row.label, result)))
        print(answer)
        print(result)
        await msg.channel.send(answer)

    elif command == 'remove' and len(msg_content) >= 3:
        await msg.channel.send(delete_data(
            label_type=msg_content[1],
            label=' '.join(msg_content[2:])
        ))

    elif command == 'rowcount':
        await msg.channel.send(f"The table \"data\" consists of {get_rowcount()} rows")

    elif command == 'myrowcount':
        await msg.channel.send(f"The table \"data\" consists of {get_personal_rowcount(msg.author.id)} rows belonging to {msg.author.name}")

    elif command == 'h' or command == 'help' and len(msg_content) == 1:
        await msg.channel.send(get_help_string())

    elif command == 'mycat':
        cat_list_str = '\n - '.join(get_all_cats(msg.author.id))
        await msg.channel.send(f"The list of all your categories is:{cat_list_str}")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-' * 15)


client.run(config['token'])
