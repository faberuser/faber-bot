import discord
import re
import aiohttp
import asyncio
import config
import random
import time
from discord.ext import commands


class Pandora(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author == message.author.bot
            or message.author == self.client.user
            or message.mention_everyone
        ):
            return
        if self.client.user in message.mentions or isinstance(
            message.channel, discord.channel.DMChannel
        ):
            async with message.channel.typing():
                try:
                    input = re.sub(
                        "<@!?{0.user.id}>".format(
                            self.client), "", message.content
                    ).strip()
                    print("{0}: ".format(message.author) + input)
                    params = {
                        "botid": config.botID,
                        "custid": message.author.id,
                        "input": input.strip("?") or "Hello",
                    }
                    session = aiohttp.ClientSession()
                    resp = await session.get(
                        "https://www.pandorabots.com/pandora/talk-xml", params=params
                    )
                    if resp.status == 200:
                        text = await resp.text()
                        text = text[text.find(
                            "<that>") + 6: text.rfind("</that>")]
                        text = (
                            text.replace("&quot;", '"')
                            .replace("&lt;", "<")
                            .replace("&gt;", ">")
                            .replace("&amp;", "&")
                            .replace("<br>", " ")
                            .replace("<a", "")
                            .replace('href="', "")
                            .replace('" target="_blank">', "")
                            .replace("</a>", "")
                        )
                        print("{0.user}: ".format(self.client) + text)
                        await message.reply(text)
                    else:
                        await message.reply(random.choice(config.error_message))
                    await session.close()
                except asyncio.TimeoutError:
                    await message.reply("i think im drunk")


async def setup(client):
    await client.add_cog(Pandora(client))
