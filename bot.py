#Made by:

print("""
.########..#######..##....##.##....##......####.............##....###....##....##.########......##.##.......#######..########.##..........#####..
....##....##.....##.###...##..##..##......##..##............##...##.##...##...##..##............##.##......##.....##.##.......##....##...##...##.
....##....##.....##.####..##...####........####.............##..##...##..##..##...##..........#########....##........##.......##....##..##.....##
....##....##.....##.##.##.##....##........####..............##.##.....##.#####....######........##.##......########..#######..##....##..##.....##
....##....##.....##.##..####....##.......##..##.##....##....##.#########.##..##...##..........#########....##.....##.......##.#########.##.....##
....##....##.....##.##...###....##.......##...##......##....##.##.....##.##...##..##............##.##......##.....##.##....##.......##...##...##.
....##.....#######..##....##....##........####..##.....######..##.....##.##....##.########......##.##.......#######...######........##....#####..
.########..########..########..######..########.##....##.########..##.                                                                           
.##.....##.##.....##.##.......##....##.##.......###...##....##....####                                                                           
.##.....##.##.....##.##.......##.......##.......####..##....##.....##.                                                                           
.########..########..######....######..######...##.##.##....##........                                                                           
.##........##...##...##.............##.##.......##..####....##.....##.                                                                           
.##........##....##..##.......##....##.##.......##...###....##....####                                                                           
.##........##.....##.########..######..########.##....##....##.....##.  """)

print('-------')

print("""
   _____           _                  _             ____            _   
  / ____|         | |                (_)           |  _ \          | |  
 | |  __    __ _  | |   __ _  __  __  _    __ _    | |_) |   ___   | |_ 
 | | |_ |  / _` | | |  / _` | \ \/ / | |  / _` |   |  _ <   / _ \  | __|
 | |__| | | (_| | | | | (_| |  >  <  | | | (_| |   | |_) | | (_) | | |_ 
  \_____|  \__,_| |_|  \__,_| /_/\_\ |_|  \__,_|   |____/   \___/   \__|
""")
print('-------')


#Importing main modules
import discord
import asyncio
import datetime
import json
import youtube_dl
import inspect
import io
import traceback
import textwrap


#importing extensions.
from contextlib import redirect_stdout
from cogs.utils import checks
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime


#bot starts here:
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


initial_extensions = [
    'cogs.moderation',
    'cogs.botadmin',


]


if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        
        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester or '231522942868127744' or '197818276305305602' or '244531479462412288':
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))


version = '0.0.2b'


#define credentials file + open it.
def load_credentials():
	with open('config.json') as f:
		return json.load(f)


#Gets info from credentials.json
if True == True:
	credentials = load_credentials()
	token = credentials['token']
	status = credentials['status']
	botowner = credentials['botowner']
	shards = credentials['sharding']


#define bot and prefix
description = """Galaxia Private Bot \n type g)help for a list of commands."""


bot = Bot(command_prefix=commands.when_mentioned_or('g)', 'db)'), description=description)


#bot.add_cog(Utility(bot))
#bot.add_cog(Permissions(bot))
#bot.add_cog(Beta(bot))
#bot.add_cog(REPL(bot))
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print('Logged in as: {0.name} (ID:{0.id})'.format(bot.user))
    print(version)
    print('------')
    print('Sharding:')
    print(bot.shard_count)
    print('------')
    await bot.change_presence(game=discord.Game(name='{}'.format(status,)), status=discord.Status.dnd)


@bot.event
async def on_resumed():
	print('Connection was lost but is back again.')


@bot.event
async def on_member_join(member):
	server = member.server
	await bot.set_roles(member, discord.Object(316201434561642496))


@bot.event
async def on_member_ban(member):
	server = member.server
	
	
	print('{} got banned'.format(member))
	
	
	embanned = discord.Embed(title='Banned!')
	embanned.add_field(name='Banned user:', value='{}'.format(member))
	embanned.set_image(url='https://static1.comicvine.com/uploads/original/11123/111235780/5258653-gtfo-iron-man-vs.-thor-gif.gif')
	embanned.set_footer(text='{0.display_name} (ID: {0.id})'.format(member))
	

	await client.send_message(server, embed=embanned)


@bot.event
async def on_server_join(server):
	print('joined {}'.format(server.name))
	osjembed = discord.Embed(title='Hello, I am {0.name}!'.format(bot.user), description='Hello, I was invited to {0.name} by an admin. \n you can invoke commands by pinging me and saying help \n EXAMPLE: ```@{1.name} help``` or by saying `g)help!`'.format(server, bot.user))
	osjembed.add_field(name='How to invoke commands:', value='g)help or @{0.name} help')
	osjembed.add_field(name='Version:', value=version)
	await bot.send_message(server, embed=osjembed)


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))





bot.run(token)