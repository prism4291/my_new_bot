import discord
import dotenv
import os

from server import server_thread

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.channel.send(message.content)

server_thread()
client.run(TOKEN)
