import os
import sys
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from langdetect import detect
from googletrans import Translator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!tr help"))

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'Error in {event}:', exc_info=True)

# Rest of your bot code remains the same...
# [Previous event handlers and commands]

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !tr help for available commands.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {str(error)}")

if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
