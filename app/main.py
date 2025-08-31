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
LOG_CHANNEL = None

gemini_clients=[]
for i in range(4):
    gemini_clients.append(genai.Client(api_key=os.environ.get(f"GEMINI_API_KEY{i+1}")))
GEMINI_API_KEY_INDEX=0


async def get_msg(message_content):
    gemini_response = await gemini_clients[GEMINI_API_KEY_INDEX].aio.models.generate_content(
        model='gemini-2.5-flash',
        contents=message_content,
        config=types.GenerateContentConfig(
            system_instruction='次のメッセージを、「こんにちは。ふふ。声をかけていただけると嬉しいです。」や「わあ、いただきます。」のような口調のメッセージに修正し、<answer></answer>形式で出力してください。',
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )
    )
    return gemini_response

async def send_msg(message_channel,msg,files_to_send):
    if files_to_send:
        for file in files_to_send:
            file.fp.seek(0)
        if not msg:
            await message_channel.send(files=files_to_send)
            return
    for i in range(0, len(msg),1900):
        t=msg[i:i+1900]
        if i==0:
            await message_channel.send(content=t, files=files_to_send)
        else:
            await message_channel.send(content=t)

@client.event
async def on_ready():
    global LOG_CHANNEL
    LOG_CHANNEL = client.get_channel(1411635590847402037)
    await send_msg(LOG_CHANNEL,"Ready!",None)

@client.event
async def on_message(message):
    global GEMINI_API_KEY_INDEX,LOG_CHANNEL
    if message.author == client.user:
        return
    if False:
        return
    if message.content or message.attachments:
        files_to_send = []
        if message.attachments:
            for attachment in message.attachments:
                file_bytes = await attachment.read()
                discord_file = discord.File(io.BytesIO(file_bytes), filename=attachment.filename)
                files_to_send.append(discord_file)
        message_content=message.content
        message_channel=message.channel
        await send_msg(LOG_CHANNEL,f"{message.author} at {message_channel} :\n{message_content}",files_to_send)
        try:
            gemini_response=await get_msg(message_content)
        except:
            GEMINI_API_KEY_INDEX=(GEMINI_API_KEY_INDEX+1)%4
            try:
                gemini_response=await get_msg(message_content)
            except genai.errors.APIError as e:
                await send_msg(LOG_CHANNEL,f"エラーです。\n{e}",None)
                return
        t=gemini_response.text
        t=t.split("<answer>")[-1]
        t=t.split("</answer>")[0]
        try:
            await message.delete()
        except Exception as e:
            await send_msg(LOG_CHANNEL,f"削除失敗です。\n{e}",None)
            pass
        await send_msg(message_channel,t,files_to_send)
    

server_thread()
client.run(TOKEN)
