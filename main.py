import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

counting_channel = None
current_number = 1

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'Current Number: {current_number}'))
    print(f'Logged in as {bot.user.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    global counting_channel
    counting_channel = ctx.channel
    with open('counting.txt', 'w') as file:
        file.write(f'{counting_channel.id}\n{current_number}')
    embed = discord.Embed(
        title='Counting Channel Setup',
        description='Dieser Channel wurde als Counting Channel gesetzt.',
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    global current_number

    if message.author.bot:
        return

    if message.channel == counting_channel:
        if message.content.isdigit():
            if int(message.content) == current_number:
                current_number += 1
                await bot.change_presence(activity=discord.Game(name=f'Current Number: {current_number}'))
                with open('counting.txt', 'w') as file:
                    file.write(f'{counting_channel.id}\n{current_number}')
            else:
                await message.add_reaction('❌')
                embed = discord.Embed(
                    title=f'Das Counting wurde bei {current_number} unterbrochen',
                    description=f'Der User {message.author.mention} hat das Counting unterbrochen. Es wird nun wieder bei **1** gestartet.',
                    color=discord.Color.red()
                )
                await counting_channel.send(embed=embed)
                current_number = 1
                with open('counting.txt', 'w') as file:
                    file.write(f'{counting_channel.id}\n{current_number}')
    
    await bot.process_commands(message)

bot.run('YOUR-BOT-TOKEN-HERE')
