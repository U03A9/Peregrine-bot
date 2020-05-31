import discord
import re

class Peregrine(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.lower())
        summary = "Testing 1 ... 2 ... 3"

        # Prevent bot replying to self

        if message.author.id == self.user.id:
            return

        # Check if poster has moderation bypass

        #

        # Check if URL exists in message. If so, submit to HA

        if urls:
            storedurl = urls
            testmessage = await message.channel.send("Captured URL is: {}".format(storedurl))
            await message.delete()
            botmessage = await message.channel.send('The URL has been submitted to Hybrid-Analysis for evaluation. Awaiting report...'.format(message))

            # Generate report with Hybrid Analysis

            # Edit previous message and add URL for report

            # Query status loop..

            # Edit message further with summary and unclickable urls

            await botmessage.edit(content = summary)
            await testmessage.delete(delay=5)
            await botmessage.delete(delay=5)

client = Peregrine()
client.run('token')
