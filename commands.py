import json
import discord
from data import *


with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    prefix = config['prefix']
    insertion_prefix = config['insertion-prefix']

help_string = f"""
{insertion_prefix}<category> <your value>
{prefix}ga <category> <char or .>
{prefix}remove <category> <value>
{prefix}rowcount
{prefix}myrowcount
{prefix}mycat
"""


async def get_help_string(msg: discord.Message) -> str:
    await msg.channel.send(help_string)


async def getall(msg_content: str, msg: discord.Message):
    result = get_all(msg_content[2], msg_content[1], msg.author.id)
    table_data = '\n'.join(sorted(map(lambda row: '- ' + row.label, result)))
    answer = f"Results for the category \"{msg_content[1]}\" (Count: {len(result)})\n{table_data}"
    print(list(map(lambda row: row.label, result)))
    print(answer)
    print(result)
    await msg.channel.send(answer)


async def remove(msg_content: str, msg: discord.Message):
    await msg.channel.send(delete_data(
        label_type=msg_content[1],
        label=' '.join(msg_content[2:]),
        author_id=msg.author.id
    ))


async def rowcount(msg: discord.Message):
    await msg.channel.send(f"The table \"data\" consists of {get_rowcount()} rows")


async def myrowcount(msg: discord.Message):
    await msg.channel.send(
        f"The table \"data\" consists of {get_personal_rowcount(msg.author.id)} rows belonging to {msg.author.name}")


async def mycat(msg: discord.Message):
    cat_list_str = '\n - ' + '\n - '.join(get_all_cats(msg.author.id))
    await msg.channel.send(f"The list of all your categories is:{cat_list_str}")
