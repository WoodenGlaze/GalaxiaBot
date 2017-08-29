import discord
import sqlite3
from discord.ext import commands
from cogs.utils import checks
db = '/opt/Galaxia/GalaxiaBot/DB/warframe.db'


class warframe:


	def __init__(self, bot):
		self.bot = bot


	@commands.command(hidden=True)
	@checks.is_owner()
	async def wfnuke(self):
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		c.execute('''DROP TABLE stats''')
		c.execute('''CREATE TABLE stats
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             user text, 
             uid numeric, 
             warframe text,
             level INTEGER,
			 mod1 text,
			 mod2 text,
			 mod3 text,
			 mod4 text,
			 mod5 text,
			 mod6 text,
			 mod7 text,
			 mod8 text,
			 mod9 text,
			 mod10 text,
			 mod1l text,
			 mod2l text,
			 mod3l text,
			 mod4l text,
			 mod5l text,
			 mod6l text,
			 mod7l text,
			 mod8l text,
			 mod9l text,
			 mod10l text)''')
		conn.commit()
		conn.close()	
		await self.bot.say('Nuked table and remade it!')

	@commands.command(hidden=True)
	@checks.is_owner()
	async def wfcdb(self):
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		c.execute('''CREATE TABLE stats
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             user text, 
             uid numeric, 
             warframe text,
             level INTEGER,
			 mod1 text,
			 mod2 text,
			 mod3 text,
			 mod4 text,
			 mod5 text,
			 mod6 text,
			 mod7 text,
			 mod8 text,
			 mod9 text,
			 mod10 text,
			 mod1l INTEGER,
			 mod2l INTEGER,
			 mod3l INTEGER,
			 mod4l INTEGER,
			 mod5l INTEGER,
			 mod6l INTEGER,
			 mod7l INTEGER,
			 mod8l INTEGER,
			 mod9l INTEGER,
			 mod10l INTEGER)''')

		conn.commit()
		conn.close()
		await self.bot.say('Created Database.')


	@commands.command(pass_context=True)
	async def wfregister(self, ctx, warframe=str('help'), level=None, mod1=None, mod2=None, mod3=None, mod4=None, mod5=None, mod6=None, mod7=None, mod8=None, mod9=None, mod10=None, mod1l=None, mod2l=None, mod3l=None, mod4l=None, mod5l=None, mod6l=None, mod7l=None, mod8l=None, mod9l=None, mod10l=None):
		"""Test Register"""
		auid = ctx.message.author.id
		id = None
		user = str(ctx.message.author.name)
		uid = int(ctx.message.author.id)
		if warframe == 'help':
			await self.bot.say('To register: \nType: g)wfregister (warframe name) (Warframe level) [Mod 1] [Mod 2] [Mod 3] [Mod 4] [Mod 5] [Mod 6] [Mod 7] [Mod 8] [Mod 9] [Mod 10] [Mod 1 level] [Mod 2 level] [Mod 3 level] [Mod 4 level] [Mod 5 level] [Mod 6 level] [Mod 7 level] [Mod 8 level] [Mod 9 level] [Mod 10 level]')
		else:
