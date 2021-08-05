import discord
from discord.ext import commands
from main import Utilities
import ast
import asyncio


print(discord.__version__)
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents= intents)

@client.event
async def on_ready():
        print(f"[!] Initializing...")
        print(f"[!] Initialization complete!")


@client.command()
async def members(ctx):
      membes = ctx.message.guild.members
      server = ctx.message.guild
      print(len(membes))
      for member in membes:
          member_roles =[]
          for role in member.roles:
              member_roles.append(role.name)
          if 'members' not in member_roles:
              role = discord.utils.get(server.roles, name="member")
              print(type(role))
              await membes.add_roles(role)

@client.command()
async def clear(ctx):
    auth = ctx.author
    guild = ctx.message.guild
    channel_name = ctx.channel.name
    existing_channel = discord.utils.get(ctx.message.guild.channels, name=channel_name)
    if existing_channel is not None:
        await  existing_channel.clone()
        await existing_channel.delete()

@client.command()
async def verify(ctx):
        server = ctx.message.guild
        channel = ctx.message.channel
        user_id = ctx.author.id
        member = ctx.author
        print(type(member))
        data = None
        with open('data.txt') as fileread:
            x = fileread.read()
            data = ast.literal_eval(x)
        fileread.close()
        flag = False
        for id in data.keys():
            if id != user_id:
                continue
            flag = True
        if flag:
            nickname = data[user_id]
            await member.edit(nick=nickname)
            role = discord.utils.get(server.roles, name="members")
            print(type(role))
            await member.add_roles(role)
            temp = discord.utils.get(server.roles, name="non-verified")
            await member.remove_roles(temp)
        else:
            try:
                await channel.send("Please enter your name: (You have 60 seconds to complete the verification)")
                msg = await client.wait_for("message", timeout=60)
                txt = msg.content
            except asyncio.TimeoutError:
                await channel.send("Sorry You did not reply in time")
                await channel.send("Please run the !verify command again")
            data[user_id] = txt
            wrt = str(data)
            file = open('data.txt', 'w')
            file.write(wrt)
            file.close()
            role = discord.utils.get(server.roles, name="members")
            print(type(role))
            await member.add_roles(role)
            temp = discord.utils.get(server.roles, name="non-verified")
            await member.edit(nick=txt)
            await member.remove_roles(temp)



client.run("ODM2MzcwODYxNTQ4MTA5ODk0.YIdBEA.3jW1_FAMPFePnMvcj9eVaFU2d8U")