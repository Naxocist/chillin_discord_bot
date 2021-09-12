from discord.ext import commands
from bs4 import BeautifulSoup
from random import *
from datetime import *
from data_process import *
import pytz
import discord
import requests
import asyncio
import os
import json


def get_language(msg):
    with open("language.json", "r", encoding="utf-8") as f:
        lang = json.load(f)
    return lang[str(msg.guild.id)]


gif_list = ["https://c.tenor.com/c3ks1DYnyr4AAAAC/anime-anime-girl.gif",
            "https://c.tenor.com/czmwFLhXJQ0AAAAC/anime-i-dont-know.gif",
            "https://c.tenor.com/ZINgFAwKh1QAAAAC/anime-love.gif",
            "https://c.tenor.com/Am61DGzxpGoAAAAC/anime-laughing.gif",
            "https://c.tenor.com/mkunLNebofwAAAAC/anime-headbang.gif",
            "https://c.tenor.com/H63Kb7qg8HoAAAAC/anime-chainsaw.gif",
            "https://c.tenor.com/0XNOlxxAFvcAAAAC/chuunibyou-anime.gif"]

client = commands.Bot(command_prefix=".",
                      activity=discord.Activity(type=discord.ActivityType.watching, name="for .help"))

client.remove_command('help')


def get_anime_name(specify):
    possible = []
    if not specify:
        return choice(animes)

    specify_list = specify.lower().split()
    for g in genre:
        if all(ele in g for ele in specify_list):
            possible.append(animes[genre.index(g)])

    return choice(possible)


@client.event
async def on_ready():  # Ready
    print("Chillin' bot is ready for her duty!")


@client.event
async def on_guild_join(guild):
    with open("language.json", "r", encoding="utf-8") as f:
        lang = json.load(f)
    print("Joined", guild.id)

    lang[str(guild.id)] = "en"

    with open("language.json", "w", encoding="utf-8") as f:
        json.dump(lang, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("language.json", "r", encoding="utf-8") as f:
        lang = json.load(f)

    lang.pop(str(guild.id))

    with open("language.json", "w", encoding="utf-8") as f:
        json.dump(lang, f, indent=4)


@client.command(pass_context=True, aliases=["lang"])
@commands.has_permissions(administrator=True)
async def language(ctx, l=""):

    if l == "":
        flag = "🇹🇭" if get_language(ctx) == "th" else "🇺🇸"
        await ctx.send(f"Current language `{get_language(ctx)}` {flag}")

    elif l in ["en", "th"]:
        with open("language.json", "r", encoding="utf-8") as f:
            lang = json.load(f)

        lang[str(ctx.guild.id)] = l

        with open("language.json", "w", encoding="utf-8") as f:
            json.dump(lang, f, indent=4)
        await ctx.send("Submitted!")

    else:
        await ctx.send(embed=discord.Embed(title="Supported languages",
                                           description="> Thai `th` 🇹🇭\n> English `en` 🇺🇸"))


@client.command(aliases=['a'])  # random anime [optional genre]
async def anime(ctx, *, specify=""):
    anime = get_anime_name(specify)
    title = anime[:anime.index(":")] + '\n' + ">" + anime[anime.index(":") + 1:] if ':' in anime and len(anime) > 30 \
        else anime
    embed = discord.Embed(title=title, colour=discord.Colour.random())

    g_list = genre[animes.index(anime)]
    g_list.insert(4, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])

    if get_language(ctx) == "en":
        episode = "`Movie`" if ep[anime] == '0' else f"`{ep[anime]}`" + " episodes"
        ss = "not specified" if episode == "The movie" else season[anime]
        image = pic[anime]
        ranked = rank[anime]
        url = link[anime]
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        embed.add_field(name="Genre", value=g_value, inline=False)
        embed.add_field(name="Season", value=f"`{ss}`", inline=True)
        embed.add_field(name="Length", value=episode, inline=True)
        embed.add_field(name=f"Ranked: #`{ranked}`", value=f"[Check it out!]({url})", inline=False)

        embed.set_image(url=image)
    else:
        episode = "`ภาพยนตร์`" if ep[anime] == '0' else f"`{ep[anime]}`" + " ตอน"
        ss = "ไม่ระบุ" if episode == "The movie" else season[anime]
        image = pic[anime]
        ranked = rank[anime]
        url = link[anime]
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        embed.add_field(name="ปรเภท", value=g_value, inline=False)
        embed.add_field(name="ซีซั่น", value=f"`{ss}`", inline=True)
        embed.add_field(name="ความยาว", value=episode, inline=True)
        embed.add_field(name=f"อันดับ: #`{ranked}`", value=f"[>ข้อมูลเพื่มเติม<]({url})", inline=False)

        embed.set_image(url=image)
    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "📬")
    r_possible = []
    reaction_dict = {"Magic": "✨", "Action": "⚔", "Romance": "💗", "Supernatural": "🌪️", "Comedy": "😝",
                     "Drama": "🎭", "Kids": "🧒", "School": "🏫", "Fantasy": "🐉", "Cars": "🏎", "Sports": "🏀",
                     "Sci-fi": "🧪", "Game": "🎮", "Music": "🎶", "Superpower": "🦸", "Military": "🪖"}
    for g, r in reaction_dict.items():
        if g in g_value:
            r_possible.append(r)
    await discord.Message.add_reaction(msg, choice(r_possible)) if r_possible else \
        await discord.Message.add_reaction(msg, "🔥")


