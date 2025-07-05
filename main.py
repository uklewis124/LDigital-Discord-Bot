import os

from colorama import Fore
import colorama
import requests
import discord
import asyncio
import aioping

INTENTS = discord.Intents.all()
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

bot = discord.Bot(intents=INTENTS)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='server-info', description="Check the LDigital Infrastructure Status", integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
async def server_info(ctx: discord.ApplicationContext):
    await ctx.defer()

    async def fetch_status():
        discord_latency = round(bot.latency * 1000)

        async def get_ams1_latency():
            try:
                delay = await aioping.ping("ams-1.ldigital.dev", timeout=3)
                return round(delay * 1000, 2)
            except (TimeoutError, OSError):
                return None

        async def get_ams2_latency():
            try:
                delay = await aioping.ping("node2.ldigital.dev", timeout=3)
                return round(delay * 1000, 2)
            except (TimeoutError, OSError):
                return None

        async def get_ams3_latency():
            try:
                delay = await aioping.ping("ams-3.ldigital.dev", timeout=3)
                return round(delay * 1000, 2)
            except (TimeoutError, OSError):
                return None

        async def get_dus1_latency():
            try:
                delay = await aioping.ping("dus-1.ldigital.dev", timeout=3)
                return round(delay * 1000, 2)
            except (TimeoutError, OSError):
                return None

        ams1_latency, ams2_latency, ams3_latency, dus1_latency = await asyncio.gather(
            get_ams1_latency(),
            get_ams2_latency(),
            get_ams3_latency(),
            get_dus1_latency()
        )

        embed = discord.Embed(
            title="LDigital Infrastructure Status",
            description="Current latency to LDigital infrastructure.",
            color=discord.Color.blue()
        )
        embed.add_field(name="AMS-1 Latency", value=f"{ams1_latency} ms" if ams1_latency is not None else "Offline",
                        inline=False)
        embed.add_field(name="AMS-2 Latency", value=f"{ams2_latency} ms" if ams2_latency is not None else "Offline",
                        inline=False)
        embed.add_field(name="AMS-3 Latency", value=f"{ams3_latency} ms" if ams3_latency is not None else "Offline",
                        inline=False)
        embed.add_field(name="DUS-1 Latency", value=f"{dus1_latency} ms" if dus1_latency is not None else "Offline",
                        inline=False)
        embed.add_field(name="Discord Latency", value=f"{discord_latency} ms", inline=False)
        embed.set_footer(text="LDigital Bot | Developed by LDigital Team")
        await ctx.followup.send(embed=embed)

    try:
        async with ctx.channel.typing():
            await fetch_status()
    except discord.errors.Forbidden:
        await fetch_status()



if __name__ == '__main__':
    bot.run(os.environ['DISCORD_TOKEN'])