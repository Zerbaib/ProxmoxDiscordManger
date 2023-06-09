import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord.ext.commands.cooldowns import CooldownMapping, BucketType
import requests

TOKEN = "TOKEN"
bot = commands.Bot(
    intents=discord.Intents.all(),
    case_insensitive=True,
)
slash = SlashCommand(bot, sync_commands=True)

PROXMOX_API_URL = "https://your-proxmox-api-url/api2/json"
PROXMOX_NODE = "your-proxmox-node"
PROXMOX_USER = "your-proxmox-username"
PROXMOX_PASSWORD = "your-proxmox-password"

@bot.event
async def on_ready():
    print("Bot is ready!")


@slash.slash(
        name="create",
        description="Create a Proxmox VM",
        option=[
            {
            "name": "vm_name",
            "description": "Nom de la VM",
            "type": 3,
            "required": True
        },
        {
            "name": "memory",
            "description": "Quantité de mémoire (en GB)",
            "type": 4,
            "required": True
        },
        {
            "name": "storage",
            "description": "Stockage",
            "type": 3,
            "required": True
        },
        {
            "name": "cpu_cores",
            "description": "Nombre de cœurs CPU",
            "type": 4,
            "required": True
        }])
async def create(ctx: SlashContext, vm_name: str, memory: int, storage: str, cpu_cores: int):
    vm_create_url = f"{PROXMOX_API_URL}/nodes/{PROXMOX_NODE}/qemu"

    vm_data = {
        "vmid": None,  # Laissez Proxmox attribuer un ID automatiquement
        "name": vm_name,
        "memory": memory * 1024,  # Conversion en MB
        "storage": storage,
        "cores": cpu_cores
    }

    headers = {
        "Authorization": f"PVEAuthCookie={PROXMOX_USER}@{PROXMOX_NODE}={PROXMOX_PASSWORD}"
    }

    response = requests.post(vm_create_url, json=vm_data, headers=headers)

    if response.status_code == 200:
        await ctx.send(f"La VM {vm_name} a été créée avec succès !")
    else:
        await ctx.send("Erreur lors de la création de la VM.")



bot.run(TOKEN)