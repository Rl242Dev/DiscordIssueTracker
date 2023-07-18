# ─── Secrets ──────────────────────────────────────────────────────────────────

token = "" # Token du bot

 # Github secrets

github_token = ""
owner = ""
repo = ""

# ─── Packages ─────────────────────────────────────────────────────────────────

import discord
import requests
import json

# ─── Global Class ─────────────────────────────────────────────────────────────

class client(discord.Client):
    synced = False

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        self.add_view(ConfigButton())
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Connecté à : {client.user}')


class ConfigButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⛔ | Report une Issue", style=discord.ButtonStyle.blurple, custom_id="config_button")
    async def configButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await newIssue(interaction)


class IssueForm(discord.ui.Modal, title="💻 | Report d'une Issue"):
    IssueTitle = discord.ui.TextInput(label="📜 | Titre de l'Issue", style=discord.TextStyle.short, placeholder="",
                                default="", required=True, max_length=255)
    IssueBody = discord.ui.TextInput(label="📜 | Contenu de l'Issue", style=discord.TextStyle.paragraph, placeholder="",
                                default="", required=True, max_length=4000)

    async def on_submit(self, interaction):
        if self.IssueTitle.value in blacklists_words:
            await interaction.response.send_message("❌ | Votre report contenait un mot blacklisté")
            return

        if self.IssueBody.value in blacklists_words:
            await interaction.response.send_message("❌ | Votre report contenait un mot blacklisté")
            return

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {github_token}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            "title": self.IssueTitle.value,
            "body": self.IssueBody.value,
        }

        response = requests.post(f"https://api.github.com/repos/{owner}/{repo}/issues", data=json.dumps(data), headers=headers)
        if(response.status_code == 201):
            await interaction.response.send_message("✅ | Vous avez report avec succès une Issue", ephemeral=True)
        else:
            await interaction.response.send_message("❌ | Il y a eu une erreur lors de la création de l'Issue", ephemeral=True)
            print(response.content)

# ─── Global Variables ─────────────────────────────────────────────────────────


aclient = client()
tree = discord.app_commands.CommandTree(aclient)

blacklists_words = []


# ─── Code ─────────────────────────────────────────────────────────────────────

async def newIssue(interaction: discord.Interaction):
    await interaction.response.send_modal(IssueForm())


@tree.command(name="start", description="Start")
async def start(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Vous ne pouvez pas executer cette commande", ephemeral=True)

    embed = discord.Embed(title="**Création Report**",
                          description="Cliquez sur le bouton configuration afin de report une Issue")
    await interaction.channel.send(embed=embed, view=ConfigButton())


aclient.run(token=token)
