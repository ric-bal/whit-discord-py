import os
from typing import Optional
import discord
from discord import FFmpegPCMAudio
import discord.ext
import asyncio
from googlesearch import search
import random

from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

ID = os.getenv("ID")


@client.event
async def on_ready():
  await tree.sync(guild=discord.Object(id=ID))
  print(f"{client.user} is now running!")

  try:
    synced = await tree.sync()
    print(f"synced {len(synced)} command(s)")
  except Exception as e:
    print(e)



# spin the wheel embed and button
new_list = []

def setNewList(items): # set new list, called from 'spin the wheel' slash command 
  global new_list
  new_list = items

class SpinAgainButton(discord.ui.View):
  def __init__(self):
    super().__init__()

  @discord.ui.button(label="Spin Again", style=discord.ButtonStyle.blurple)
  async def rollButton(self, interaction: discord.Interaction, button: discord.ui.Button):
    random_num = random.randint(0, len(new_list) - 1)
    joined_list = ', '.join(new_list)


    script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
    script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
    rel_path = "files/imgs/spin the wheel.png" #"files/imgs/spin the wheel.png"
    abs_file_path = os.path.join(script_dir, rel_path)

    file = discord.File(abs_file_path, filename="image.png")


    embedVar = discord.Embed(title=new_list[random_num] + "!", 
                            color=discord.Colour.blurple())
    embedVar.add_field(name="Possible Choices   ", 
                      value=joined_list, 
                      inline=True)
    embedVar.add_field(name="Result", 
                      value=new_list[random_num], 
                      inline=True)
    embedVar.set_image(url="attachment://image.png")

    await interaction.message.delete()
    await interaction.channel.send(file=file, embed=embedVar)
    await interaction.channel.send(view=SpinAgainButton())
  


# ------------------------------  COMMANDS ---------------------------------------------



#hello
@tree.command(name="hello", description="Say hello to Whit")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(
    f"Sending 2PB zip bomb to user {interaction.user.mention}")




# say
@tree.command(name="say", description="Whit repeats what you say")
async def say(interaction: discord.Interaction, text: str):
  await interaction.response.send_message(text)




# picture
@tree.command(name="picture", description="Whit will send a random picture")
async def picture(interaction: discord.Interaction):
  script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
  script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
  rel_path = "files/imgs/orange.jpeg"
  abs_file_path = os.path.join(script_dir, rel_path)
  
  await interaction.response.send_message(file=discord.File(abs_file_path))




# one thousand pings
@tree.command(name="one-thousand-pings",
              description="Whit will ping a chosen user one thousand times")
async def pings(interaction: discord.Interaction, user: discord.Member):
  script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
  script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
  rel_path = "files/imgs/orange.jpeg"
  abs_file_path = os.path.join(script_dir, rel_path)
  
  await interaction.response.send_message(file=discord.File(abs_file_path))




# dont google
@tree.command(
  name="dont-google",
  description=
  "Whit does not google something for you"
)
async def dont_google(interaction: discord.Interaction,
                      query: str,
                      results_returned: int = 1):
  await interaction.response.send_message(f'Showing results for "{query}":')

  for value in search(query, tld="co.in", num=results_returned, stop=results_returned, pause=0.2):
    await interaction.channel.send(f"{value}")




# spin the wheel
@tree.command(
  name="spin-the-wheel",
  description=
  "Whit randomly chooses an item from a list of items. (( IMPORTANT: Separate items with a comma ))"
)
async def spin(interaction: discord.Interaction,
                      list: str):
  list = list.split(',')
  new_list = []           # defined above wheel spin class button (scroll up)
  for item in list:
    item = item.strip()
    new_list.append(item)

  random_num = random.randint(0, len(new_list) - 1)
  joined_list = ', '.join(new_list)


  script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
  script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
  rel_path = "files/imgs/spin the wheel.png" #"files/imgs/spin the wheel.png"
  abs_file_path = os.path.join(script_dir, rel_path)

  file = discord.File(abs_file_path, filename="image.png")


  embedVar = discord.Embed(title=new_list[random_num] + "!", 
                           color=discord.Colour.blurple())
  embedVar.add_field(name="Possible Choices   ", 
                     value=joined_list, 
                     inline=True)
  embedVar.add_field(name="Result", 
                     value=new_list[random_num], 
                     inline=True)
  embedVar.set_image(url="attachment://image.png")

  setNewList(new_list)
  await interaction.response.send_message(file=file, embed=embedVar)
  await interaction.channel.send(view=SpinAgainButton())





