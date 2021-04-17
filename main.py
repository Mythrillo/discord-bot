import os
import discord
import io
import aiohttp
from dotenv import load_dotenv
import random
from discord.ext import commands
import bs4 as bs
from urllib.request import urlopen


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name="olek")
async def on_message(ctx):
    await ctx.send("to cwel",delete_after=5)


@bot.command(name="anime")
async def on_message(ctx):
    # Ściąga losowy obrazek z safebooru.org
    query = urlopen("https://safebooru.org/index.php?page=post&s=random")
    soup = bs.BeautifulSoup(query, "html.parser")
    image = soup.find(id="image").get("src")
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                await ctx.send("Nie da się ściagnąć ;(")
                return
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'Super-obrazek.png'))


@bot.command(name="generuj")
async def on_message(ctx, number_of_teams=2, game=None):
    number_of_teams = int(number_of_teams)
    if number_of_teams < 2:
        await ctx.send("Debilu daj więcej drużyn")
    elif ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.guild.get_channel(ctx.author.voice.channel.id)
        channel_members = channel.members
        for i in range(len(channel_members)):
            if channel_members[i].bot:
                channel_members.pop(i)
        number_of_members = len(channel_members)
        if number_of_teams > number_of_members:
            await ctx.send("Debilu za dużo drużyn a za mało zawodników")
            return
        teams = []
        if number_of_members % number_of_teams == 0:
            team_size = int(number_of_members / number_of_teams)
            for i in range(number_of_teams):
                team = random.sample(channel_members, team_size)
                teams.append(team)
                channel_members = list(set(channel_members) - set(team))
        else:
            r = number_of_members % int(number_of_teams)
            team_size = int((number_of_members - r) / number_of_teams)
            for i in range(number_of_teams):
                team = random.sample(channel_members, team_size)
                channel_members = list(set(channel_members) - set(team))
                if r != 0:
                    tmp = random.choice(channel_members)
                    team.append(tmp)
                    channel_members.remove(tmp)
                    r -= 1
                teams.append(team)
        k = 0
        for team in teams:
            if game is None:
                await ctx.send(
                    "Drużyna: " + str(k + 1) + "\n" + "\n".join([str(i) for i in team])
                )
                k += 1
            elif game == "cs" and number_of_teams == 2:
                if k == 0:
                    k += 1
                    await ctx.send(
                        "Terroryści: " + "\n" + "\n".join([str(i) for i in team])
                    )
                else:
                    await ctx.send(
                        "Antyterroryści: " + "\n" + "\n".join([str(i) for i in team])
                    )
            elif game == "lol" and number_of_teams == 2:
                if k == 0:
                    k += 1
                    await ctx.send(
                        "Blue side: " + "\n" + "\n".join([str(i) for i in team])
                    )
                else:
                    await ctx.send(
                        "Red side: " + "\n" + "\n".join([str(i) for i in team])
                    )
    else:
        await ctx.send("Debilu nie jesteś w kanale dźwiękowym. Weź sie ogarnij.")


bot.run(TOKEN)
