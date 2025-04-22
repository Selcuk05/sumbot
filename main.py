from gemini_wrapper import GeminiSummarizer

import discord
from discord.ext import commands
from dotenv import dotenv_values

import requests
from bs4 import BeautifulSoup
import PyPDF2
import docx

summarizer = GeminiSummarizer()

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online as: {bot.user}!")

@bot.command()
async def sum_url(ctx, url: str):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        text = ' '.join(text.split())

        summary = summarizer.summarize(text, 1000)
        await ctx.send(embed=create_embed("Summary", summary))
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def sum_file(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        text = ""
        if attachment.filename.endswith(".txt"):
            text = await attachment.read()
            text = text.decode("utf-8")
        elif attachment.filename.endswith(".pdf"):
            pdf_file = await attachment.read()
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        elif attachment.filename.endswith(".docx"):
            docx_file = await attachment.read()
            doc = docx.Document(docx_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text
        else:
            await ctx.send("Please upload a .txt/docx/pdf file.")
            return

        summary = summarizer.summarize(text, 1000)
        await ctx.send(embed=create_embed("Summary", summary))
    else:
        await ctx.send("No file attached.")

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=0x00ff00)
    return embed


bot.run(dotenv_values(".env")["DISCORD_TOKEN"])
