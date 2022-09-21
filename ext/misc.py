import discord
from discord.ext import commands


class Misc(commands.Cog):
    """Miscellaneous commands, such as ping and help."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check the ping of the bot."""
        embed = discord.Embed(
            title="Bot Latency",
            description=f"**{int(self.bot.latency * 100)}**ms",
            colour=self.bot.main_colour,
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Get the bot's invite link."""
        embed = discord.Embed(
            title="Invite the bot with this link:",
            description="https://top.gg/bot/728604287206424637",
            colour=self.bot.main_colour,
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def feedback(self, ctx, *, feedback):
        """Sends the owner feedback."""
        user = self.bot.get_user(425340416531890178)
        embed = discord.Embed(
            title="Feedback:", description=feedback, colour=self.bot.main_colour
        )
        await user.send(ctx.author.mention, embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def help(self, ctx, *, category=None):
        """This command!"""
        if category is None:
            embed = discord.Embed(
                title="Category Listing and Uncatergorized Commands",
                description="""Use `colour help *category*` to find out more about them!""",
                colour=self.bot.main_colour,
            )

            cogs_desc = ""
            for cog in self.bot.cogs:
                if cog != "TopGG":
                    cogs_desc += f"`{cog}` - {self.bot.cogs[cog].__doc__}\n"

            embed.add_field(name="Categories", value=cogs_desc, inline=False)

            cmds = [
                cmd
                for cmd in self.bot.walk_commands()
                if not (cmd.cog_name or cmd.hidden)
            ]
            if len(cmds) > 0:
                cmds_desc = ""
                for cmd in cmds:
                    sig = f"{cmd.name} {cmd.signature}".strip()
                    cmds_desc += f"`{sig}` - {cmd.help}\n"
                embed.add_field(
                    name="Uncatergorized Commands", value=cmds_desc, inline=False
                )
        else:
            bot_cogs = {name.lower(): cog for name, cog in self.bot.cogs.items()}
            if category.lower() in bot_cogs.keys() and category.lower() != "topgg":
                embed = discord.Embed(
                    title=f"{list(self.bot.cogs.keys())[list(self.bot.cogs.values()).index(bot_cogs[category.lower()])]} Command Listing",
                    description=f"{bot_cogs[category.lower()].__doc__}",
                    colour=self.bot.main_colour,
                )

                cmds = list(bot_cogs[category.lower()].walk_commands())

                if len(cmds) > 0:
                    cmds_desc = ""
                    for cmd in cmds:
                        sig = f"{cmd.name} {cmd.signature}".strip()
                        cmds_desc += f"`{sig}` - {cmd.help}\n"
                    embed.add_field(name="Commands", value=cmds_desc, inline=False)
                else:
                    embed.add_field(
                        name="No Commands",
                        value="Maybe they haven't been added yet?",
                        inline=False,
                    )
            else:
                embed = discord.Embed(
                    title="Error!",
                    description=f"The category `{category}` doesn't even exist!",
                    colour=self.bot.main_colour,
                )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
