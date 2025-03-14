from gemini_wrapper import GeminiSummarizer

import discord
from dotenv import dotenv_values

# Intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

summarizer = GeminiSummarizer()


# Events
@client.event
async def on_ready():
    print(f"Bot online as: {client.user}")


client.run(dotenv_values(".env")["DISCORD_TOKEN"])
