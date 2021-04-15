import requests, json, discord, datetime, asyncio, aiohttp
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

x = datetime.datetime.now()

with open('Saves/setup.json') as f:
    config = json.load(f)

if config['api-key'] == 'Fortnite API Key Here (If Not Leave Default)':
    apikey = False
else:
    apikey = True

bot = commands.Bot(command_prefix=config['prefix'])

@bot.command()
async def aes(ctx):
  r = requests.get('https://benbotfn.tk/api/v1/aes')
  rr = r.json()

  mainkey = rr['mainKey']
  version = rr['version']
  embed = discord.Embed(title=f"{version} Aes", description="")
  embed.add_field(name='MainKey', value=f'``{mainkey}``', inline=False)
  for sub_dict in rr['dynamicKeys']:
      embed.add_field(name=sub_dict.split('FortniteGame/Content/Paks/')[1].strip().replace('"', ''), value=f"``{rr['dynamicKeys'][sub_dict]}``", inline=False)
      embed.set_footer(text=f'{ctx.guild.name}', icon_url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)

@bot.command()
async def bearer(ctx):
  r = requests.get('https://api.nitestats.com/v1/epic/bearer')
  rr = r.json()

  accessToken = rr['accessToken']
  lastUpdated = rr['lastUpdated']
  embed = discord.Embed(title=f"Bearer Token", description="")
  embed.add_field(name='Access Token', value=f'``{accessToken}``', inline=False)
  embed.add_field(name='Last Updated', value=f"``{lastUpdated}``", inline=False)
  embed.set_footer(text=f'Updated every 10 minutes - {ctx.guild.name}', icon_url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)
                      
@bot.command()
async def fltoken(ctx):
  r = requests.get('https://api.nitestats.com/v1/epic/builds/fltoken')
  rr = r.json()

  version = rr['version']
  fltoken = rr['fltoken']
  embed = discord.Embed(title=f"FLToken", description="")
  embed.add_field(name='Version', value=f'``{version}``', inline=False)
  embed.add_field(name='FLToken', value=f"``{fltoken}``", inline=False)
  embed.set_footer(text=f'Refreshes automatically in under 1sec when a new build releases - {ctx.guild.name}', icon_url=f'{ctx.guild.icon_url}')
  await ctx.send(embed=embed)

@tasks.loop(seconds=30)
async def taskbrnews():
    with open('Saves/news.json', 'r') as file:
        old = json.load(file)
    try:
      if apikey == True:
          async with aiohttp.ClientSession() as session:
              async with session.get("https://fortnite-api.com/v2/news/br", headers={"Authorization":config["api-key"]}) as r:
                  response = await r.json()
                  if response != old:
                      channel = bot.get_channel(config['news-channel'])
                      embed=discord.Embed(
                          title='Br News',
                      )
                      embed.set_image(url=response['data']['image'])
                      await channel.send(embed=embed)
                  with open('Saves/news.json', 'w') as file:
                      json.dump(response, file, indent=3)
      else:
          async with aiohttp.ClientSession() as session:
              async with session.get("https://fortnite-api.com/v2/news/br") as r:
                  response = await r.json()
                  if response != old:
                      channel = bot.get_channel(config['news-channel'])
                      embed=discord.Embed(
                          title='Br News',
                      )
                      embed.set_image(url=response['data']['image'])
                      await channel.send(embed=embed)
                  with open('Saves/news.json', 'w') as file:
                      json.dump(response, file, indent=3)
    except Exception as e:
      print("ERROR! Woah that wasn't supposed to happen " + e)
      pass


@tasks.loop(seconds=30)
async def autobuild():
    with open('Saves/build.json', 'r') as file:
        old = json.load(file)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://benbotfn.tk/api/v1/status") as statuss:
            status = await statuss.json() 
            if status != old:
                await bot.change_presence(activity=discord.Game(name=f"{status['currentFortniteVersion']}"))
                async with session.get("https://benbotfn.tk/api/v1/aes") as response:
                    response = await response.json()
                    embed=discord.Embed(
                        title="Fortnite Static Key Update Detected", 
                        color=0xff0a0a
                    )
                    channel = bot.get_channel(config["build-channel"])
                    embed.add_field(name=f"Build", value=f"{response['version']}", inline=False)
                    embed.add_field(name="AES", value=f"{response['mainKey']}", inline=False)
                    await channel.send(embed=embed)
            with open('Saves/build.json', 'w') as file:
                json.dump(status, file, indent=3)

@tasks.loop(seconds=30)
async def autofltoken():
    with open('Saves/fltoken.json', 'r') as file:
        old = json.load(file)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.nitestats.com/v1/epic/builds/fltoken") as statuss:
            status = await statuss.json() 
            if status != old:
                async with session.get("https://api.nitestats.com/v1/epic/builds/fltoken") as response:
                    response = await response.json()
                    embed=discord.Embed(
                        title="Fortnite FLToken Updated", 
                        color=0xff0a0a
                    )
                    channel = bot.get_channel(config["build-channel"])
                    embed.add_field(name=f"Build", value=f"{response['version']}", inline=False)
                    embed.add_field(name="FLToken", value=f"{response['fltoken']}", inline=False)
                    await channel.send(embed=embed)
            with open('Saves/fltoken.json', 'w') as file:
                json.dump(status, file, indent=3)

