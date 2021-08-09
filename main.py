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
    await ctx.send("to cwel", delete_after=5)


@bot.command(name="besty")
async def on_message(ctx):
    query = urlopen("https://besty.pl/losuj")
    soup = bs.BeautifulSoup(query, "html.parser")
    posts = soup.find_all("img", {"class": "img-responsive"}, limit=2)
    image = posts[1].get("src")
    file_type = image.split(".")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                await ctx.send("Nie da się ściagnąć ;(")
                return
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, "Super-obrazek." + file_type))

@bot.command(name="role")
async def on_message(ctx):
    roles = ["Top", "Mid", "Jungle", "Support", "Marksman"]
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.guild.get_channel(ctx.author.voice.channel.id)
        channel_members = channel.members
        for i in range(len(channel_members)):
            if channel_members[i].bot:
                channel_members.pop(i)
        if len(channel_members) != 5:
            await ctx.send("Nie ma pięciu osób na kanale.")
            return
        for i in range(len(channel_members)):
            r = random.randint(0, len(roles))
            await ctx.send(channel_members[i].mention + ": " + roles[r] + "\n")
            roles.pop(r)
    else:
        await ctx.send("Debilu nie jesteś w kanale dźwiękowym. Weź sie ogarnij.")


@bot.command(name="rule34")
async def on_message(ctx, *args):
    # Ściąga losowy obrazek z gelbooru.com lub losowe zdjęcie z zadanego tagu
    if not args:
        r = random.randint(0, 999501)
        query = urlopen("https://rule34.xxx/index.php?page=dapi&s=post&q=index&id=" + str(r))
        soup = bs.BeautifulSoup(query, "html.parser")
        post = soup.find("post")
        image = post.get("file_url")
    else:
        if len(args) > 1:
            tag = "_".join(args).lower()
            tag = tag.replace("&", "%20")
        else:
            tag = args[0]
        query = urlopen("https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1&tags=" + tag)
        soup = bs.BeautifulSoup(query, "html.parser")
        count = int(soup.find("posts").get("count"))
        if count == 0:
            # Próba znalezenia podobnego tagu
            await ctx.send("Szukam podobnego tagu.\n")
            tag += "~"
            query = urlopen("https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1&tags=" + tag)
            soup = bs.BeautifulSoup(query, "html.parser")
            count = int(soup.find("posts").get("count"))
            if count == 0:
                await ctx.send("Nie ma obrazka z tym tagiem.")
                return

        # Na rule34.xxx nie trzeba ograniczać głębokości wyszukiwania
        pid = random.randint(0, int(count / 100))

        query = urlopen("https://rule34.xxx/index.php?page=dapi&s=post&q=index&pid=" + str(pid)
                        + "&limit=100&tags=" + tag)
        soup = bs.BeautifulSoup(query, "html.parser")
        posts = soup.find_all("post")
        r = random.randint(0, len(posts)-1)
        post = posts[r]
        image = post.get("file_url")
    file_type = image.split(".")[-1]

    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                await ctx.send("Nie da się ściagnąć ;(")
                return
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, "Super-obrazek." + file_type))


@bot.command(name="anime")
async def on_message(ctx, *args):
    # Ściąga losowy obrazek z gelbooru.com lub losowe zdjęcie z zadanego tagu
    if not args:
        query = urlopen("https://gelbooru.com/index.php?page=post&s=random")
        soup = bs.BeautifulSoup(query, "html.parser")
        image = soup.find(id="image").get("src")
    else:
        if len(args) > 1:
            tag = "_".join(args).lower()
            tag = tag.replace("&", "%20")
        else:
            tag = args[0]
        query = urlopen("https://gelbooru.com/index.php?page=dapi&s=post&limit=1&q=index&tags=" + tag + "%20-loli-underage")
        soup = bs.BeautifulSoup(query, "html.parser")
        count = int(soup.find("posts").get("count"))
        if count == 0:
            # Próba znalezenia podobnego tagu
            await ctx.send("Szukam podobnego tagu.\n")
            tag += "~"
            query = urlopen("https://gelbooru.com/index.php?page=dapi&s=post&limit=1&q=index&tags=" + tag + "%20-loli-underage")
            soup = bs.BeautifulSoup(query, "html.parser")
            count = int(soup.find("posts").get("count"))
            if count == 0:
                await ctx.send("Nie ma obrazka z tym tagiem.")
                return
        if int(count / 100) > 200:
            pid = random.randint(0, 200)
        else:
            pid = random.randint(0, int(count / 100))

        query = urlopen("https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&pid=" + str(pid)
                        + "&tags=" + tag + "%20-loli-underage")
        soup = bs.BeautifulSoup(query, "html.parser")
        posts = soup.find_all("post")
        r = random.randint(0, len(posts)-1)
        post = posts[r]
        image = post.get("file_url")
    file_type = image.split(".")[-1]

    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                await ctx.send("Nie da się ściagnąć ;(")
                return
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, "Super-obrazek." + file_type))


