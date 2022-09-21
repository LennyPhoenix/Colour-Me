import random

import discord
from discord.ext import commands


class ColourRoles(commands.Cog, name="Colour Roles"):
    """Colour Roles commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_colour_roles(self, guild: discord.Guild):
        roles = await guild.fetch_roles()
        for role in roles:
            if role == guild.default_role:
                continue

            if (
                role.name.startswith("#")
                and len(role.name) == 7
                and role.name == role.name.lower()
            ):
                yield role

    async def clear_member_colour_roles(self, ctx: commands.Context):
        if ctx.guild is not None:
            remove = []
            async for role in self.get_colour_roles(ctx.guild):
                if ctx.author in role.members:
                    remove.append(role)

            await ctx.author.remove_roles(*remove, reason="Colour Me role.")

    async def delete_unused_colour_roles(self, ctx: commands.Context):
        if ctx.guild is not None:
            async for role in self.get_colour_roles(ctx.guild):
                if len(role.members) <= 0:
                    await role.delete(reason="Colour Me role.")

    async def give_colour_role(self, ctx: commands.Context, colour: discord.Colour):
        if ctx.guild is not None:
            add_role: discord.Role | None = None

            async for role in self.get_colour_roles(ctx.guild):
                if role.colour == colour:
                    add_role = role
                    break

            if add_role is None:
                add_role = await ctx.guild.create_role(
                    name=str(colour), colour=colour, reason="Colour Me role."
                )

            await ctx.author.add_roles(add_role, reason="Colour Me role.")

    @commands.command()
    async def me(self, ctx: commands.Context, *, colour: discord.Colour):
        """Gives you a role to make you any colour! (Provide a Hex-Code)"""
        await self.clear_member_colour_roles(ctx)
        await self.give_colour_role(ctx, colour)
        await self.delete_unused_colour_roles(ctx)

        await ctx.message.add_reaction("✅")

    @commands.command()
    async def random(self, ctx: commands.Context):
        """Gives you a random colour."""
        colour = discord.Colour.from_rgb(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        await self.clear_member_colour_roles(ctx)
        await self.give_colour_role(ctx, colour)
        await self.delete_unused_colour_roles(ctx)

        await ctx.message.add_reaction("✅")

        await ctx.send(f"Applied colour `{colour}`.")

    @commands.command()
    async def clear(self, ctx: commands.Context):
        """Removes your colour role."""
        await self.clear_member_colour_roles(ctx)
        await self.delete_unused_colour_roles(ctx)

        await ctx.message.add_reaction("✅")


async def setup(bot: commands.Bot):
    await bot.add_cog(ColourRoles(bot))
