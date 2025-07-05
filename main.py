import os

from Scripts.rst2odt import description
from colorama import Fore
import colorama
import requests
import discord

INTENTS = discord.Intents.all()
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

bot = discord.Bot(intents=INTENTS)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='ping', description='Check the bot\'s latency')
async def ping(ctx):
    await ctx.defer(ephemeral=True)
    async with ctx.channel.typing():
        latency = round(bot.latency * 1000)

        embed = discord.Embed(
            title="Bot Latency",
            description=f"**Latency:** {latency}ms",
            color=discord.Color.green()
        )
        await ctx.followup.send(embed=embed)

@bot.command(name='server-info', description="Check the LDigital Infrastructure Status")
async def server_info(ctx: discord.ApplicationContext):
    await ctx.defer()
    async with ctx.channel.typing():
        discord_latency = round(bot.latency * 1000)

        def get_ams1_latency():
            # Ping AMS-1 host



if __name__ == '__main__':
    bot.run(os.environ['DISCORD_TOKEN'])