@client.command(aliases=["ah"])
@commands.is_nsfw()
async def animehentai(ctx):
    if get_language(ctx) == "en":
        anime = choice(nsfw)
        embed = discord.Embed(title=f"{anime}", url=link[anime], colour=discord.Colour.random())

        episode = "`1` ep" if ep[anime] == '1' else f"`{ep[anime]}`" + " eps"
        ss = "not specified" if episode == "The movie" else season[anime]
        image = pic[anime]
        ranked = rank[anime]
        g_list = nsfw_genre[nsfw.index(anime)]
        g_list.insert(3, "\n")
        g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        embed.add_field(name="Genre", value=g_value, inline=False)
        embed.add_field(name="Season", value=f"`{ss}`", inline=True)
        embed.add_field(name="Length", value=episode, inline=True)
        embed.add_field(name=f"`{ranked}`", value="-" * 39, inline=False)

        embed.set_image(url=image)

        msg = await ctx.send(embed=embed)
        await discord.Message.add_reaction(msg, "📬")
        await discord.Message.add_reaction(msg, "💪")
    else:
        anime = choice(nsfw)
        embed = discord.Embed(title=f"{anime}", url=link[anime], colour=discord.Colour.random())

        episode = "`1` ตอน" if ep[anime] == '1' else f"`{ep[anime]}`" + " ตอน"
        ss = "ไม่ระบุ" if episode == "ภาพยนตร์" else season[anime]
        image = pic[anime]
        ranked = rank[anime]
        g_list = nsfw_genre[nsfw.index(anime)]
        g_list.insert(3, "\n")
        g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        embed.add_field(name="ประเภท", value=g_value, inline=False)
        embed.add_field(name="ซีซั่น", value=f"`{ss}`", inline=True)
        embed.add_field(name="ควายาว", value=episode, inline=True)
        embed.add_field(name=f"`{ranked}`", value="-" * 39, inline=False)

        embed.set_image(url=image)

        msg = await ctx.send(embed=embed)
        await discord.Message.add_reaction(msg, "📬")
        await discord.Message.add_reaction(msg, "💪")


