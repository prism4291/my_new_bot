import discord
import dotenv
import os
import io
import asyncio
from server import server_thread
#import google.generativeai as genai

dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#gemini_key = os.environ.get("gemini_key")
#genai.configure(api_key=gemini_key)
#gemini_model = genai.GenerativeModel(
#    "gemini-2.5-flash",
#    system_instruction="次のメッセージを、「こんにちは。ふふ。声をかけていただけると嬉しいです。」や「わあ、いただきます。」のような口調のメッセージに修正してください。"
#)

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
        #gemini_chat = gemini_model.start_chat()
        #gemini_res=await gemini_chat.send_message_async(genai.protos.Content(parts=[genai.protos.Part(text=message.content)]))
        await message.channel.send(content=message.content, files=files_to_send)
        try:
            await message.delete()
        except:
            pass

server_thread()
client.run(TOKEN)
