import discord
from discord.ext import commands
import requests
import config

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.slash_command(name="create", description="Crée une VM Proxmox")
async def create_vm(ctx: discord.InteractionContext, vm_name: str, memory: int, storage: str, cpu_cores: int):
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