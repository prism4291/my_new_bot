import discord
import dotenv
import os
import io
import asyncio
from server import server_thread
from google import genai
from google.genai import types


dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

gemini_client = genai.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id!=1399717134162202627:
        return
    if message.content or message.attachments:
        files_to_send = []
        if message.attachments:
            for attachment in message.attachments:
                file_bytes = await attachment.read()
                discord_file = discord.File(io.BytesIO(file_bytes), filename=attachment.filename)
                files_to_send.append(discord_file)
        gemini_response = await gemini_client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.content,
            config=types.GenerateContentConfig(
                system_instruction='次のメッセージを、「こんにちは。ふふ。声をかけていただけると嬉しいです。」や「わあ、いただきます。」のような口調のメッセージに修正してください。',
            )
        )
        await message.channel.send(content=gemini_response, files=files_to_send)
        try:
            await message.delete()
        except:
            pass

server_thread()
client.run(TOKEN)
