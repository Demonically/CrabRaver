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
        """ """
        if 'crab rave' in message.content.lower():
            vc = await message.author.voice.channel.connect()
            # Source to ffmpeg executable
            ffmpegSource = path('C:', 'Users', 'Xithr', 'Documents', 'ffmpeg', 'bin', 'ffmpeg.exe')
            # Music
            sound = path('music', 'crabrave.mp3')
            vc.play(discord.FFmpegPCMAudio(executable=ffmpegSource, source=sound))
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 0.1
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

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
    async def leave(self, ctx):
        pass # I'll put something here so the bot can leave a voice channel

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
