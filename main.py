import discord
import requests

TOKEN = "TOKEN"
bot = discord.Client()

PROXMOX_API_URL = "https://your-proxmox-api-url/api2/json"
PROXMOX_NODE = "your-proxmox-node"
PROXMOX_USER = "your-proxmox-username"
PROXMOX_PASSWORD = "your-proxmox-password"

@bot.event
async def on_ready():
    print("Bot is ready!")

bot.run(TOKEN)