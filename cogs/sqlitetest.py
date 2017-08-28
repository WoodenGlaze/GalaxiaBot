import discord
import sqlite3


from discord.ext import commands
from cogs.utils import checks


class StatsTest:


	def __init__(self, bot):
		self.bot = bot


	@commands.command(hidden=True)
	@checks.is_owner()
	async def nuke(self):
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		c.execute('''DROP TABLE stats''')
		c.execute('''CREATE TABLE stats
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             user text, 
             uid numeric, 
             rep real NOT NULL DEFAULT 0, 
             thanks real NOT NULL DEFAULT 0,
             currency INTERGER NOT NULL DEFAULT 0)''')
		conn.commit()
		conn.close()	
		await self.bot.say('Nuked table and remade it!')

	@commands.command(hidden=True)
	@checks.is_owner()
	async def cdb(self):
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		c.execute('''CREATE TABLE stats
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             user text, 
             uid numeric, 
             rep real NOT NULL DEFAULT 0, 
             thanks real NOT NULL DEFAULT 0,
             currency INTERGER NOT NULL DEFAULT 0)''')

		conn.commit()
		conn.close()
		await self.bot.say('Created Database.')


	@commands.command(pass_context=True)
	async def register(self, ctx):
		"""Test Register"""
		auid = ctx.message.author.id
		id = None
		user = str(ctx.message.author.name)
		uid = int(ctx.message.author.id)
		rep = '0'
		thanks = '0'
		currency = '0'
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		for row in c.execute('SELECT uid FROM stats WHERE uid = ("%s")' % ctx.message.author.id):
			await self.bot.say(row)
			await self.bot.say('Already registered.')
			conn.close()
		else:
			c.execute("INSERT INTO stats VALUES (?, ?, ?, ?, ?, ?)", (id, user, uid, rep, thanks, currency))
			await self.bot.say('Registered!')
			conn.commit()
			conn.close()


	@commands.command()
	async def test(self):
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		for row in c.execute('SELECT * FROM stats ORDER BY user'):
			await self.bot.say(row)
		conn.close()


	@commands.command(pass_context=True)
	async def rep(self, ctx, mem:discord.Member):
		"""Test reputation command"""
		user = mem.name
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		if mem.id == ctx.message.author.id:
			await self.bot.say("You cannot give yourself a reputation point!")
		else:
			c.execute("UPDATE stats SET rep = rep + 1 WHERE uid = ('%s')" % mem.id)
			await self.bot.say('{0.name} has given {1.name} a reputation point!'.format(ctx.message.author, mem))
			conn.commit()
			conn.close()






def setup(bot):
	bot.add_cog(StatsTest(bot))