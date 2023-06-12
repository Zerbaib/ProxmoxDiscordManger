import disnake
from disnake.ext import commands
import requests
import config

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

intents = disnake.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.slash_command(
    name="createvm",
    description="Crée une VM Proxmox"
)
async def create_vm(ctx: disnake.ApplicationCommandInteraction, vm_name: str, memory: int, storage: str, cpu_cores: int):
    if ctx.author.id != config.ID:
        await ctx.response.send_message("Désolé, vous n'êtes pas autorisé à exécuter cette commande.", ephemeral=True)
        return

    await ctx.response.defer()

    try:
        vm_create_url = f"{config.PROXMOX_API_URL}/nodes/{config.PROXMOX_NODE}/qemu"
        vm_data = {"vmid": None, "name": vm_name, "memory": memory * 1024, "storage": storage, "cores": cpu_cores}
        headers = {"Authorization": f"PVEAuthCookie={config.PROXMOX_USER}@{config.PROXMOX_NODE}={config.PROXMOX_PASSWORD}"}
        response = requests.post(vm_create_url, json=vm_data, headers=headers, verify=False)

        print(response.text)  # Affiche la réponse de l'API dans la console

        if response.status_code == 200:
            await ctx.edit_original_message(content=f"La VM {vm_name} a été créée avec succès !")
        else:
            await ctx.edit_original_message(content="Erreur lors de la création de la VM.")

    except Exception as e:
        print(f"Erreur lors de la création de la VM : {e}")




bot.run(config.TOKEN)
