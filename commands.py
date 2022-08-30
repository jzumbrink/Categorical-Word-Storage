import json
import discord
from data import *


with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    prefix = config['prefix']
    insertion_prefix = config['insertion-prefix']

help_string = f"""
**Insert new value into a category:** ```{insertion_prefix}<category> <your value>```
**Commands** (Note that the short aliases for each command are used in the examples, the full names of the commands are also working)
__help__: ```{prefix}h```
__getall__: displays all entities from a category starting with a given character (use \".\" to display all)  ```{prefix}ga <category> <char or .>```
__remove__:  ```{prefix}rm <category> <entity>```
__rowcount__: returns the number of rows/entities in the whole database ```{prefix}rc```
__myrowcount__: returns the number of rows/entities you are currently having ```{prefix}mrc```
__mycategories__: returns a list of all your categories ```{prefix}mc```
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
