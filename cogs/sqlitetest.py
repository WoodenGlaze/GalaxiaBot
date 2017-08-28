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
			new = str(row).replace("(","").replace(",","").replace("'","").replace(")","")
			await self.bot.say(new)
		conn.close()


	@commands.command(pass_context=True)
	async def user(self, ctx, member:discord.Member = None):
		"""Gets user information"""
		conn = sqlite3.connect('C:/Users/Dion/Desktop/GalaxiaBot/cogs/DB/stats.db')
		c = conn.cursor()
		emmem1 = discord.Embed(title='Member Information')
		emmem2 = discord.Embed(title='Member Information')

		if member is None:
			member = ctx.message.author

		for row in c.execute('SELECT uid FROM stats WHERE uid = ("%s")' % ctx.message.author.id):
			for reputation in c.execute('SELECT rep FROM stats WHERE uid = ("%s")' % member.id):
				rep = reputation
			for thanks in c.execute('SELECT thanks FROM stats WHERE uid = ("%s")' % member.id):
				tnx = thanks
			for currency in c.execute('SELECT currency FROM stats WHERE uid = ("%s")' % member.id):
				cur = currency
			emmem1.set_author(name='{0.display_name}'.format(member), icon_url='{}'.format(member.avatar_url or member.default_avatar_url))
			emmem1.set_thumbnail(url='{0.avatar_url}'.format(member))
			emmem1.add_field(name='User ID:', value='{0.id}'.format(member), inline=True)
			emmem1.add_field(name='Created at:', value='{0.created_at}'.format(member), inline=True)
			emmem1.add_field(name='Joined at:', value='{0.joined_at}'.format(member), inline=True)
			emmem1.add_field(name='Reputation:', value='{}'.format(str(rep).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Thanks:', value='{}'.format(str(tnx).replace("(","").replace(",","").replace("'","").replace(")","")))		
			emmem1.add_field(name='Money:', value='{}'.format(str(cur).replace("(","").replace(",","").replace("'","").replace(")","")))
			await self.bot.say(embed=emmem1)
			conn.close()
		else:
			emmem2.set_author(name='{0.display_name}'.format(member), icon_url='{}'.format(member.avatar_url or member.default_avatar_url))
			emmem2.set_thumbnail(url='{0.avatar_url}'.format(member))
			emmem2.add_field(name='User ID:', value='{0.id}'.format(member), inline=True)
			emmem2.add_field(name='Created at:', value='{0.created_at}'.format(member), inline=True)
			emmem2.add_field(name='Joined at:', value='{0.joined_at}'.format(member), inline=True)
			await self.bot.say(embed=emmem2)



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