#			if mod1 = None:
#				mod1l = None
#			if mod2 = None:
#				mod2l = None
#			if mod3 = None:
#				mod3l = None
#			if mod4 = None:
#				mod4l = None
#			if mod5 = None:
#				mod5l = None
#			if mod6 = None:
#				mod6l = None
#			if mod7 = None:
#				mod7l = None
#			if mod8 = None:
#				mod8l = None
#			if mod9 = None:
#				mod9l = None
#			if mod10 = None:
#				mod10l = None
#Making some assumptions that when mods are not entered there is no level there.


			conn = sqlite3.connect('{}'.format(db))
			c = conn.cursor()
			for row in c.execute('SELECT uid FROM stats WHERE uid = ("%s")' % ctx.message.author.id):
				await self.bot.say('Already registered.')
				conn.close()
			else:
				c.execute("INSERT INTO stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, user, uid, warframe, level, mod1, mod2, mod3, mod4, mod5, mod6, mod7, mod8, mod9, mod10, mod1l, mod2l, mod3l, mod4l, mod5l, mod6l, mod7l, mod8l, mod9l, mod10l))
				await self.bot.say('Registered!')
				conn.commit()
				conn.close()


	@commands.command(pass_context=True)
	async def unregister(self, ctx):
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		for row in c.execute('SELECT * FROM stats WHERE uid = ("%s")' % ctx.message.author.id):
			c.execute('DELETE FROM stats WHERE uid = ("%s")' % ctx.message.author.id)
			await self.bot.say('Removed entry with from user: {0.name} ({0.id})'.format(ctx.message.author))
			conn.close()


	@commands.command()
	async def wftest(self):
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		for row in c.execute('SELECT * FROM stats ORDER BY user'):
			new = str(row).replace("(","").replace(",","").replace("'","").replace(")","")
			await self.bot.say(new)
		conn.close()


	@commands.command()
	async def wftest2(self):
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		for row in c.execute('SELECT * FROM warframes ORDER BY name'):
			new = str(row).replace("(","").replace(",","").replace("'","").replace(")","")
			await self.bot.say(new)
		conn.close()


	@commands.command(pass_context=True)
	async def wfuser(self, ctx, member:discord.Member = None):
		"""Gets user information"""
		conn = sqlite3.connect('{}'.format(db))
		c = conn.cursor()
		emmem1 = discord.Embed(title='Member Information')
		emmem2 = discord.Embed(title='Member Information')

		if member is None:
			member = ctx.message.author

		for row in c.execute('SELECT uid FROM stats WHERE uid = ("%s")' % ctx.message.author.id):
#Warfame
			for warframe in c.execute('SELECT warframe FROM stats WHERE uid = ("%s")' % member.id):
				wf = warframe
			for level in c.execute('SELECT level FROM stats WHERE uid = ("%s")' % member.id):
				wfl = level
			for icon in c.execute('SELECT icon_url FROM warframes WHERE name = ("%s")' % wf):
				pic = icon
#Mods
			for mod1 in c.execute('SELECT mod1 FROM stats WHERE uid = ("%s")' % member.id):
				wfm1 = mod1
			for mod2 in c.execute('SELECT mod2 FROM stats WHERE uid = ("%s")' % member.id):
				wfm2 = mod2
			for mod3 in c.execute('SELECT mod3 FROM stats WHERE uid = ("%s")' % member.id):
				wfm3 = mod3
			for mod4 in c.execute('SELECT mod4 FROM stats WHERE uid = ("%s")' % member.id):
				wfm4 = mod4
			for mod5 in c.execute('SELECT mod5 FROM stats WHERE uid = ("%s")' % member.id):
				wfm5 = mod5
			for mod6 in c.execute('SELECT mod6 FROM stats WHERE uid = ("%s")' % member.id):
				wfm6 = mod6
			for mod7 in c.execute('SELECT mod7 FROM stats WHERE uid = ("%s")' % member.id):
				wfm7 = mod7
			for mod8 in c.execute('SELECT mod8 FROM stats WHERE uid = ("%s")' % member.id):
				wfm8 = mod8
			for mod9 in c.execute('SELECT mod9 FROM stats WHERE uid = ("%s")' % member.id):
				wfm9 = mod9
			for mod10 in c.execute('SELECT mod10 FROM stats WHERE uid = ("%s")' % member.id):
				wfm10 = mod10
#Mod levels
			for mod1l in c.execute('SELECT mod1l FROM stats WHERE uid = ("%s")' % member.id):
				wfm1l = mod1l
			for mod2l in c.execute('SELECT mod2l FROM stats WHERE uid = ("%s")' % member.id):
				wfm2l = mod2l
			for mod3l in c.execute('SELECT mod3l FROM stats WHERE uid = ("%s")' % member.id):
				wfm3l = mod3l
			for mod4l in c.execute('SELECT mod4l FROM stats WHERE uid = ("%s")' % member.id):
				wfm4l = mod4l
			for mod5l in c.execute('SELECT mod5l FROM stats WHERE uid = ("%s")' % member.id):
				wfm5l = mod5l
			for mod6l in c.execute('SELECT mod6l FROM stats WHERE uid = ("%s")' % member.id):
				wfm6l = mod6l
			for mod7l in c.execute('SELECT mod7l FROM stats WHERE uid = ("%s")' % member.id):
				wfm7l = mod7l
			for mod8l in c.execute('SELECT mod8l FROM stats WHERE uid = ("%s")' % member.id):
				wfm8l = mod8l
			for mod9l in c.execute('SELECT mod9l FROM stats WHERE uid = ("%s")' % member.id):
				wfm9l = mod9l
			for mod10l in c.execute('SELECT mod10l FROM stats WHERE uid = ("%s")' % member.id):
				wfm10l = mod10l

			print(wf, wfl, wfm1, wfm1l, wfm2, wfm2l, wfm3, wfm3l, wfm4, wfm4l, wfm5, wfm5l, wfm6, wfm6l, wfm7, wfm7l, wfm8, wfm8l, wfm9, wfm9l, wfm10, wfm10l)
			emmem1.set_author(name='{0.display_name}'.format(member), icon_url='{}'.format(member.avatar_url or member.default_avatar_url))
			print(pic)
			emmem1.set_thumbnail(url=str(pic).replace("(","").replace(",","").replace("'","").replace(")",""))
			emmem1.add_field(name='Created at:', value='{0.created_at}'.format(member), inline=True)
			emmem1.add_field(name='Joined at:', value='{0.joined_at}'.format(member), inline=True)
			emmem1.add_field(name='Warframe:', value='{}'.format(str(wf).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Warframe Level:', value='{}'.format(str(wfl).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 1:', value='{0} : level {1}'.format(str(wfm1).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm1l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 2:', value='{0} : level {1}'.format(str(wfm2).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm2l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 3:', value='{0} : level {1}'.format(str(wfm3).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm3l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 4:', value='{0} : level {1}'.format(str(wfm4).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm4l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 5:', value='{0} : level {1}'.format(str(wfm5).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm5l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 6:', value='{0} : level {1}'.format(str(wfm6).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm6l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 7:', value='{0} : level {1}'.format(str(wfm7).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm7l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 8:', value='{0} : level {1}'.format(str(wfm8).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm8l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 9:', value='{0} : level {1}'.format(str(wfm9).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm9l).replace("(","").replace(",","").replace("'","").replace(")","")))
			emmem1.add_field(name='Mod 10:', value='{0} : level {1}'.format(str(wfm10).replace("(","").replace(",","").replace("'","").replace(")",""), str(wfm10l).replace("(","").replace(",","").replace("'","").replace(")","")))			
			await self.bot.say(embed=emmem1)




def setup(bot):
	bot.add_cog(warframe(bot))