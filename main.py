import interactions
from interactions import Intents
from transcribe import transcribe
from consts import COUNTRY_EMOJI_MAPPING
from dotenv import load_dotenv
import os
import sys

load_dotenv()

if os.environ.get("DISCORD_TOKEN") is None:
    print("You are lacking an enviornment variable DISCORD_TOKEN! Exiting....")
    sys.exit(1)

bot = interactions.Client(
    token = os.environ["DISCORD_TOKEN"],
    intents = Intents.new(messages=True, message_content=True, reactions=True, guilds=True)
)

@interactions.listen()
async def on_startup():
    print(f"We have logged in as {bot.user.display_name}")

@interactions.listen()
async def on_message_create(event):
    """
    Here we are checking for every new single message and transcribing them accordingly
    """
    message = event.message
    # Check if we have been mentioned
    mentions = event.message.mention_users
    async for mention in mentions:
        if mention.id == bot.user.id:
            # Check if it's a reply
            original_message = await event.message.fetch_referenced_message()
            if original_message is not None:
                message = original_message

    # Check if we have attachments
    if message.attachments == []:
        return

    if len(message.attachments) != 1:
        return

    if not 'voice-message.ogg' in message.attachments[0].url:
        return

    print(message.attachments[0].url)
    await transcribe(FILE_URL=message.attachments[0].url, ORIGINAL_MESSAGE=message, REGENERATE=False)

@interactions.listen()
async def on_message_reaction_add(reaction):
    """
    This checks 
    """
    # Check if it is a reaction on our bot
    if reaction.message.author.id != bot.user.id:
        return

    # Get the Original Message
    original_message = await reaction.message.fetch_referenced_message()

    if reaction.reaction.emoji.name == "🔥":
        await transcribe(
            FILE_URL = original_message.attachments[0].url, 
            ORIGINAL_MESSAGE = original_message, 
            NEW_MESSAGE = reaction.message,
            REGENERATE = True
        )

    if reaction.reaction.emoji.name in COUNTRY_EMOJI_MAPPING:
        await transcribe(
            FILE_URL = original_message.attachments[0].url, 
            ORIGINAL_MESSAGE = original_message, 
            NEW_MESSAGE = reaction.message,
            REGENERATE = True,
            LANGUAGE = COUNTRY_EMOJI_MAPPING[reaction.reaction.emoji.name]
        )




bot.start()
