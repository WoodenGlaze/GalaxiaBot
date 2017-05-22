from discord.ext import commands
from .utils import checks
import discord
import inspect
import asyncio


import datetime
from collections import Counter


class Botadmin:
	"""Admin only commands"""


	def __init__(self, bot):
		self.bot = bot


	@commands.command(hidden=True)
	@checks.is_owner()
	async def load(self, *, module : str):
		"""Loads a module"""
		try:
			self.bot.load_extension('cogs.'+module)
		except Exception as e:
			await self.bot.say('\N{PISTOL}')
			await self.bot.say('{}: {}'.format(type(e).__name__, e))
		else:
			await self.bot.say('\N{OK HAND SIGN}')


	@commands.command(Hidden=True)
	@checks.is_owner()
	async def unload(self, *, module : str):
		"""Unloads a module"""
		try:
			print('Unloading {}'.format(module))
			self.bot.unload_extension('cogs.'+module)
		except Exception as e:
			await self.bot.say('\N{PISTOL}')
			await self.bot.say('{}: {}'.format(type(e).__name__, e))
		else:
			await self.bot.say('\N{OK HAND SIGN}')


	@commands.command(name='reload', hidden=True)
	@checks.is_owner()
	async def _reload(self, *, module : str):
		"""Reloads a module"""
		try:
			self.bot.unload_extension('cogs.'+module)
			self.bot.load_extension('cogs.'+module)
		except Exception as e:
			await self.bot.say('\N{PISTOL}')
			await self.bot.say('{}: {}'.format(type(e).__name__, e))
		else:
			await self.bot.say('\N{OK HAND SIGN}')


def setup(bot):
	bot.add_cog(Botadmin(bot))