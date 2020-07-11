#!/usr/bin/python3

import discord
import requests
import secrets

class StalkBot(discord.Client):
    async def on_message(self, message):
        # check if bot posted
        if message.author == self.user: return

        if message.content[0] == '!':
            # check if valid command
            command = message.content.split(' ')
            print(command)
            if command[0] == '!stalk':
                try:
                    print(command[1])
                except:
                    err_string = ("Invalid command!\n" "Available commands:\n"
                                    "\tprice <stalk price> <am/pm>")
                    await message.channel.send(err_string)
                 
        # print('Message from {0.author}: {0.content}'.format(message))

if __name__ == "__main__":
    bot = StalkBot()
    bot.run(secrets.A_TOKEN)

    # use api from Turnip Calculator (https://ac-turnip.com/) to predict
        # want to find out how they are actually doing this but damn
        # if their site aint nice as hell
    # r = requests.get('https://api.ac-turnip.com/data/?f=-129-93-160-193-168-46')
    # print(r.json())