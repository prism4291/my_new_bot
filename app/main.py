import discord
import dotenv
import os
import asyncio

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
    await message.channel.send(message.content)

server_thread()
client.run(TOKEN)
