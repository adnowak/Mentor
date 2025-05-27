import os
import dotenv
import discord
from discord import app_commands
from discord.ext import commands


dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# Using commands.Bot instead of Client for better slash command support
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    # Sync commands globally (for all guilds) - this can take up to an hour to propagate
    # Note: During development, you might want to use guild-specific commands
    # which update instantly
    try:
        print("Syncing global commands...")
        await bot.tree.sync()
        print("Global commands synced successfully!")
    except Exception as e:
        print(f"Error syncing commands: {e}")


# Example of a regular message command (will be deprecated by Discord eventually)
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


# Example of an application command (slash command)
@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency}ms")


# Another example of an application command with parameters
@bot.tree.command(name="greet", description="Greet a user")
@app_commands.describe(user="The user to greet", message="Custom greeting message")
async def greet(
    interaction: discord.Interaction, user: discord.User, message: str = "Hello"
):
    await interaction.response.send_message(f"{message}, {user.mention}!")


# Install command to guide users on how to install the bot
@bot.tree.command(name="install", description="Learn how to install this bot")
async def install(interaction: discord.Interaction):
    install_guide = """
**How to install this bot:**

1. **Requirements:**
   - Python 3.8 or higher
   - Discord Developer Account
   
2. **Setup:**
   - Clone the repository
   - Create a `.env` file with your `DISCORD_BOT_TOKEN`
   - Install requirements: `pip install -r requirements.txt`
   - Run the bot: `python app/main.py`
   
3. **Add to Server:**
   - Use the OAuth2 URL generator in the Discord Developer Portal
   - Select bot and applications.commands scopes
   - Choose appropriate permissions
   - Open the generated URL and select your server

For more detailed instructions, visit our GitHub repository.
"""
    await interaction.response.send_message(install_guide)


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
