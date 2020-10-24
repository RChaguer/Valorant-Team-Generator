import discord
import random as r
from webserver import keep_alive
import os
from discord.ext import commands, tasks

from discord import Guild
from discord.utils import get


client = discord.Client()

agents_ids = [721807208324661248, 721807169531674696, 721807133397483600, 721807108651089952, 721807047888339044,
              721807036924297288, 721806995165937786, 721806966267052131, 721806929420222536, 721806762650501131,
              721806683176828959]

agents = {721807208324661248:'REYNA',721807169531674696:'RAZE',721807133397483600:'PHOENIX',721807108651089952:'JETT',721807047888339044:'SOVA',721807036924297288:'BREACH',721806995165937786:'CYPHER',721806966267052131:'VIPER',721806929420222536:'OMEN',721806762650501131:'SAGE', 721806683176828959:'BRIMSTONE'}

maps = ["HAVEN", "SPLIT", "BIND", "ASCENT"]


def random_team_gen(db):
    team1 = [player for player in db.keys()]
    team2 = []
    for i in range(len(db)//2):
        player = r.choice(team1)
        team2.append(player)
        team1.remove(player)
    return team1, team2


def random_agent_gen(team, database):
    global agents_ids
    available_agents = [agent for agent in agents_ids]
    final_team = []
    for player in team:
        agent = r.choice(database[player])
        while agent not in available_agents:
            agent = r.choice(database[player])
        final_team.append([player, agent])
        available_agents.remove(agent)
    return final_team


def generate_match(database):
    global maps
    map = r.choice(maps)
    team1, team2 = random_team_gen(database)
    final_team1, final_team2 = random_agent_gen(team1, database), random_agent_gen(team2, database)
    message = "MAP = {} \n".format(map)
    message += "ATTACKING: \n"
    for player, agent in final_team1:
        message += "{} : {}\n".format(player, agents[agent])
    message += "DEFENDING: \n"
    for player, agent in final_team2:
        message += "{} : {}\n".format(player, agents[agent])
    return message

def generate_unrated(database):
    team = [player for player in database.keys()]
    final_team = random_agent_gen(team, database)
    message = "Composition: \n"
    for player, agent in final_team:
        message += "{} : {}\n".format(player, agents[agent])
    return message


@client.event
async def on_message(message):
    channel = client.get_channel(703983175772405790)
    cur_members = []
    for member in channel.members:
        cur_members.append(member)
    players = []

    db = {}
    for player in cur_members:
        for role in player.roles:
            if role.id in agents_ids:
                if player not in db:
                    db[player] = [role.id]
                else:
                    db[player] += [role.id]

    if str(message.content) == "-matchmake":
      if str(message.author) == "BigShaq1208#8492":
        await message.channel.send("Wa jm3 krrk, had noob hada")
      if str(message.author) == "Meteor#2465":
        await message.channel.send("Hello Master <3")
      await message.channel.send(generate_unrated(db))
    elif str(message.content) == "-matchmake_c":
      if str(message.author) == "BigShaq1208#8492":
        await message.channel.send("Wa jm3 krrk, had noob hada")
      if str(message.author) == "Meteor#2465":
        await message.channel.send("Hello Master <3")
      await message.channel.send(generate_match(db))
    elif str(message.content) == "-matchmake_help":
        await message.channel.send("send -matchmake for unrated matchmaking or -matchmake_c for custom game matchmaking")

keep_alive()
#TOKEN= os.environ.get("DISCORD_BOT_SECRET")

client.run("NzIxODA5MTE4MjUxMzE5NDE4.XwD7Xg.clvUghbwMJFSiBXL7WKtPFJjky8")
