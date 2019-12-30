import discord
from discord.ext import commands
import datetime
import json

client = commands.Bot(command_prefix = ';')
tokenFile = open('token.txt', 'r')
token = tokenFile.readline()

@client.event
async def on_ready():
    print('Online: Tetris99 Bot#7917 (ID: 651135979209621516)')

@client.event
async def on_member_join(member):
    memberMention = member.mention
    t99Server = client.get_guild(546595455983943690)
    modChannel = t99Server.get_channel(549452266864771102)
    dateNow, dateCreated = datetime.datetime.now(), member.created_at
    userSinceCreated = (dateNow - dateCreated).days * 24

    if userSinceCreated > 48:
        #print(userSinceCreated)
        pass
    else:
        await t99Server.ban(user=member, reason="Account is less than 48 hours old")
        await modChannel.send(memberMention + '** has been kicked from the server for having an account under 48 hours old**')

@client.command(name = 'ping')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} Pong!')

@client.command(name = 'leaderboard')
async def leaderboard(ctx, numberOfPlayers = 10):
    with open('leaderboard.json', 'r+') as f:
        leaderboardFile = json.load(f)

        sortedDict = {k: v for k, v in sorted(leaderboardFile.items(), key=lambda item: item[1], reverse=True)}
        counter = 1
        fullMessage = ''

        for player in sortedDict:
            if sortedDict[player] < 100:
                fullMessage += f'{player} - {sortedDict[player]}★\n'
            else:
                fullMessage += f'{player} - {sortedDict[player] - 99}★★\n'

        await ctx.send(fullMessage)
        
@client.command(name = 'leaderboardadd')
@commands.has_permissions(manage_messages = True)
async def leaderboardadd(ctx, playerName, playerLevelStr):
    with open('leaderboard.json', 'r+') as f:
        leaderboardFile = json.load(f)
    playerLevelInt = -99

    for character in playerLevelStr:
        if character == '*':
            playerLevelInt += 99

    if playerLevelStr[2:] == '**':
        playerLevelInt += int(playerLevelStr[:len(playerLevelStr) - 2])
    else:
        playerLevelInt += int(playerLevelStr[:len(playerLevelStr) - 1])

    leaderboardFile[playerName] = playerLevelInt
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboardFile, f)

    if playerLevelInt > 99:
        await ctx.send(f'{playerName} has been successfully added to the leaderboard with level {playerLevelInt - 99}★★')
    else:
        await ctx.send(f'{playerName} has been successfully added to the leaderboard with level {playerLevelInt}★')

client.run(token.strip())