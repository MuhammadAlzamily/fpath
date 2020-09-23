import discord
import praw
from discord.ext import commands
import random
import requests
import os
filehandle = open("commands.md")
filehandle = filehandle.read()
bot = commands.Bot(command_prefix='$', case_insensitive=True)
reddit = praw.Reddit(client_id=os.environ.get("praw_client_id"), client_secret=os.environ.get("praw_client_secret"),
                     user_agent="myredditbot1.0")


adult_subs = ['ass', 'boobs', 'nudes', 'milf', 'bdsm']
memes_subs = ['memes', 'dankmemes']
dad_jokes_subs = ['dadjokes']


@bot.event
async def on_ready():
    print("bot connected")
    print(bot.user)


myembed = discord.Embed(type="rich",
                        colour=discord.Color.dark_red(), description=filehandle)

myembed.set_image(
    url="https://cdn.pixabay.com/photo/2017/05/04/15/12/welcome-sign-2284312__340.jpg")


myembed.set_footer(text="Bot by: @Muhammad#2048",
                   icon_url="https://www.flaticon.com/premium-icon/icons/svg/895/895903.svg")


myembed.set_author(
    name="FPath", icon_url="https://www.flaticon.com/premium-icon/icons/svg/1183/1183664.svg")

myembed.add_field(name="$meme", value="Used to get a meme", inline=False)
myembed.add_field(
    name="$nsfw", value="Used to get a sexy pic of who knows what", inline=False)
myembed.add_field(name="$joke", value="For terrible dad jokes ", inline=False)
myembed.add_field(
    name="$covid [country]", value="For the latest stats of the country passed to the command, in case of multiple country names like New Zealand plz wrap them in quotation marks", inline=False)


@bot.event
async def on_member_join(member):
    myembed.title = f"Hello and welcome to {member.guild}"
    await member.send(embed=myembed)
    chan = discord.utils.get(member.guild.channels, name="general")
    await chan.send(f"{member.mention} hello and welcome, plz enjoy your time here and be nice to the others and that's pretty much it :)")


@bot.command()
async def nsfw(ctx):
    subreddit = reddit.subreddit(random.choice(adult_subs))
    top = subreddit.random()
    embed = discord.Embed(title=top.title)
    embed.set_image(url=top.url)
    await ctx.author.send(embed=embed)


@bot.command()
async def meme(ctx):
    subreddit = reddit.subreddit(random.choice(memes_subs))
    top = subreddit.random()
    embed = discord.Embed(title=top.title)
    embed.set_image(url=top.url)
    await ctx.send(embed=embed)


@bot.command()
async def joke(ctx):
    subreddit = reddit.subreddit(random.choice(dad_jokes_subs))
    top = subreddit.random()
    thejoke = f"{top.title} {top.selftext}"
    await ctx.send(thejoke)


headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "6f8f5d760bmsh67db04f0c711434p11b987jsne23a91fa6cc9"
}

url = "https://covid-19-data.p.rapidapi.com/country"


@bot.command()
async def covid(ctx, arg):
    cases = discord.Embed(type='rich', color=discord.Color.dark_blue())
    cases.set_thumbnail(
        url="https://cdn.pixabay.com/photo/2020/03/19/21/35/covid-4948866__340.jpg")
    cases.set_footer(text="Stay home please")
    cases.set_author(name="COVID-19 data",
                     icon_url="https://rapidapi-prod-collections.s3.amazonaws.com/50ac3a55-4378-4965-a9a4-80bc9d05ac7a.jpg")
    querystring = {"format": "json", "name": arg}
    resp = requests.get(url=url, headers=headers, params=querystring)
    resp = resp.json()[0]
    for k, v in resp.items():
        cases.add_field(name=k, value=v, inline=False)
    await ctx.send(embed=cases)
bot.run("NzUzNjEwMDY4MjI1OTQ5NzY4.X1osEQ.6lKqDGgiv1AjmNxKN5HdCynT_JI")
