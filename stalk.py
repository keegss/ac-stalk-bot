#!/usr/bin/python3

"""stalk.py
Main interface between Discord and Bot. Processes all incoming messages
looking for stalk commands.
"""

from datetime import date
import discord
import requests
import secrets
from mongo import Mongo
from tabulate import tabulate

class StalkBot(discord.Client):

    available_commands = ("Available commands:"
                        "\n\tprice <stalk price> <am/pm>"
                        "\n\tset <day> <stalk price> <am/pm>"
                        "\n\tpredict"
                        "\n\tinfo"
                        "\n\tclear")

    err_string = ("Invalid command!\n" + available_commands)

    mongo = Mongo()


    async def on_message(self, message):
        """
        @brief Async callback called after any message is posted to server
        @param message - message data
        """

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
            await self.info(message)
        elif cmd_type == 'info':
            await self.info(message)
        elif cmd_type == 'clear':
            await self.clear(message)
        elif cmd_type == 'help':
            await self.help(message)
        elif cmd_type == 'fish':
            await self.get_fish(message)
        else:
            await message.channel.send(self.err_string)
            return
                 
    async def price(self, message, command):
        """
        @brief Verify price command and send user price data to database
        @param message - message data
        @param command - command to be verified
        """

        try:
            if len(command) == 2:
                day = None
                price = command[0]
                am_or_pm = command[1]
            else:
                day = command[0]
                price = command[1]
                am_or_pm = command[2]
        except:
            await message.channel.send(self.err_string)
            return

        user = message.author
        price_err_str = ('Invalid price command;\n' 
                         'Example use: !stalk price <day (optional)> <cost as integer> <string am or pm>')

        days = {'monday' : 0, 'tuesday' : 1, 'wednesday' : 2, 'thursday' : 3, 'friday' : 4, 'saturday' : 5}

        # verify command input
        if day and (not isinstance(day, str) or day.lower() not in days):
            await message.channel.send(price_err_str)
            return
        elif not price.isnumeric() or not isinstance(am_or_pm, str) or \
                                    not (am_or_pm == 'am' or am_or_pm == 'pm'):
            await message.channel.send(price_err_str)
            return

        formatted_user_data = self.mongo.enter_user_price(str(user), price, am_or_pm, days[day.lower()] if day else None)
        await message.channel.send(formatted_user_data)
    
    async def info(self, message):
        """
        @brief Retrieve info on user
        @param message - message data
        """

        user = str(message.author)
        user_data = self.mongo.formatted_user_data(user)
        if user_data:
            await message.channel.send('User Data for {}\n{}'.format(user, user_data))
            await message.channel.send(file=discord.File('img.png'))
        else:
            await message.channel.send('No data for user {}!'.format(user))
    
    async def clear(self, message):
        """
        @brief Clear data on user
        @param message - message data
        """

        user = str(message.author)
        self.mongo.reset_user(user)
        await message.channel.send('Cleared data for user {}'.format(user))

    async def get_fish(self, message):
        """
        @brief Retrieve and send formatted fish data
        @param message - message data
        """

        curr_month = date.today().month
        fish_data = requests.get('http://acnhapi.com/v1/fish')
        available_fish = []
        for fish, data in fish_data.json().items():
            if data['availability']['isAllYear']:
                available_fish.append((data['name']['name-USen'],
                                    data['availability']['location'],
                                    data['availability']['rarity'],
                                    data['price'],
                                    data['price-cj']))
                continue

            # print(fish, data)
            months_available = data['availability']['month-northern'].split('&')
            ranges = []
            for months in months_available:
                ranges.append(months.strip().split('-'))
            for r in ranges:
                if curr_month >= int(r[0]) and curr_month <= int(r[1]):
                    available_fish.append((data['name']['name-USen'], 
                                        data['availability']['location'],
                                        data['availability']['rarity'],
                                        data['price'],
                                        data['price-cj']))
                    break

        res = tabulate(available_fish, headers=['Name', 'Location', 'Rarity', 
                                                'Price', 'CJ Price'])
        res = '```\n' + res + '\n```\n'
        await message.channel.send(res)

    async def help(self, message):
        await message.channel.send(self.available_commands)

if __name__ == "__main__":
    bot = StalkBot()
    bot.run(secrets.A_TOKEN)
    bot.mongo.close()