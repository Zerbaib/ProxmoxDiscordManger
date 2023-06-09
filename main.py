import discord
from discord.ext import commands
import requests

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
bot = commands.Bot(command_prefix="/")

PROXMOX_API_URL = "https://your-proxmox-api-url/api2/json"
PROXMOX_NODE = "your-proxmox-node"
PROXMOX_USER = "your-proxmox-username"
PROXMOX_PASSWORD = "your-proxmox-password"

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.slash_command(name="createvm", description="Crée une VM Proxmox")
async def create_vm(ctx: discord.InteractionContext, vm_name: str, memory: int, storage: str, cpu_cores: int):
    vm_create_url = f"{PROXMOX_API_URL}/nodes/{PROXMOX_NODE}/qemu"
    vm_data = {"vmid": None, "name": vm_name, "memory": memory * 1024, "storage": storage, "cores": cpu_cores}
    headers = {"Authorization": f"PVEAuthCookie={PROXMOX_USER}@{PROXMOX_NODE}={PROXMOX_PASSWORD}"}
    response = requests.post(vm_create_url, json=vm_data, headers=headers)

    if response.status_code == 200:
        await ctx.send(f"La VM {vm_name} a été créée avec succès !")
    else:
        await ctx.send("Erreur lors de la création de la VM.")

bot.run(TOKEN)