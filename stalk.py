#!/usr/bin/python3

import discord
import requests
import secrets

class StalkBot(discord.Client):

    err_string = ("Invalid command!\n" "Available commands:\n"
                        "\tprice <stalk price> <am/pm>")

    async def on_message(self, message):
        # ignore if bot post
        if message.author == self.user: return

        command = message.content.split(' ')

        # verify if command
        if command[0] != '!stalk':
            return


        # verify command present and handle
        try:
            cmd_type = command[1]
        except:
            await message.channel.send(self.err_string)
            return

        if cmd_type == 'price':
            try:
                price = command[2]
                am_or_pm = command[3]
            except:
                await message.channel.send(self.err_string)
                return

            self.price(message, price, am_or_pm)
        elif cmd_type == 'predict':
            self.predict(message)
        else:
            await message.channel.send(self.err_string)
            return
                 
    async def price(self, message, price, am_or_pm):
        user = message.author
        print(user)
        print(price)
        print(am_or_pm)
        # verify input
        if not isinstance(price, int) or not isinstance(am_or_pm, str):
            await message.channel.send(('Invalid price command;\n' 
                                        'Example use: !stalk price <cost as integer> <string am or pm>'))
            return

        # for user
            # store price for current day as am/pm
            # in db

    async def predict(self, message):
        # for user
            # retrieve current week prices so far from database
            # use Turnip Calculator to get current prediction
        # r = requests.get('https://api.ac-turnip.com/data/?f=-129-93-160-193-168-46')
        # print(r.json())

if __name__ == "__main__":
    bot = StalkBot()
    bot.run(secrets.A_TOKEN)