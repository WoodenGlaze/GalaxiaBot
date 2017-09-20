import discord
from discord.ext import commands


class Moderation:


	def __init__(self, bot):
		self.bot = bot
    	b = DBans(token="CAXOsqkioa")

	@commands.command()
	@commands.has_permissions(kick_members = True)
	async def kick(self, mem:discord.Member):
		"""Kicks a user"""
		await self.bot.kick(mem)
		await self.bot.say('Kicked member: {0.name}'.format(mem))


	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, mem:discord.Member):
		"""Bans a user."""
		await self.bot.ban(mem)
		print('Banned user: {0.name}'.format(mem))

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setrole(self, mem:discord.Member, role:discord.Role):
		"""Sets a users role, Usage: g)setrole [User] [Role Name Including Caps]"""
		await self.bot.add_roles(mem, role)
		await self.bot.say('Added {0.name} to {1.name}'.format(role, mem))


	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def check(self, mem:discord.Member):
		status = b.lookup(member.id)
		checkembed = discord.Embed(title='Member ban status')
		checkembed.add_field(name='Member ID:', value='{}'.format(member.id))
		checkembed.add_field(name='Global ban status:', value='{}'.format(status))
		await bot.send_message(channel, embed=checkembed)



def setup(bot):
	bot.add_cog(Moderation(bot))