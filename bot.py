"""
>> CrabRaver
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import json
import asyncio

from discord.ext import commands as comms
import discord

from output import path, now, printc


class CrabRaver(comms.Bot):
    """ """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = json.load(open(path('config.json'), 'r'))
        
    """ Events """

    async def on_ready(self):
        printc('[ ! ]: RAVER IS READY TO CRAB')


class MainCog(comms.Cog):
    """ """

    def __init__(self, bot):
        """ Objects: 
        comms.Bot subclass as an attribute
        """
        self.bot = bot

    """ Events """

    @comms.Cog.listener()
    async def on_message(self, message):
        """ """
        if 'Crab Rave' in message.content:
            try:
                vc = await message.author.voice.channel.connect()
                vc.play(discord.FFmpegPCMAudio(path('music', 'crabrave.mp3')))
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 0.25
                while vc.is_playing():
                    await asyncio.sleep(1)
                vc.stop()
            except asyncio.TimeoutError:
                printc(f'Connecting to channel: <{channel}> timed out.')


    """ Commands """

    @comms.command()
    async def icon(self, ctx):
        """ """
        await ctx.send(self.bot.user.avatar_url)

    @comms.command()
    async def song(self, ctx):
        """ """
        await ctx.send('https://youtu.be/LDU_Txk06tM')

    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        """ """
        printc('[WARNING]: RAVER IS LOGGING OUT')
        await ctx.bot.logout()


if __name__ == "__main__":
    bot = CrabRaver(command_prefix='!', help_command=None)
    bot.add_cog(MainCog(bot))
    bot.run(bot.config['discord'], bot=True, reconnect=True)
