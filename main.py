import discord
from discord.ext import commands
from discord_interactions import *
import requests
import config

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.slash_command(
    name="createvm",
    description="Crée une VM Proxmox",
    options=[
        Option(str, "vm_name", "Le nom de la VM"),
        Option(int, "memory", "La quantité de mémoire (en Mo)"),
        Option(str, "storage", "L'espace de stockage"),
        Option(int, "cpu_cores", "Le nombre de cœurs CPU")
    ]
)
async def create_vm(ctx, vm_name, memory, storage, cpu_cores):
    if ctx.author.id != config.ID:
        await ctx.send("Désolé, vous n'êtes pas autorisé à exécuter cette commande.")
        return

    vm_create_url = f"{config.PROXMOX_API_URL}/nodes/{config.PROXMOX_NODE}/qemu"
    vm_data = {"vmid": None, "name": vm_name, "memory": memory * 1024, "storage": storage, "cores": cpu_cores}
    headers = {"Authorization": f"PVEAuthCookie={config.PROXMOX_USER}@{config.PROXMOX_NODE}={config.PROXMOX_PASSWORD}"}
    response = requests.post(vm_create_url, json=vm_data, headers=headers)

    if response.status_code == 200:
        await ctx.send(f"La VM {vm_name} a été créée avec succès !")
    else:
        await ctx.send("Erreur lors de la création de la VM.")

bot.run(config.TOKEN)