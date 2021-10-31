import json

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
"""


def get_help_string():
    return help_string
