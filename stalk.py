import discord
import secrets

class StalkBot(discord.Client):
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

if __name__ == "__main__":
    bot = StalkBot()
    bot.run(secrets.A_TOKEN)