# vc ping add
@tree.command(name="add-vc-ping",
              description="Whit will ping you if someone joins vc")
async def vc_ping_add(interaction: discord.Interaction):
  found = False
  with open('ping_users.txt', 'r') as file:
    for row in file:
      if interaction.user.mention == row.strip():
        found = True

  if found == False:
    with open('ping_users.txt', 'a') as file:
      file.write(interaction.user.mention + "\n")
      file.close()
    await interaction.response.send_message("I've added you to the list", ephemeral=True)
    return
  await interaction.response.send_message("You're already in the list", ephemeral=True)


# vc ping remove
@tree.command(name="remove-vc-ping",
              description="Whit will remove you from the vc ping list")
async def vc_ping_remove(interaction: discord.Interaction):
  found = False
  lines = []
  with open('ping_users.txt', 'r') as file:
    for row in file:
      if interaction.user.mention == row.strip():
        found = True
    lines = file.readlines()

  if found == True:
    with open("ping_users.txt", "w") as file:
      for line in lines:
        if line.strip("\n") != interaction.user.mention:
          file.write(line)

    await interaction.response.send_message("I've removed you from the list", ephemeral=True)
    return

  await interaction.response.send_message("You're not in the list", ephemeral=True)




# toggle entrance music 
@tree.command(
  name="toggle-join-audio",
  description="Whit plays special audio everytime someone joins vc"
)
async def entrance_music(interaction: discord.Interaction):
  global canPlayAudio

  if canPlayAudio:
    canPlayAudio = False
  else:
    canPlayAudio = True

  embedVar = discord.Embed(title="TOGGLE", description="Play join audio:    " + "`" + str(canPlayAudio) + "`", color=discord.Colour.blurple())
  await interaction.response.send_message(embed=embedVar)




# someone joins vc, inclueds special join audio
canPlayAudio = True

@client.event
async def on_voice_state_update(member, before, after):
  # determining sound file path
  script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
  script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
  rel_path = "files/sound/clown music.mp3"
  abs_file_path = os.path.join(script_dir, rel_path)

  ffmpeg_path = os.path.join(script_dir, "ffmpeg_bins/ffmpeg")

  if member != client.user and before.channel != after.channel:
    if len(client.voice_clients) == 1:      # disconnect if vc is empty (triggered whenever someone joins/leaves)
      for vc in client.voice_clients: 
        if vc.guild == member.guild:
          source = discord.FFmpegPCMAudio(executable=ffmpeg_path, source=abs_file_path, before_options="-ss 00:02:31:99") # easy way to terminate ffmpeg player, skips to almost end of song
          player = vc.pause()
          player = vc.play(source)
          await asyncio.sleep(0.01)
          await vc.disconnect()


  if member == client.user:
    return
  
  if not before.channel and after.channel:
    channel = client.get_channel(1134500945691156560)      # text channel
    vchannel = member.voice.channel                        # voice channel
    
    # ping users if someone joined vc
    with open('ping_users.txt', 'r') as file:
      for row in file:
        if not row.isspace():
          await channel.send(row, delete_after=5)

    # special music plays if someone joins vc
    if canPlayAudio:
      for vc in client.voice_clients: 
        if vc.guild == member.guild:
          await vc.disconnect()


      await asyncio.sleep(0.02) # throws errors if not here, i dont know why, dont delete this (if still throwing errors, increase time) 
      
      try:
        voice = await vchannel.connect()
      except Exception as e:
        embedVar = discord.Embed(title="ERROR", description=(str(e) + " (Wait a few minutes for discord to fail voice handshake)"), color=discord.Colour.blurple())
        await channel.send(embed=embedVar)

      source = discord.FFmpegPCMAudio(executable=ffmpeg_path, source=abs_file_path)
      player = voice.play(source)
      


# running the bot
TOKEN = os.environ.get("TOKEN")
client.run(TOKEN)

client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="hold music"))







"""
# get whit into vc
@tree.command(
  name="join-vc",
  description="Whit joins vc"
)
async def join(interaction: discord.Interaction):  
  try:
    channel = interaction.user.voice.channel
  except AttributeError:
    await interaction.response.send_message("You're not in vc", ephemeral=True)
    return

  if interaction.client.voice_clients: # check if array is not empty (bot is is vc)
    if interaction.guild.voice_client.channel == channel: # check if target channel is same as current channel
      await interaction.response.send_message("I'm already in the same vc as you", ephemeral=True)
      return
      
    await interaction.guild.voice_client.disconnect() 

  await channel.connect()
  await interaction.response.send_message("Joined vc", ephemeral=True)

"""

