import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def fetch_news_with_images():
    url = "https://kooora.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_data = []
    articles = soup.select("div.newsHolder div.item")

    for article in articles[:5]:
        title_tag = article.select_one("a.title")
        img_tag = article.select_one("img")

        if not title_tag or not img_tag:
            continue

        title = title_tag.text.strip()
        link = title_tag["href"]
        image_url = img_tag["src"]

        if not link.startswith("http"):
            link = "https://kooora.com" + link

        news_data.append({
            "title": title,
            "url": link,
            "image": image_url
        })

    return news_data

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    while True:
        news_items = fetch_news_with_images()
        for news in news_items:
            embed = discord.Embed(
                title=news['title'],
                url=news['url'],
                description="اضغط على العنوان لقراءة التفاصيل 🔗",
                color=0x00ff00
            )
            embed.set_image(url=news['image'])
            embed.set_footer(text="📰 من موقع كووورة")

            await channel.send(embed=embed)

        await asyncio.sleep(3600)  # كل ساعة

client.run(TOKEN)
