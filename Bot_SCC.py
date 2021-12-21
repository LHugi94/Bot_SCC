import discord as dc
import secrets
import string
from discord import role
import lichess.api as lia

def createPW():
    chars = string.digits + string.ascii_letters + string.punctuation
    pw = ''.join(secrets.choice(chars) for _ in range(40))
    return pw

def rateUser(tbr, role):
    tbr = tbr.split('@/')[1]
    liUser = lia.user(tbr)
    numberOfGames = [0,0,0,0,0]
    formats = ['blitz','bullet','classical','rapid','ultrabullet']
    counter = 0
    while counter < 5:
        numberOfGames[counter] = liUser.get('perfs', {}).get(formats[counter], {}).get('games')
        counter += 1
    ratings = []
    for i in numberOfGames:
        if i < 15:
            i = 0
        else:
            ratings[i] = liUser.get('perfs', {}).get(formats[counter], {}).get('rating')
    maxRating = max(ratings)
    defineRole = [0, 1000,1200,1400,1600,1800,2000,2200]
    counter2 = 0
    for i in defineRole:
        if maxRating >= defineRole[i]:
            counter2 += 1
        elif maxRating < defineRole[i]:
            pass
    role = defineRole[counter2]
    return role

class DcClient(dc.Client):
    #Einloggen
    async def on_ready(self):
        print("I'm ready for the requests!")
    
    #Wenn Nachricht gepostet
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("$givepw "):            
            if str(message.channel.type) == "private":
                await message.author.send(createPW(), delete_after=60)
        
        if message.content.startswith("$rateme "):     
            if str(message.channel.name) == "rollenverifikation":
                tbr = message.content
                rateUser(tbr, role)
                await tbr.add_roles(dc.utils.get(tbr.guild.roles, name=role))

        

#Discord API
client = DcClient()
client.run(Token goes here)
