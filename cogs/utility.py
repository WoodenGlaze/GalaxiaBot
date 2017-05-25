from discord.ext import commands
from .utils import checks
import discord
import inspect
import asyncio


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
	async def user(self, ctx, member:discord.Member = None):
		"""Gets user information"""
		emmem = discord.Embed(title='Member Information')


		if member is None:
			member = ctx.message.author


		emmem.set_author(name='{0.display_name}'.format(member), icon_url='{}'.format(member.avatar_url or member.default_avatar_url))
		emmem.set_thumbnail(url='{0.avatar_url}'.format(member))
		emmem.add_field(name='User ID:', value='{0.id}'.format(member), inline=True)
		emmem.add_field(name='Created at:', value='{0.created_at}'.format(member), inline=True)
		emmem.add_field(name='Joined at:', value='{0.joined_at}'.format(member), inline=True)


		await self.bot.say(embed=emmem)


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


#	@commands.command()
#	async def oauth(self):
#		"""Gives OAuth link"""
#		emoauth = discord.Embed(title='OAuth invite link')
#		client_id =  self.bot.user.id
#		oauth = discord.utils.oauth_url(client_id, permissions=discord.Permissions.all(), server=None)
#		emoauth.add_field(name='Link', value='{}'.format(oauth))
#		await self.bot.say(embed=emoauth)


def setup(bot):
	bot.add_cog(Utility(bot))