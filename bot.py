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
    """ Subclass """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = json.load(open(path('config.json'), 'r'))
        
    """ Events """

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='NoiseStorm: Crab Rave'))
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
        """ Plays Crab Rave when someone says crab rave """
        if 'crab rave' in message.content.lower():
            vc = await message.author.voice.channel.connect()
            # vc.play(discord.FFmpegPCMAudio(executable=ffmpegSource, source=sound))
            vc.play(discord.FFmpegPCMAudio(source=path('music', 'crabrave.mp3'), options='-loglevel fatal'))
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 0.2
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ When a user doesn't do what the crabs want """
        await ctx.send(f'Crabs have disagreed with your command: {error}')

    """ Commands """

    @comms.command()
    async def icon(self, ctx):
        """ Gives the Icon that the Crabs use """
        await ctx.send(self.bot.user.avatar_url)

    @comms.command()
    async def song(self, ctx):
        """ Gives the youtube video of Crab Rave """
        await ctx.send('https://youtu.be/LDU_Txk06tM')

    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        """ Makes the Crabs go back into their cave """
        printc('[WARNING]: RAVER IS LOGGING OUT')
        await ctx.bot.logout()


if __name__ == "__main__":
    bot = CrabRaver(command_prefix='crab ', help_command=None)
    bot.add_cog(MainCog(bot))
    bot.run(bot.config['discord'], bot=True, reconnect=True)
