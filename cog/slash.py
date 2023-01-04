import utils
import discord
import favicon
from discord.ext import commands
from module import PixivDownloader
from saucenao_api import SauceNao


class SlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 傳送訊息到指定ID的使用者或聊天室
    @commands.slash_command(description = "Download illustrates from specific pixiv users.")
    async def pixiv_user(self, ctx, id_or_url, tag:bool=True, limit:int=5):
        self.bot.logger.info(f"'pixiv_user' id_or_url={id_or_url}, tag={tag}, limit={limit}")
        if ctx.author.id==self.bot.owner_id:
            await ctx.respond(">> Processing...")

            pixiv_downloader = PixivDownloader()
            target = ctx

            user_ids = []
            for id in id_or_url.split('/'):
                try:
                    user_ids.append(int(id))
                except ValueError as e:
                    pass

            res = await pixiv_downloader.illust_user(
                user_ids=user_ids,
                limit=limit,
                use_tag=tag,
                output=True
            )
            if res:
                await utils.send_illusts(target=ctx, illusts=res)
                await self.bot.reply(target, "'pixiv_user' Complete")
            else:
                await self.bot.reply(target, "'pixiv_user' No Result Found")

    # @commands.slash_command(description = "I NEED THE SAUCE.")
    # async def sauce(self, ctx, url:str):
    #     if ctx.author.id==self.bot.owner_id:

    #         await ctx.respond(">> Processing...")
    #         sauce = SauceNao(self.bot.json_loader.get(["SauceNao", "api_key"]))
    #         results = sauce.from_url(url.split("?")[0])

    #         if results:
    #             results.short_remaining  # 4  (per 30 seconds limit)
    #             results.long_remaining   # 99 (per day limit)

    #             res = sorted(results, key = lambda res: res.index_id)[0]
                
    #             if res.similarity > 80:
    #                 await ctx.send(f"Similarity: {res.similarity}%")
    #                 embed=discord.Embed(title=res.title, url=res.urls[0])
    #                 icons = favicon.get(res.urls[0])
    #                 embed.set_author(name=res.author, icon_url=icons[0].url)
    #                 embed.set_image(url=res.thumbnail)
    #                 await ctx.send(embed=embed)
    #                 await self.bot.reply(ctx, "'sauce' Complete")
    #             else:
    #                 await self.bot.reply(ctx, "No high similarity result")
    #         else:
    #             await self.bot.reply(ctx, "No high similarity result")
    
def setup(bot):
    bot.add_cog(SlashCog(bot))
