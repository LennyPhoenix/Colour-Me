import discord
from discord.ext import commands

import os


class Bot(commands.Bot):
    bot_roles = {}
    main_colour = discord.Colour.from_rgb(80, 0, 255)

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix=[
                "colour ",
                "color ",
                "colour",
                "color",
                "Colour ",
                "Color ",
                "Colour",
                "Color",
            ],
            case_insensitive=True,
            intents=intents,
        )
        self.remove_command("help")

    def get_bot_role(self, guild: discord.Guild):
        if guild.id in self.bot_roles.keys():
            return self.bot_roles[guild.id]
        for role in guild.me.roles:
            if len(role.members) == 1 and role.members[0] == guild.me:
                self.bot_roles[guild.id] = role
                return role

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found!",
                description="That command could not be found.",
                colour=self.main_colour,
            )

        if isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(
                title="Error: Bad Argument",
                description="Make sure you are providing a hex-code.",
                colour=self.main_colour,
            )

        embed = discord.Embed(
            title="Error!",
            description=f"""
```py
{error}
```
""",
            colour=self.main_colour,
        )
        await ctx.send(embed=embed)

    async def on_ready(self):
        if self.user is not None:
            print(f"Logged in as {self.user} with id {self.user.id}.")

            game = discord.Game("with colour. | colour help")
            await self.change_presence(status=discord.Status.online, activity=game)

            await self.load_extension("ext.colour_roles")
            await self.load_extension("ext.misc")
            await self.load_extension("ext.topgg")
        else:
            print("User is none, something went wrong...")

    async def on_message(self, message):
        # Ignore Bot
        if message.author.bot:
            return

        # Process Commands
        await self.process_commands(message)


if __name__ == "__main__":
    colour_bot = Bot()
    token = os.environ.get("TOKEN")

    if token is not None:
        colour_bot.run(token)
    else:
        print("Failed to start bot, TOKEN environment variable is not set.")