@client.command(aliases=["d"])
@commands.is_nsfw()
async def doujin(ctx, code=""):
    code = code.strip()
    if code:
        url = 'https://nhentai.net/g/' + code
    else:
        url = "https://nhentai.net/random/"
    async with ctx.typing():
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        await asyncio.sleep(0.1)
    error = soup.find("div", class_="container error")
    if get_language(ctx) == "en":
        if error:
            green = randint(0, 150)
            embed = discord.Embed(title="We don't know that sauce!", description="> May be `typos` somewhere?",
                                  color=discord.Colour.from_rgb(224, green, 0))
            await ctx.send(embed=embed)
        else:
            pic = soup.find("img", class_="lazyload")['data-src']
            name_list = soup.find("h1", class_="title")
            name = [i.text for i in name_list]
            id = soup.find("h3", id="gallery_id").text
            embed = discord.Embed(title=name[0]+name[1]+name[2], url=f"https://nhentai.net/g/{id[1:]}",
                                  color=discord.Colour.random())
            if code:
                embed.add_field(name=f"Sauce # `{code}` delivered!", value="Verified Sauce! Here you go.")
            else:
                embed.add_field(name=f"Random sauce => # `{id}` delivered!", value="`There you go!`")

            embed.set_image(url=pic)
            msg = await ctx.send(embed=embed)
            await discord.Message.add_reaction(msg, "📬")
            await discord.Message.add_reaction(msg, "👍🏻")
    else:
        if error:
            green = randint(0, 150)
            embed = discord.Embed(title="ซอสปลอมไอ้สลัด!", description="> พิมพ์ผิดป่าว?",
                                  color=discord.Colour.from_rgb(224, green, 0))
            await ctx.send(embed=embed)
        else:
            pic = soup.find("img", class_="lazyload")['data-src']
            name_list = soup.find("h1", class_="title")
            name = [i.text for i in name_list]
            id = soup.find("h3", id="gallery_id").text
            embed = discord.Embed(title=name[0]+name[1]+name[2], url=f"https://nhentai.net/g/{id[1:]}",
                                  color=discord.Colour.random())
            if code:
                embed.add_field(name=f"ซอส # `{code}` มาส่งละ!", value="ซอสของจริงหว่ะ!")
            else:
                embed.add_field(name=f"พรจากบอท => # `{id}`!", value="`ได้แล้วนะ ไปอ่านเลยป่าว..`")

            embed.set_image(url=pic)

            msg = await ctx.send(embed=embed)
            await discord.Message.add_reaction(msg, "📬")
            await discord.Message.add_reaction(msg, "👍🏻")


@client.command(aliases=['dat'])  # date function
async def date(ctx):
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    text = str(now.strftime("%A, %d %b %Y %H:%M %p"))
    d = discord.Embed(title=text, color=discord.Colour.random())
    async with ctx.typing():
        await asyncio.sleep(0.5)
    await ctx.send(embed=d)


@client.event
async def on_reaction_add(reaction, user):  # check reaction
    if user == client.user:
        return
    if reaction.emoji == "📬":
        await reaction.message.add_reaction("✅")
        await user.send(embed=reaction.message.embeds[0])


