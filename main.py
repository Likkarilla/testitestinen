import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup
import schedule
import time

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)
prefix = '!'

async def get_daily_word():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://raamattu.uskonkirjat.net/servlet/biblesite.Daily?m=FinPR') as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'html.parser')

                daily_word_element = soup.find('p', {'class': 'text'})

                if daily_word_element:
                    daily_word = daily_word_element.get_text().strip()
                    return daily_word
                else:
                    return None
    except Exception as e:
        print(f"Virhe haettaessa päivittäistä sanaa: {e}")
        raise

async def send_daily_word(channel):
    try:
        daily_word = await get_daily_word()
        if daily_word:
            await channel.send(f'Päivän sana: {daily_word}')
        else:
            await channel.send('Päivän sanaa ei löydetty.')
    except Exception as e:
        print(f'Virhe haettaessa päivittäistä sanaa: {e}')

@client.event
async def on_ready():
    print(f'Kirjautunut sisään nimellä {client.user}')
    schedule.every().day.at("08:00").do(send_daily_word, channel=None)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if 'testi' in message.content.lower():
        try:
            daily_word = await get_daily_word()
            if daily_word:
                await message.channel.send(f'Päivän sana: {daily_word}')
            else:
                await message.channel.send('Päivän sanaa ei löydetty.')
        except Exception as e:
            print(f'Virhe haettaessa päivittäistä sanaa testiviestissä: {e}')
            await message.channel.send('Virhe haettaessa päivittäistä sanaa testiviestissä.')

    await client.process_commands(message)

client.run('MTE1OTQ1OTg4MTE4MzYyNTI0Ng.Gpc9-K.yrf4UMIKVdRcmf3rHjHq1pRRgND1gYGJ4ncBzc')  # Korvaa YOUR_BOT_TOKEN botin tokenilla
