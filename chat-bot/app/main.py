import os
import random
import dotenv
import discord
from discord.ext import commands

# Load environment variables
dotenv.load_dotenv()

# Set up intents - these tell Discord what events your bot wants to receive
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Your guild ID - IMPORTANT: Set this in your .env file for instant command updates
GUILD_ID = os.getenv("GUILD_ID")  # Read from environment variables


@bot.event
async def on_ready():
    print(f"✅ {bot.user} is now online!")
    print(f"📊 Connected to {len(bot.guilds)} server(s)")

    # Print guild information for debugging
    for guild in bot.guilds:
        print(f"🏰 Connected to guild: {guild.name} (ID: {guild.id})")

    # Sync commands to a specific guild for instant updates during development
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"🔄 Synced {len(synced)} commands to guild {GUILD_ID}")
            print("✅ Guild-specific commands should appear instantly!")
        except discord.errors.Forbidden:
            print(
                f"❌ Bot doesn't have permission to sync commands to guild {GUILD_ID}"
            )
        except discord.errors.HTTPException as e:
            print(f"❌ HTTP error syncing to guild: {e}")
    else:
        # For development: sync to the first guild the bot is in
        if bot.guilds:
            first_guild = bot.guilds[0]
            try:
                synced = await bot.tree.sync(guild=first_guild)
                print(
                    f"🔄 Synced {len(synced)} commands to guild {first_guild.name} ({first_guild.id})"
                )
                print("💡 Tip: Set GUILD_ID to this guild ID for consistent syncing!")
                print(f"💡 Add this line to your code: GUILD_ID = {first_guild.id}")
            except discord.errors.Forbidden:
                print(
                    f"❌ Bot doesn't have permission to sync commands to guild {first_guild.name}"
                )
            except discord.errors.HTTPException as e:
                print(f"❌ HTTP error syncing to guild: {e}")
        else:
            print("⚠️  No guilds found! Make sure the bot is added to a server.")
            print("⚠️  Syncing globally instead (takes up to 1 hour)")
            try:
                synced = await bot.tree.sync()
                print(
                    f"🌍 Synced {len(synced)} commands globally (may take up to 1 hour)"
                )
            except discord.errors.HTTPException as e:
                print(f"❌ HTTP error syncing globally: {e}")


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Simple responses to regular messages
    content = message.content.lower()

    if "hello" in content or "hi" in content:
        await message.reply("Hello there! 👋")

    elif content.endswith("?"):
        await message.reply("That's an interesting question! 🤔")

    elif "bot" in content:
        await message.add_reaction("🤖")

    # Process commands (important for prefix commands to work)
    await bot.process_commands(message)


# === SLASH COMMANDS ===


@bot.tree.command(name="ping", description="Check bot latency and status")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"**Latency:** {latency}ms\n**Status:** Online ✅",
        color=discord.Color.green(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="say", description="Make the bot say something")
async def say(
    interaction: discord.Interaction, message: str, channel: discord.TextChannel = None
):
    """Make the bot say a message in the current or specified channel"""
    target_channel = channel or interaction.channel

    if target_channel != interaction.channel:
        await target_channel.send(f"📢 {message}")
        await interaction.response.send_message(
            f"✅ Message sent to {target_channel.mention}!", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"📢 {message}")


@bot.tree.command(name="userinfo", description="Get information about a user")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    """Display information about a user"""
    target_user = user or interaction.user

    embed = discord.Embed(
        title=f"👤 User Info: {target_user.display_name}",
        color=(
            target_user.color
            if target_user.color != discord.Color.default()
            else discord.Color.blue()
        ),
    )

    embed.set_thumbnail(url=target_user.display_avatar.url)
    embed.add_field(name="Username", value=target_user.name, inline=True)
    embed.add_field(name="ID", value=target_user.id, inline=True)
    embed.add_field(
        name="Joined Server",
        value=target_user.joined_at.strftime("%B %d, %Y"),
        inline=True,
    )
    embed.add_field(
        name="Account Created",
        value=target_user.created_at.strftime("%B %d, %Y"),
        inline=True,
    )
    embed.add_field(
        name="Highest Role", value=target_user.top_role.mention, inline=True
    )
    embed.add_field(name="Status", value=str(target_user.status).title(), inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="serverinfo", description="Get information about this server")
