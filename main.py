import discord, os, config, logging
from discord.ext import commands

logging.basicConfig(
    handlers=[logging.FileHandler("./log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=config.prefix, case_insensitive=True, intents=intents
        )

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error


client = Client()

# help command
class MinimalHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=config.embed_color)
            await destination.send(embed=emby)


client.help_command = MinimalHelpCommand()


@client.event
async def on_ready():
    print("Logged in as {0} ({0.id})".format(client.user))


client.run(config.token, reconnect=True)