@bot.command(name="safeAnime")
async def on_message(ctx, *args):
    # Ściąga losowy obrazek z safebooru.org lub losowe zdjęcie z zadanego tagu
    if not args:
        r = random.randint(0, 2000000)
        query = urlopen("https://safebooru.org/index.php?page=dapi&s=post&q=index&id=" + str(r))
        soup = bs.BeautifulSoup(query, "html.parser")
        post = soup.find("post")
        image = post.get("file_url")
    else:
        if len(args) > 1:
            tag = "_".join(args).lower()
            tag = tag.replace("&", "%20")
        else:
            tag = args[0]
        query = urlopen("https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1&tags=" + tag)
        soup = bs.BeautifulSoup(query, "html.parser")
        count = int(soup.find("posts").get("count"))
        if count == 0:
            # Próba znalezenia podobnego
            await ctx.send("Szukam podobnego tagu.\n")
            tag += "~"
            query = urlopen("https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1&tags=" + tag)
            soup = bs.BeautifulSoup(query, "html.parser")
            count = int(soup.find("posts").get("count"))
            if count == 0:
                await ctx.send("Nie ma obrazka z tym tagiem.")
                return
        # Ustawiamy max = 200 bo nie pozwala na więcej
        if int(count / 100) > 200:
            pid = random.randint(0, 200)
        else:
            pid = random.randint(0, int(count / 100))
        query = urlopen("https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=100&pid=" + str(pid)
                        + "&tags=" + tag)
        soup = bs.BeautifulSoup(query, "html.parser")
        posts = soup.find_all("post")
        r = random.randint(0, len(posts)-1)
        post = posts[r]
        image = post.get("file_url")
    file_type = image.split(".")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                await ctx.send("Nie da się ściagnąć ;(")
                return
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, "Super-obrazek." + file_type))


@bot.command(name="generuj")
async def on_message(ctx, number_of_teams=2, game=None):
    number_of_teams = int(number_of_teams)
    if number_of_teams < 2:
        await ctx.send("Debilu daj więcej drużyn")
    elif ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.guild.get_channel(ctx.author.voice.channel.id)
        channel_members = channel.members
        bots_numbers = []
        for i in range(len(channel_members)):
            if channel_members[i].bot:
                bots_numbers.append(i)
        for number in bots_numbers:
            channel_members.pop(number)
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
                    "Drużyna: " + str(k + 1) + "\n" + "\n".join([i.mention for i in team])
                )
                k += 1
            elif game == "cs" and number_of_teams == 2:
                if k == 0:
                    k += 1
                    await ctx.send(
                        "Terroryści: " + "\n" + "\n".join([i.mention for i in team])
                    )
                else:
                    await ctx.send(
                        "Antyterroryści: " + "\n" + "\n".join([i.mention for i in team])
                    )
            elif game == "lol" and number_of_teams == 2:
                if k == 0:
                    k += 1
                    await ctx.send(
                        "Blue side: " + "\n" + "\n".join([i.mention for i in team])
                    )
                else:
                    await ctx.send(
                        "Red side: " + "\n" + "\n".join([i.mention for i in team])
                    )
    else:
        await ctx.send("Debilu nie jesteś w kanale dźwiękowym. Weź sie ogarnij.")


bot.run(TOKEN)