@tasks.loop(seconds=30)
async def autobg():
    with open('Saves/bg.json', 'r') as file:
        old = json.load(file)
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.fortniteapi.net/v1/game/backgrounds") as statuss:
            status = await statuss.json() 
            if status != old:
                async with session.get("http://www.fortniteapi.net/v1/game/backgrounds") as response:
                    response = await response.json()
                    embed=discord.Embed(
                        title="Fortnite Dynamic Backgrounds Updated", 
                        color=0xff0a0a
                    )
                    channel = bot.get_channel(config["build-channel"])
                    embed.add_field(name=f"Stage", value=f"{response['backgrounds'][0]['stage']}", inline=False)
                    embed.add_field(name="Type", value=f"{response['backgrounds'][0]['_type']}", inline=False)
                    embed.add_field(name="Key", value=f"{response['backgrounds'][0]['key']}", inline=False)
                    embed.add_field(name=f"Stage", value=f"{response['backgrounds'][1]['stage']}", inline=False)
                    embed.add_field(name="Type", value=f"{response['backgrounds'][1]['_type']}", inline=False)
                    embed.add_field(name="Key", value=f"{response['backgrounds'][1]['key']}", inline=False)
                    await channel.send(embed=embed)
            with open('Saves/bg.json', 'w') as file:
                json.dump(status, file, indent=3)

@tasks.loop(seconds=30)
async def autobrshop():
    with open('Saves/shop.json', 'r') as file:
        old = json.load(file)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.peely.de/v1/shop") as r:
                response = await r.json()
                if response != old:
                    with open('Saves/shop.json', 'w') as file:
                        json.dump(response, file, indent=3)
                        file.close()
                    with open('Saves/shop.json', 'r') as file:
                        new = json.load(file)
                    channel = bot.get_channel(config['shop-channel'])
                    embed=discord.Embed(
                        title='Br Shop - ' + new['time'],
                    )
                    embed.set_image(url=new['url'])
                    await channel.send(content=new['url']) # discord caches images in embed ig so no embeds boooo
    except Exception as e:
      print("ERROR! Woah that wasn't supposed to happen " + str(e))
      pass

@bot.event
async def on_ready():
    print('Bot Ready/Logged In')
    status=requests.get(
        'https://benbotfn.tk/api/v1/status'
    ).json()
    await bot.change_presence(activity=discord.Game(name=f"{status['currentFortniteVersion']}"))
    taskbrnews.start()
    autobuild.start()
    autobrshop.start()
    autofltoken.start()
    autobg.start()

@bot.command()
async def stats(ctx, arg):
  r = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={arg}&image=all')
  rr = r.json()
  embed=discord.Embed()
  embed.set_image(url=f"{rr['data']['image']}")
  await ctx.send(embed=embed)

@bot.command()
async def brnews(ctx):
    response=requests.get(
        'https://fortnite-api.com/v2/news/br'
    ).json()
    embed=discord.Embed(
        title='Br News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def creativenews(ctx):
    response=requests.get(
        'https://fortnite-api.com/v2/news/creative'
    ).json()
    embed=discord.Embed(
        title='Creative News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def stwnews(ctx):
    response=requests.get(
        'https://api.peely.de/v1/stw/news'
    ).json()
    embed=discord.Embed(
        title='Save The World News'
    )
    embed.set_image(
        url=response['data']['image']
    )
    await ctx.send(embed=embed)

@bot.command()
async def search(ctx, cosnamee):
  #cosnamee = cosnamee.strip('>search ')
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={cosnamee}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(color=0x0d95fd)
      embed.add_field(name='Name', value=f"``{sub_dict['name']}``", inline=False)
      embed.add_field(name='ID', value=f"``{sub_dict['id']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['description']}``", inline=False)
      embed.add_field(name='Type', value=f"``{sub_dict['type']['value']}``", inline=False)
      embed.add_field(name='Display Type', value=f"``{sub_dict['type']['displayValue']}``", inline=False)
      embed.add_field(name='Backend Value', value=f"``{sub_dict['type']['backendValue']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['rarity']['value']}``", inline=False)
      embed.add_field(name='Backend Rarity', value=f"``{sub_dict['rarity']['backendValue']}``", inline=False)
      embed.add_field(name='Series', value=f"``{sub_dict['series']}``", inline=False)
      embed.add_field(name='Shop History', value=f"``{sub_dict['shopHistory']}``", inline=False)
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=f"``{sub_dict['introduction']['text']}``", inline=False)
        embed.add_field(name='Display Asset Path', value=f"``{sub_dict['displayAssetPath']}``", inline=False)
        embed.add_field(name='Definition Path', value=f"``{sub_dict['definitionPath']}``", inline=False)
        embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=f"{bot.user.name} | uwu")
        message = await ctx.send(embed=embed)
  else:
    embed = discord.Embed(color=0xff0f0f)
    embed.add_field(name='Error', value=f"``{rr['error']}``", inline=False)
    embed.set_footer(text=f"{bot.user.name} | uwu")
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()
                    
@bot.command()
async def brshop(ctx, aliases=['shop', 'itemshop']):
    response=requests.get('https://api.peely.de/v1/shop').json()
    embed=discord.Embed(
        title=response['time']
    )
    embed.set_image(
        url=response['uniqueurl']
    )
    await ctx.send(embed=embed)

bot.run(config["token"], reconnect=True)
