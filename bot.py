import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Function to prompt user for the bot token and secret code
def setup_environment():
    """Prompt the user for bot token and secret code if not in .env."""
    print("Setup: Please enter your bot token and secret code.\n")
    
    token = input("Bot Token: ").strip()
    secret_code = input("Secret Code: ").strip()

    with open('.env', 'w') as f:
        f.write(f"DISCORD_TOKEN={token}\n")
        f.write(f"SECRET_CODE={secret_code}\n")

    print("Token and secret code have been saved in .env file.")

# Load the environment variables
load_dotenv()

# Ensure the token and secret code are set
token = os.getenv("DISCORD_TOKEN")
if not token:
    print("No token found! Please run the bot setup.")
    setup_environment()
    token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def say(ctx, *, sentence: str):
    """Admin command to make the bot say something."""
    await ctx.send(sentence)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a user from the server (admin only)."""
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned!")
    except discord.Forbidden:
        await ctx.send("I do not have permission to ban this member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member: str):
    """Unban a user from the server (admin only)."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user
        if (user.name == member_name and user.discriminator == member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned!")
            return

    await ctx.send(f"User {member} not found in the banned list.")

@bot.event
async def on_message(message):
    """Handle messages and prevent bot from responding to itself."""
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Start the bot with token from environment variable
def run_bot():
    if not token:
        print("Error: No token provided. Please run the bot setup.")
        return
    bot.run(token)

if __name__ == "__main__":
    run_bot()