async def serverinfo(interaction: discord.Interaction):
    """Display information about the current server"""
    guild = interaction.guild

    embed = discord.Embed(
        title=f"🏰 Server Info: {guild.name}", color=discord.Color.gold()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(
        name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True
    )
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="roll", description="Roll a dice")
async def roll(interaction: discord.Interaction, sides: int = 6, count: int = 1):
    """Roll dice with specified sides and count"""
    if sides < 2 or sides > 100:
        await interaction.response.send_message(
            "❌ Dice must have between 2 and 100 sides!", ephemeral=True
        )
        return

    if count < 1 or count > 10:
        await interaction.response.send_message(
            "❌ You can roll between 1 and 10 dice!", ephemeral=True
        )
        return

    results = [random.randint(1, sides) for _ in range(count)]
    total = sum(results)

    embed = discord.Embed(title="🎲 Dice Roll", color=discord.Color.random())

    if count == 1:
        embed.description = f"🎯 **Result:** {results[0]}\n📊 **Dice:** d{sides}"
    else:
        embed.description = f"🎯 **Results:** {', '.join(map(str, results))}\n📊 **Total:** {total}\n🎲 **Dice:** {count}d{sides}"

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    """Flip a coin and get heads or tails"""
    result = random.choice(["Heads", "Tails"])
    emoji = "🪙" if result == "Heads" else "🟡"

    embed = discord.Embed(
        title="🪙 Coin Flip",
        description=f"{emoji} **{result}!**",
        color=discord.Color.gold(),
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="joke", description="Get a random programming joke")
async def joke(interaction: discord.Interaction):
    """Tell a random programming joke"""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
        "Why do Java developers wear glasses? Because they can't C# 👓",
        "A SQL query goes into a bar, walks up to two tables and asks... 'Can I join you?' 🍺",
        "Why did the programmer quit his job? He didn't get arrays! 📊",
        "What's a programmer's favorite hangout place? Foo Bar! 🍻",
        "Why don't programmers like nature? It has too many bugs! 🌿🐛",
        "What do you call a programmer from Finland? Nerdic! 🇫🇮",
    ]

    selected_joke = random.choice(jokes)

    embed = discord.Embed(
        title="😂 Programming Joke",
        description=selected_joke,
        color=discord.Color.random(),
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="poll", description="Create a simple yes/no poll")
async def poll(interaction: discord.Interaction, question: str):
    """Create a poll with yes/no reactions"""
    embed = discord.Embed(
        title="📊 Poll",
        description=f"**{question}**\n\n✅ = Yes\n❌ = No",
        color=discord.Color.blue(),
    )
    embed.set_footer(text=f"Poll created by {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()
    await message.add_reaction("✅")
    await message.add_reaction("❌")


@bot.tree.command(name="avatar", description="Get a user's avatar")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    """Display a user's avatar in full size"""
    target_user = user or interaction.user

    embed = discord.Embed(
        title=f"🖼️ {target_user.display_name}'s Avatar",
        color=(
            target_user.color
            if target_user.color != discord.Color.default()
            else discord.Color.blue()
        ),
    )
    embed.set_image(url=target_user.display_avatar.url)
    embed.add_field(
        name="Direct Link", value=f"[Click here]({target_user.display_avatar.url})"
    )

    await interaction.response.send_message(embed=embed)


# === PREFIX COMMANDS ===


@bot.command(name="hello")
async def hello_command(ctx):
    """Simple hello command using prefix"""
    await ctx.send(
        f"Hello {ctx.author.mention}! 👋 Try using `/ping` for a fancier response!"
    )


@bot.command(name="info")
async def info_command(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title="🤖 Bot Information",
        description="A simple Discord bot made with discord.py!",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Prefix", value="`!`", inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Python", value="3.8+", inline=True)

    await ctx.send(embed=embed)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
