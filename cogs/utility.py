from discord.ext import commands
from .utils import checks
from cogs.utils import checks
import discord
import inspect
import asyncio
import datetime
import git
from PythonGists import PythonGists

version = '0.0.3a'



class Utility:
	"""All bot related info
	"""


	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def botinfo(self):
		"""Info about the bot"""
		owner = 'Tony Stark (Sara\'s Bad Wolf)#4827'
		owner_avatar = 'https://images-ext-1.discordapp.net/.eJwNwtsNwyAMAMBdGACHh8GwjYtFkqptEND-VNk90d1ffftLZbXN2UYGKPLRso9ydOHWdDnewD-e3AeYJXjrkvXBeLwtBIKRmDFJYLJID0ccsUZvaky2iuhnW9V5AUSEHkA.SpVN-eueYIiLbVPrnQG1KYS-7iY?width=80&height=80'
		emin = discord.Embed(title='Bot Info')
		emin.set_author(name='{}'.format(owner), icon_url='{}'.format(owner_avatar))
		emin.set_thumbnail(url='https://cdn.discordapp.com/attachments/315980889253347328/315991418441170944/unknown.png')
		emin.add_field(name='Version', value=version)
		emin.add_field(name='Library Version:', value=discord.__version__)
		emin.add_field(name='Made for:', value='The Galaxia server')
		emin.add_field(name='Inspiration:', value='<@130512502302834688>')
		emin.add_field(name='Author:', value=owner)
		await self.bot.say(embed=emin)


	@commands.command(pass_context=True)
	async def about(self, ctx, txt: str =None):
		"""New about command."""
		if txt != 'short':
			em = discord.Embed(color=0x42f4df, title='Galaxia Bot V2',
				description='Galaxia is an allround bot, with stats, user info and other useful information!')
			em.add_field(name='Contribute here:',
				value='[Github link](https://github.com/WoodenGlaze/GalaxiaBot)')
			em.add_field(name='Quick Examples:', value='g)user, g)register, g)play')
			if txt == 'link': em.add_field(name='Official Discord Server:', value='Join the official Discord server [here](https://discord.gg/rK4M7st)')
			em.set_footer(text='Made by Hopes and Dreams#4827 & 𝕁𝕒𝕜𝕠𝕓#5771', icon_url='http://i.imgur.com/e5L7fJr.png')
			await self.bot.say(content=None, embed=em)
		else:
			await self.bot.say('https://github.com/WoodenGlaze/GalaxiaBot')


#	@commands.command(pass_context=True)
#	async def user(self, ctx, member:discord.Member = None):
#		"""Gets user information"""
#		emmem = discord.Embed(title='Member Information')
#
#
#		if member is None:
#			member = ctx.message.author
#
#
#		emmem.set_author(name='{0.display_name}'.format(member), icon_url='{}'.format(member.avatar_url or member.default_avatar_url))
#		emmem.set_thumbnail(url='{0.avatar_url}'.format(member))
#		emmem.add_field(name='User ID:', value='{0.id}'.format(member), inline=True)
#		emmem.add_field(name='Created at:', value='{0.created_at}'.format(member), inline=True)
#		emmem.add_field(name='Joined at:', value='{0.joined_at}'.format(member), inline=True)
#
#
#		await self.bot.say(embed=emmem)


	@commands.command(hidden=True)
	@checks.is_owner()
	async def echo(self, message, ttson=None):
		ttsarg = False
		if ttson == None:
			ttsarg = False
		else:
			ttsarg = True
		await self.bot.say(message, tts=ttsarg)


	@commands.command(pass_context=True)
	@commands.has_permissions(manage_nicknames = True)
	async def cn(self, ctx, nickname, member:discord.Member=None):
		"""Change nicknames of a person, must be lower than bot."""
		if member is None:
			member = ctx.message.author
		await self.bot.change_nickname(member, nickname)


	"""@commands.command()
	async def prefixes(self):
		await self.bot.say(prefix)"""


	@commands.command()
	async def oauth(self):
		"""Gives OAuth link"""
		emoauth = discord.Embed(title='OAuth invite link')
		client_id =  self.bot.user.id
		oauth = discord.utils.oauth_url(client_id, permissions=discord.Permissions.all(), server=None)
		emoauth.add_field(name='Link', value='{}'.format(oauth))
		await self.bot.say(embed=emoauth)


	@commands.command(pass_context=True)
	async def status(self, ctx):
        """Bot stats."""
        uptime = (datetime.datetime.now() - self.bot.uptime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            time = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
        else:
            time = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
        game = self.bot.game
        if not game:
            game = 'None'
        channel_count = 0
        for guild in self.bot.guilds:
            channel_count += len(guild.channels)

		em = discord.Embed(title='Bot Stats', color=0x32441c)
		em.add_field(name=u'\U0001F553 Uptime', value=time, inline=False)
		em.add_field(name=u'\U0001F4E4 Msgs sent', value=str(self.bot.icount))
		em.add_field(name=u'\U0001F4E5 Msgs received', value=str(self.bot.message_count))
		em.add_field(name=u'\u2757 Mentions', value=str(self.bot.mention_count))
		em.add_field(name=u'\u2694 Servers', value=str(len(self.bot.guilds)))
		em.add_field(name=u'\ud83d\udcd1 Channels', value=str(channel_count))
		em.add_field(name=u'\u270F Keywords logged', value=str(self.bot.keyword_log))
		g = u'\U0001F3AE Game'
		if '=' in game: g = '\ud83c\udfa5 Stream'
			em.add_field(name=g, value=game)
		mem_usage = '{:.2f} MiB'.format(__import__('psutil').Process().memory_full_info().uss / 1024 ** 2)
		em.add_field(name=u'\U0001F4BE Memory usage:', value=mem_usage)
		try:
			g = git.cmd.Git(working_dir=os.getcwd())
			branch = g.execute(["git", "rev-parse", "--abbrev-ref", "HEAD"])
			g.execute(["git", "fetch", "origin", branch])
			version = g.execute(["git", "rev-list", "--right-only", "--count", "{}...origin/{}".format(branch, branch)])
			if branch == "master":
				branch_note = "."
			else:
				branch_note = " (`" + branch + "` branch)."
			if version == '0':
				status = 'Up to date%s' % branch_note
			else:
			latest = g.execute(
				["git", "log", "--pretty=oneline", "--abbrev-commit", "--stat", "--pretty", "-%s" % version,
 				"origin/%s" % branch])
			gist_latest = PythonGists.Gist(description='Latest changes for the selfbot.', content=latest,
											name='latest.txt')
			if version == '1':
				status = 'Behind by 1 release%s [Latest update.](%s)' % (branch_note, gist_latest)
			else:
				status = '%s releases behind%s [Latest updates.](%s)' % (version, branch_note, gist_latest)
			em.add_field(name=u'\U0001f4bb Update status:', value=status)
            except:
                pass
            await ctx.send(content=None, embed=em)
        else:
            msg = '**Bot Stats:** ```Uptime: %s\nMessages Sent: %s\nMessages Received: %s\nMentions: %s\nguilds: %s\nKeywords logged: %s\nGame: %s```' % (
            time, str(self.bot.icount), str(self.bot.message_count), str(self.bot.mention_count),
            str(len(self.bot.guilds)), str(self.bot.keyword_log), game)
            await ctx.send(self.bot.bot_prefix + msg)
        await ctx.message.delete()		


def setup(bot):
	bot.add_cog(Utility(bot))