import asyncio
from datetime import timedelta, datetime, timezone
from encodings import aliases
import discord
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


n_gif = "https://cdn.discordapp.com/attachments/1241067234768453636/1334954745109942373/thomas-yapping-about.gif"
bot = commands.Bot(command_prefix="&", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


@bot.event
async def on_message(m):
    if m.author == bot.user: return
    print(f"Message from {m.author} : {m.content}")

    if m.content.lower().startswith("hello"):
        await m.channel.send(f"hello {m.author}")
    if m.content == "123":
        await m.channel.send("456")

    await bot.process_commands(m)


@bot.command()
async def echo(ctx, *, text: str):
    await ctx.send(text)

@bot.command(aliases=["gif"])
async def n(ctx):
    await ctx.send(n_gif)

@bot.command()
async def embed(ctx):
    e = discord.Embed(title="title for embed", description="description for embed", color=discord.Color.brand_green())
    e.add_field(name="field 1 title", value="field 1 description", inline=False)
    e.add_field(name="field 2 title", value="field 2 description", inline=True)
    e.add_field(name="field 3 title", value="field 3 in the same line as field 2", inline=True)
    e.set_footer(text="footer text")
    e.set_author(name="author name")
    await ctx.send(embed=e)

@bot.command()
async def longembed(ctx):
    e = discord.Embed(title="long embed", description="", color=discord.Color.brand_green())
    for i in range(1, 26):
        e.add_field(name=f"field {i}", value=f"value {i}", inline=False)
    await ctx.send(embed=e)

@bot.command()
async def lemur(ctx):
    e = discord.Embed(title="ring tailed lemur", description="cool animal", color=discord.Color.light_grey(), url="https://en.wikipedia.org/wiki/Ring-tailed_lemur")
    e.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Ringtailed_lemurs.jpg/1280px-Ringtailed_lemurs.jpg")
    await ctx.send(embed=e)

@bot.command(aliases=["page"])
async def website(ctx):
    await ctx.send(f"Eternal Academy website : https://00santi.github.io/eternal-academy/")

class View(discord.ui.View):
    @discord.ui.button(label="button 1", style=discord.ButtonStyle.blurple)
    async def on_click(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.send_message("button clicked")

@bot.command()
async def button(ctx):
    v = View()
    await ctx.send(view=v)

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="option 1", description="description 1"),
            discord.SelectOption(label="option 2", description="description 2"),
            discord.SelectOption(label="option 3", description="description 3"),
            discord.SelectOption(label="option 4", description="description 4")
        ]
        super().__init__(placeholder="placeholder text", min_values=1, max_values=1, options=options)

    async def callback(self, i: discord.Interaction):
        await i.response.send_message(f"{self.values[0]} picked")

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

@bot.command()
async def dropdown(ctx):
    await ctx.send(view=MenuView())

@bot.command(name="mute", aliases=["mutecommand", "timeout", "mutethomas"])
async def mute(ctx):
    guild = ctx.guild
    target1 = guild.get_member(1209457903602237442)
    target2 = guild.get_member(1012357842721832961)

    if not target1 or not target2:
        await ctx.send("Couldn't find one or both target users.")
        return

    timeout_until = datetime.now(timezone.utc) + timedelta(minutes=1)

    for target in [target1, target2]:
        try:
            await target.edit(timed_out_until=timeout_until, reason=f"muted by {ctx.author}")
            await ctx.send(f"{target.display_name} has been muted for 1 minute")
        except discord.Forbidden:
            await ctx.send(f"no permission to mute {target.display_name}.")
        except Exception as e:
            await ctx.send(f"error muting {target.display_name}: {e}")

    await asyncio.sleep(60)

    for target in [target1, target2]:
        try:
            await target.edit(timed_out_until=None, reason="unmute after 1 minute")
            await ctx.send(f"{target.display_name} has been unmuted")
        except Exception as e:
            await ctx.send(f"error unmuting {target.display_name}: {e}")

@bot.command(name="help", aliases=["commands"])
async def help(ctx):
    help_text = """
`&help` - show this help message
`&mute` - mute thomas 1 minute
`&n` or `&gif` - thomas yapping about gif
`&website` - get eternal academy website
`&lemur` - lemur
"""
    await ctx.send(help_text)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)