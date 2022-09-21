from discord.ext import commands
from topgg.client import DBLClient

import os


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ.get("TOPGG_TOKEN")
        if self.token is not None:
            self.topgg = DBLClient(self.bot, self.token, autopost=True)
        else:
            print(
                "Failed to initialise top.gg client, TOPGG_TOKEN environment variable not set."
            )

    async def on_autopost_success(self):
        print("Server count posted successfully")


async def setup(bot: commands.Bot):
    await bot.add_cog(TopGG(bot))
