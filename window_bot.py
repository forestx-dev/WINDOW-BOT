import discord
import time
from discord.ext import commands

bot = commands.Bot(command_prefix="w.", description="STILL IN DEVELOPMENT. The development started recently, bot will be finished as soon as possible")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="something"))

@bot.command()
async def ping(ctx):
    """Runs the connection test to discord."""
    start = time.monotonic()
    msg = await ctx.send('Pinging...')
    millis = (time.monotonic() - start) * 1000

    # Since sharded bots will have more than one latency, this will average them if needed.
    heartbeat = ctx.bot.latency * 1000

    await msg.edit(content=f'Heartbeat: {heartbeat:,.2f}ms\tACK: {millis:,.2f}ms.')

@bot.command(pass_context=True, hidden=True)
async def exec(self, ctx, *, code : str):
    adminids = [361948178573950985]

    if ctx.author.id not in adminids:
        return
    
    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    env = {
        'bot': bot,
        'ctx': ctx,
        'message': ctx.message,
        'server': ctx.message.server,
        'channel': ctx.message.channel,
        'author': ctx.message.author
    }

    env.update(globals())

    try:
        result = eval(code, env)
        if inspect.isawaitable(result):
            result = await result
    except Exception as e:
        await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
        return

    await ctx.send(python.format(result))

@bot.command(pass_context=True)
async def say(ctx, *, something : str):
    if(something is None):
        await ctx.send("What do u want to say??")
        return

    await ctx.send(something)
    await ctx.bot.delete_message(ctx.message.author)

bot.run("NDYxNjE1OTQ3MjM3Njg3MzI2.DhYk5g.pMWZvYQ02VlVPacVWI-nZG3bT_g")
