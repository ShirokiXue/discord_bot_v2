import argparse
import shlex

import utils
from discord.ext import commands
from module import *


class PixivCmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 下載給定的Pixiv User之作品
    # @commands.slash_command(name="first_slash", guild_ids=[633116359714406420])
    @commands.command
    async def pixiv_user(self, ctx, *, user_input:str=""):
        if ctx.author.id==self.bot.owner_id:

            parser = argparse.ArgumentParser(description='Argparse for discord bot.')
            parser.add_argument("user_ids", help="must be an id of a pixiv user", type=str)
            parser.add_argument("-t", "--tag", help="whether use tag_list for filtering", action="store_true")
            parser.add_argument("-l", "--limit", type=int, default=5, help="limit the number of output image")
            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                if e.code==2: await self.bot.reply(ctx, "Wrong Input")
                return

            pixiv_downloader = PixivDownloader()
            target = ctx
            user_ids = []
            for id in args.user_ids.split('/'):
                try:
                    user_ids.append(int(id))
                except ValueError as e:
                    pass
                
            await self.bot.reply(target, "Processing...")
            res = await pixiv_downloader.illust_user(
                user_ids=user_ids,
                limit=args.limit,
                use_tag=args.tag,
                output=False
            )
            await utils.send_illusts(target=ctx, illusts=res)
            await self.bot.reply(target, "'pixiv_user' Complete")

    # 下載追蹤中的Pixiv User之作品
    @commands.command()
    async def pixiv_follow(self, ctx, *, user_input:str=""):
        if ctx.message.author.id==self.bot.owner_id:

            parser = argparse.ArgumentParser(description='Argparse for discord bot.')
            parser.add_argument("-t", "--tag", help="whether use tag_list for filtering", action="store_true")
            parser.add_argument("-l", "--limit", type=int, default=5, help="limit the number of output image")
            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                if e.code==2: await self.bot.reply(ctx, "Wrong Input")
                return

            pixiv_downloader = PixivDownloader()
            target = ctx
            await self.bot.reply(target, "Processing...")
            res = await pixiv_downloader.illust_follow(
                limit=args.limit,
                use_tag=args.tag,
                output=False
            )

            await utils.send_illusts(target=ctx, illusts=res)
            await self.bot.reply(target, "'pixiv_follow' Complete")

    # 下載排行榜上之作品
    # all_mode = ["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie", 
    #             "day_r18", "day_male_r18", "day_female_r18", "week_r18", "week_r18g"]
    @commands.command()
    async def pixiv_ranking(self, ctx, *, user_input:str=""):
        if ctx.message.author.id==self.bot.owner_id:

            parser = argparse.ArgumentParser(description='Argparse for discord bot.')
            parser.add_argument("-t", "--tag", help="whether use tag_list for filtering", action="store_true")
            parser.add_argument("-l", "--limit", type=int, default=5, help="limit the number of output image")
            parser.add_argument("-m", "--mode", type=str, default="day", help="mode of ranking")
            try:
                args = parser.parse_args(shlex.split(user_input))
            except SystemExit as e:
                if e.code==2: await self.bot.reply(ctx, "Wrong Input")
                return

            pixiv_downloader = PixivDownloader()
            target = ctx
            await self.bot.reply(target, "Processing...")
            res = await pixiv_downloader.illust_ranking(
                limit=args.limit,
                use_tag=args.tag,
                mode=args.mode,
                output=True
            )

            await utils.send_illusts(target=ctx, illusts=res)
            await self.bot.reply(target, "'pixiv_follow' Complete")

def setup(bot):
    bot.add_cog(PixivCmdCog(bot))
