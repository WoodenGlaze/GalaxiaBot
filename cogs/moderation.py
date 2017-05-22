import discord
from discord.ext import commands


class Moderation:


	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	@commands.has_permissions(kick_members = True)
	async def kick(self, mem:discord.Member):
		await self.bot.kick(mem)
		await self.bot.say('Kicked member: {0.name}'.format(mem))


	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, mem:discord.Member):
		await self.bot.ban(mem)
		print('Banned user: {0.name}'.format(mem))

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setrole(self, mem:discord.Member, role:discord.Role):
		await self.bot.add_roles(mem, role)
		await self.bot.say('Added {0.name} to {1.name}'.format(role, mem))


def setup(bot):
	bot.add_cog(Moderation(bot))