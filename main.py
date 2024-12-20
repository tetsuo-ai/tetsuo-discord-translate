import os, sys
from dotenv import load_dotenv
import discord
from deep_translator import GoogleTranslator, single_detection
from deep_translator.exceptions import LanguageNotSupportedException
import logging


TEST_MODE = False

# Set up logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger('discord')
logger.setLevel(logging.WARN)


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPL_KEY = os.getenv('DEEPL_API_KEY')

chinese_channel_id = 1316362477700775987
japanese_channel_id = 1318384551206064208
TRANSLATION_CHANNEL_IDS = [ japanese_channel_id, chinese_channel_id ] # Your specified channel ID


# Create Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# Notify on console that the discord bot is ready
@client.event
async def on_ready():
    print("The bot is ready!")
    print(f"Monitoring channel IDs: {TRANSLATION_CHANNEL_IDS}")


def detect_language(text):
    try:
        return single_detection(text, api_key=DEEPL_KEY)
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

# Handle messages
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Only process messages from the specified channels
    if message.channel.id not in TRANSLATION_CHANNEL_IDS:
        return

    try:
        # Detect the language of the message
        detected_lang = detect_language(message.content)
        
        if detected_lang is None:
            print("Could not detect language")
            return
        else:
            print(f"Detected language: {detected_lang}")
                
        # If the message is not English, translate to English
        if detected_lang != 'en':
            print(f"Message is in {detected_lang}. Translating to English.")
            translated = GoogleTranslator(source='auto', target='en').translate(message.content)
            await message.channel.send(f"translation:\n{translated}")
        # If the message is in any other language, translate to the approprate language for the channel
        else:
            if message.channel.id == japanese_channel_id: 
                print(f"Message is in {detected_lang}. Translating to Japanese.")
                translated = GoogleTranslator(source='auto', target='ja').translate(message.content)
                await message.channel.send(f"translation:\n{translated}")
            else: 
                print(f"Message is in {detected_lang}. Translating to Chinese.")
                translated = GoogleTranslator(source='auto', target='zh-CN').translate(message.content)
                await message.channel.send(f"translation:\n{translated}")

    except Exception as e:
        print(f"Translation error: {e}")


# Run the bot
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)






if TEST_MODE:

    test = "chinese"
    test = "japanese"

    class message():
        content = "Hello, how are you?"
        author = "user"

    try:
        if test == "japanese":

            detected_lang = detect_language(message.content)
            print(detected_lang)
            translated = GoogleTranslator(source='auto', target='ja').translate(message.content)
            print(f"translation:\n{translated}")          

            channel = japanese_channel_id
            message.content = "こんにちは お元気ですか？"

            # Detect the language of the message
            detected_lang = detect_language(message.content)
            print(detected_lang)

            if detected_lang in ['en']:
                translated = GoogleTranslator(source='en', target='ja').translate(message.content)
                print(f"translation:\n{translated}")

            else:
                translated = GoogleTranslator(source='auto', target='en').translate(message.content)
                print(f"translation:\n{translated}")

        if test == "chinese":
            channel = chinese_channel_id
            message.content = "你好，你好吗？"

            # Detect the language of the message
            detected_lang = detect_language(message.content)
            print(detected_lang)

            if detected_lang in ['en']:
                translated = GoogleTranslator(source='en', target='zh-CN').translate(message.content)
                print(f"translation:\n{translated}")
            else:
                translated = GoogleTranslator(source='auto', target='en').translate(message.content)
                print(f"translation:\n{translated}")

    except Exception as e:
        print(f"Translation error: {e}")

    sys.exit()

