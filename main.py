import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from langdetect import detect
from googletrans import Translator

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!tr ', intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!tr help"))

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Process commands if any
    await bot.process_commands(message)

    # Don't translate commands
    if message.content.startswith('!tr'):
        return

    try:
        # Detect language
        detected_lang = detect(message.content)
        
        # Translate if message is in English or French
        if detected_lang == 'en':
            translated = translator.translate(message.content, src='en', dest='fr')
            target_lang = 'French'
        elif detected_lang == 'fr':
            translated = translator.translate(message.content, src='fr', dest='en')
            target_lang = 'English'
        else:
            return  # Don't translate other languages

        # Create embed
        embed = discord.Embed(title=f"Translated to {target_lang}", color=0x00ff00)
        embed.add_field(name="Original", value=message.content, inline=False)
        embed.add_field(name="Translation", value=translated.text, inline=False)
        embed.set_footer(text=f"Requested by {message.author.display_name}")

        await message.channel.send(embed=embed)

    except Exception as e:
        print(f"Translation error: {e}")

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="Translator Bot Help", color=0x00ff00)
    embed.add_field(
        name="Automatic Translation",
        value="The bot automatically detects and translates messages between English and French.",
        inline=False
    )
    embed.add_field(
        name="Commands",
        value="!tr help - Show this help message",
        inline=False
    )
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
