import discord as dc
import secrets
import string
from discord import role
import lichess.api as lia

roli = 0

def createPW(): #function used to create a safe password if needed
    chars = string.digits + string.ascii_letters + string.punctuation
    pw = ''.join(secrets.choice(chars) for _ in range(40))
    return pw

def rateUser(tbr, roli): #function that provides discord role belonging to lichess rating
    tbr = tbr.split('@/')[1]
    liUser = lia.user(tbr)
    numberOfGames = [0,0,0,0,0]
    formats = ['blitz','bullet','classical','rapid','ultrabullet']
    counter = 0
    while counter < 5:
        try:
            numberOfGames[counter] = int(liUser.get('perfs', {}).get(formats[counter], {}).get('games'))
        except TypeError:
            numberOfGames[counter] = 0
        counter += 1
    ratings = [0,0,0,0,0]
    counter3 = 0
    while counter3 < 5:
        if numberOfGames[counter3] < 15:
            ratings[counter3] = 0
            counter3 += 1
        else:
            ratings[counter3] = liUser.get('perfs', {}).get(formats[counter3], {}).get('rating')
            counter3 += 1
    maxRating = max(ratings)
    defineRole = [0, 1000,1200,1400,1600,1800,2000,2200]
    counter2 = 0
    counter4 = 0
    while counter4 < 5:
        if maxRating >= defineRole[counter4]:
            counter2 += 1
            counter4 += 1
        elif maxRating < defineRole[counter4]:
            break
    roli = defineRole[counter2]
    roli = str(roli)
    print(roli)
    return roli

class DcClient(dc.Client): #defining client
    #logging in
    async def on_ready(self):
        print("I'm ready for the requests!")
          
    #message handling
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("$givepw "):            
            if str(message.channel.type) == "private":
                await message.author.send(createPW(), delete_after=60)
        
        if message.content.startswith("$rateme "):     
            if str(message.channel.name) == "rollenverifikation":
                tbr = message.content
                tbrDC = message.author
                rateUser(tbr, roli)
                await tbrDC.add_roles(dc.utils.get(tbrDC.guild.roles, name=role))

    #Discord API
client = DcClient() #initializing client
client.run('Token goes here')