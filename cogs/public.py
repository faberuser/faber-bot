import discord
import asyncio
import sys
import aiohttp
import config
from discord.ext import commands


class Public(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(417728433112612866)
        role = guild.get_role(610043053578780693)

        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return

        elif message.channel.id == 515155645020897280:
            prefixes = [";;", "."]
            ids = [184405311681986560, 547905866255433758, 945683386100514827]
            if message.content.startswith(tuple(prefixes)):
                await asyncio.sleep(60)
                await message.delete()
            elif message.author.id in ids:
                await asyncio.sleep(60)
                await message.delete()

    @commands.command(aliases=["client", "info", "infos"])
    async def bot(self, ctx):
        embed = discord.Embed(
            title="Bot Information",
            description="Owned by Faber#4622",
            colour=config.embed_color,
        )
        embed.add_field(name="**Python**", value=f"`{sys.version}`")
        embed.add_field(name="**discord.py**",
                        value=f"`{discord.__version__}`")
        await ctx.reply(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Bot Invite",
            url="https://discord.com/oauth2/authorize?client_id=1002148185290067999&scope=bot%20applications.commands&permissions=8",
            colour=config.embed_color,
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["pong"])  # ping from server to API
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.client.latency * 1000)}ms",
            colour=config.embed_color,
        )
        await ctx.reply(embed=embed)

    # get userinfo from self or a server member
    @commands.command(aliases=["user"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is not None:
            au = member
        if member is None:
            au = ctx.author
        roles = [role for role in au.roles]

        embed = discord.Embed(color=au.color)
        embed.set_author(name=f"{au}", icon_url=au.avatar_url)
        embed.set_image(url=au.avatar_url)
        # embed.add_field(
        #     name="Joined at:",
        #     value=au.joined_at.strftime("%A, %d. %B %Y at %H:%M:%S"))
        # embed.add_field(
        #     name="Created at:",
        #     value=au.created_at.strftime("%A, %d. %B %Y at %H:%M:%S"),
        # )
        # embed.add_field(
        #     name=f"Roles ({len(roles)-1}):",
        #     value=" ".join([role.mention for role in roles])[22:],
        # )
        embed.add_field(name="Top role:", value=au.top_role.mention)
        embed.add_field(name="Bot ?", value=au.bot)
        embed.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()  # get avatar from self or a server member
    async def avatar(self, ctx, member: discord.Member = None):
        if member is not None:
            au = member
        if member is None:
            au = ctx.author
        url_ = au.avatar_url
        embed = discord.Embed(title=f"{au}", colour=config.embed_color)
        embed.set_image(url=url_)
        embed.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def banner(self, ctx, member: discord.Member = None):
        if member is not None:
            user_id = member.id
            au = member
        if member is None:
            user_id = ctx.author.id
            au = ctx.author

        resolution = 1024
        endpoints = (
            "https://cdn.discordapp.com/banners/",
            "https://discord.com/api/v9/users/{}".format(user_id),
        )

        headers = {"Authorization": f"Bot {config.token}"}

        embed = discord.Embed(title=f"{au}", colour=config.embed_color)
        embed.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(endpoints[1]) as response:
                data = await response.json()
                try:
                    url = (
                        endpoints[0]
                        + str(user_id)
                        + "/"
                        + data["banner"]
                        + "?size={0}".format(resolution)
                    )
                    embed.set_image(url=url)
                    await ctx.reply(embed=embed)
                except:
                    await ctx.reply("User has no banner")

    @commands.command(aliases=["server"])  # get server info
    async def serverinfo(self, ctx):
        roles = [role for role in ctx.guild.roles]
        role_length = len(roles)

        if role_length > 50:
            roles = roles[:50]
            roles.append(">>>> [50/%s]Roles" % len(roles))

        roles = ", ".join(role.mention for role in roles)
        textchannel = len(ctx.guild.text_channels)
        voicechannel = len(ctx.guild.voice_channels)
        boostguys = len(ctx.guild.premium_subscribers)
        regional = str(ctx.guild.region)

        embed = discord.Embed(colour=config.embed_color)
        embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.add_field(name="Member count:", value=ctx.guild.member_count)
        embed.add_field(name="Member boost:", value=boostguys)
        embed.add_field(name="Nitro Boost level",
                        value=str(ctx.guild.premium_tier))
        embed.add_field(
            name="Text/Voice Channels:", value=f"{textchannel}/{voicechannel}"
        )
        embed.add_field(
            name="Do moderators require 2FA?",
            value="Yes" if ctx.guild.mfa_level == 1 else "No",
        )
        embed.add_field(name="Owner:", value=ctx.guild.owner)
        embed.add_field(
            name="Created at:",
            value=ctx.guild.created_at.strftime("%A, %d. %B %Y at %H:%M:%S"),
        )
        embed.add_field(name="Region:", value=regional)
        embed.add_field(name="Roles:", value=roles[23:])
        await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(Public(client))
