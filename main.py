import discord

TOKEN = "TOKEN"
bot = discord.Client()

@bot.event
async def on_ready():
    print("Bot is ready!")

bot.run(TOKEN)