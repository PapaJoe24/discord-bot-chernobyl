import discord
import commands
import os.path


def run_discord_bot(messages_filename, emoji_filename):
    TOKEN = 'MTE0NTQ5NTYzMjM2MzEzOTEwMw.GjWvDC.oYWBuTiTd378LA83pLQCfPHHQVPfCEpTurUdXo'
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if len(user_message) > 0 and user_message[0] == '$':
            print(f"{username} command: '{user_message}' ({channel})")
            user_message = user_message[1:]
            
            if(user_message.startswith("help")):
                await commands.send_help_message(message)
            
            elif(user_message.startswith("save_messages")):
                await commands.save_messages(message)
                await commands.send_file(message, file_path=messages_filename)

            elif(user_message.startswith("get_log")):
                if os.path.exists(messages_filename):
                    await commands.send_file(message, file_path=messages_filename)
                else:
                    await commands.send_message(message, "No file found, try using the **save_messages [channel]** command first", False)

            elif(user_message.startswith("hadow_wizard_money_gang")):
                await commands.send_message(message, "We love casting spells :man_mage::man_mage::mage::mage:", False, True)
                await commands.emoji_nuke(message, emoji_filename, max_emotes= 6 ,limit=None)
                
            elif(user_message.startswith("get_emotes")):
                await commands.get_emoji_list(message, emoji_filename)

            elif(user_message.startswith("do_laundry")):
                await commands.send_message(message, "I'm very sorry for my actions :sob:", False, True)
                await commands.cleanup_emotes(message, limit=None)

    client.run(TOKEN)