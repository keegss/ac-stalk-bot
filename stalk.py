#!/usr/bin/python3

import discord
import requests
import secrets
from mongo import Mongo

class StalkBot(discord.Client):

    err_string = ("Invalid command!\n" "Available commands:"
                        "\n\tprice <stalk price> <am/pm>"
                        "\n\tpredict")

    mongo = Mongo()

    async def on_message(self, message):
        # ignore if bot post
        if message.author == self.user: return

        command = message.content.split(' ')

        # verify if command
        if command[0] != '!stalk':
            return

        # verify command present
        try:
            cmd_type = command[1]
        except:
            await message.channel.send(self.err_string)
            return

        # handle command
        if cmd_type == 'price':
            await self.price(message, command[2:])
        elif cmd_type == 'predict':
            await self.predict(message)
        else:
            await message.channel.send(self.err_string)
            return
                 
    async def price(self, message, command):
        try:
            price = command[0]
            am_or_pm = command[1]
        except:
            await message.channel.send(self.err_string)
            return

        user = message.author

        # verify command input
        if not price.isnumeric() or not isinstance(am_or_pm, str) or \
                                    not (am_or_pm == 'am' or am_or_pm == 'pm'):
            await message.channel.send(('Invalid price command;\n' 
                                        'Example use: !stalk price <cost as integer> <string am or pm>'))
            return

        self.mongo.enter_user_price(str(user), price, am_or_pm)

    async def predict(self, message):
        user = str(message.author)
        res = self.mongo.predict(user)
        if res:
            await message.channel.send('Predict for {}.\nWeek Min Max: {}\nWeek Average Pattern: {}'.format(user, res[0], res[1]))
        else:
            await message.channel.send('No data for user {}!'.format(user))

if __name__ == "__main__":
    bot = StalkBot()
    bot.run(secrets.A_TOKEN)
    bot.mongo.close()