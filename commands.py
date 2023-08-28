import discord
import random

commands = {
    "$help": "gives a list of all avalible commands",
    "$save_messages [name of channel]": "saves all messages in desired channel and sends the text file",
    "$get_log": "sends the current saved log",
    "$get_emotes": "adds to the grand list of emotes :imp:",
    "$hadow_wizard_money_gang": "We love casting spells",
}

#Sends a help message
async def send_help_message(message):
    try:
        formatted_text = ''
        for c in commands:
            formatted_text += (f"**{c}** {commands[c]}\n")

        await message.channel.send(formatted_text)
    except Exception as e:
        print(e)


#Save the entire channel messages:
async def save_messages(message, file_name='message_log.txt'):
    channel = await get_channel(message)

    if channel is None:
        print("No Channel Found")
        return
        
    with open(file_name, 'a') as log_file:
        async for message in channel.history(limit=None):
            log_file.write(f'{message.author.name} ({message.author.id}): {message.content} - {message.created_at}\n')

    print(f"Saved Log to {file_name}")

#Cleanup emotes
async def cleanup_emotes(message, limit=None):
    async for message in message.channel.history(limit=limit):
        await message.clear_reactions()

#Get a List of Emojis in the server
async def get_emoji_list(message, emoji_filename):
    server = message.guild
    emoji_list = server.emojis
    emoji_list_str = ''

    if emoji_list:
        for emoji in emoji_list:
            if emoji.is_usable():
                emoji_list_str += f"<:{emoji.name}:{emoji.id}>\n"

    with open(emoji_filename, 'a') as file:
        file.write(emoji_list_str)

    print(f"Emoji saved to.. {emoji_filename}")

#Emoji Nuke
async def emoji_nuke(message, emoji_filename, max_emotes = 6, limit=None):
    emojis = []
    
    with open(emoji_filename, 'r') as file:
        for line in file:
            emojis.append(line.strip())

    amount_of_emotes = len(emojis)
    
    async for message in message.channel.history(limit=limit):
        for i in range(0,max_emotes):
            random_number = random.randint(0, amount_of_emotes-1)
            await message.add_reaction(emojis[random_number])

#Send a message
async def send_message(message, response, is_private, tts=False):
    try:
        if is_private:
            await message.author.send(response, tts=tts)  
        else: 
            await message.channel.send(response, tts=tts)
    except Exception as e:
        print(e)


#Send a file
async def send_file(message, file_path):
    with open(file_path, 'rb') as file:
        file_data = discord.File(file)
        await message.author.send(file=file_data)

    print(f"Sending file to.. {message.author}")


#Get the channel the user is identifying
async def get_channel(message):
    target_channel = message.content.split()[1]
    server = message.guild
    channel = None

    for c in server.channels:
        if isinstance(c, discord.TextChannel) and c.name == target_channel:
            channel = c
            print(f"Channel Found at: {channel.name}")
            break

    if(channel == None):
        print("No Channel Found")

    return channel