@client.command(pass_context=True, aliases=["commands", "command"])
async def help(ctx):  # help function
    with open('help_language.json', 'r', encoding='utf-8') as f:
        lang_data = json.load(f)
        d = lang_data[get_language(ctx)]
        h1 = d['h1']
        h2 = d['h2']
        nsfw = d['nsfw']
        save_result = d['save_result']
        contact = d['contact']
        dev = d['dev']
        _anime = d['genre']
        _anime_info = d['_anime_info']
        _date_info = d['_date_info']
        _ah_info = d['_ah_info']
        sauce = d['sauce']
        _doujin_info = d['_doujin_info']
        page = d['page']
    embed = discord.Embed(title=h1)
    embed.set_thumbnail(url=choice(gif_list))

    invite = "https://discord.com/api/oauth2/authorize?client_id=877425384864501760&permissions=137439308864&scope=bot"
    server = "https://discord.gg/3sAYuxc3aF"
    me = "Naxocist#2982"
    pages = 2
    cur_page = 1

    embed.add_field(name=nsfw, value="> ⚠", inline=True)
    embed.add_field(name=save_result, value="> 📬", inline=True)
    embed.add_field(name=contact, value=f"[Invite!]({invite}) | [Server]({server})\n{dev}: `{me}` ", inline=False)
    embed.set_footer(text=page + f" {cur_page}/{pages}")

    async with ctx.typing():
        await asyncio.sleep(0.25)
    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "◀")
    await discord.Message.add_reaction(msg, "▶")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]  # check if author is the reactor

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=30, check=check)  # stops the loop 60 sec

            if str(reaction.emoji) == "▶" and cur_page != pages:
                cur_page += 1
                new_embed = discord.Embed(title=h2)
                new_embed.set_thumbnail(url=choice(gif_list))
                new_embed.add_field(name=f"`.anime | .a [{_anime}]`", value=_anime_info)
                new_embed.add_field(name="`.date | .dat`  🕒", value=_date_info, inline=False)
                new_embed.add_field(name='`.animehentai | .ah` `⚠`', value=_ah_info, inline=True)
                new_embed.add_field(name=f'`.doujin | .d [{sauce}]` `⚠`', value=_doujin_info, inline=True)
                new_embed.add_field(name="`.language | .lang *Only Administrator*`", value="> `th`: Thai  🇹🇭\n> `en`: English 🇺🇸",
                                    inline=False)
                new_embed.set_footer(text=page+f" {cur_page}/{pages}")
                await msg.edit(embed=new_embed)
                await msg.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀" and cur_page > 1:
                cur_page -= 1
                new_embed = discord.Embed(title=h1)
                new_embed.set_thumbnail(url=choice(gif_list))
                new_embed.add_field(name=nsfw, value="> ⚠", inline=True)
                new_embed.add_field(name=save_result, value="> 📬", inline=True)
                new_embed.add_field(name=contact,
                                    value=f"[Invite!]({invite}) | [Server]({server})\n{dev}: `{me}`", inline=False)
                new_embed.set_footer(text=page + f" {cur_page}/{pages}")
                await msg.edit(embed=new_embed)
                await msg.remove_reaction(reaction, user)

            else:
                await msg.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
            break


@client.event
async def on_command_error(ctx, error):
    if "KeyError" in str(error):
        with open("language.json", "r", encoding="utf-8") as f:
            lang = json.load(f)

        lang[str(ctx.guild.id)] = "en"

        with open("language.json", "w", encoding="utf-8") as f:
            json.dump(lang, f, indent=4)
        await ctx.send(embed=discord.Embed(title=f"Your server doesn't set any language!",
                                           description="set default to `en` 🇺🇸", color=discord.Colour.red()))
        return
    if get_language(ctx) == "en":

        if isinstance(error, commands.errors.NSFWChannelRequired):
            nsfw_warn = "⚠ This is not `N S F W` channel!"
            await ctx.send(embed=discord.Embed(title=nsfw_warn, color=discord.Colour.from_rgb(225, 225, 0)))

        elif isinstance(error, commands.errors.CommandError):
            warn = "Type something wrong?"
            await ctx.send(embed=discord.Embed(title=warn, description="> maybe `typos` somewhere...",
                                               color=discord.Colour.from_rgb(225, 225, 0)))

        else:
            genre_warn = "Something wrong!"
            await ctx.send(embed=discord.Embed(title=genre_warn,
                                               description="> [Contact the support?](https://discord.gg/3sAYuxc3aF)",
                                               color=discord.Colour.from_rgb(225, 225, 0)))
    else:
        if isinstance(error, commands.errors.NSFWChannelRequired):
            nsfw_warn = "⚠ ที่นี่ไม่ใช่ช่อง ` NSFW `"
            await ctx.send(embed=discord.Embed(title=nsfw_warn,
                                               color=discord.Colour.from_rgb(225, 225, 0)))
        elif isinstance(error, commands.errors.CommandError):
            warn = "พิมพ์ผิดหรือคร้าบบ?"
            await ctx.send(embed=discord.Embed(title=warn,
                                               description="> อาจ `ผิด` ก็ได้นะ",
                                               color=discord.Colour.from_rgb(225, 225, 0)))
        else:
            genre_warn = "ระบบมีปัญหา!"
            await ctx.send(embed=discord.Embed(title=genre_warn,
                                               description="> [ติดต่อผม](https://discord.gg/3sAYuxc3aF)",
                                               color=discord.Colour.from_rgb(225, 225, 0)))

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
# client.run('ODg0Njk1Mjg2MDcxNTg2ODU3.YTcOsQ.WL5NqEvyozbxHjMevICJOSnKMro')
