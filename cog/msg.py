import discord
import utils
from discord.ext import commands
from module import PixivDownloader

class Msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):

        owner = self.bot.get_user(self.bot.owner_id)

        # DM
        if type(msg.channel) == discord.DMChannel:

            # 他人DM
            if msg.author.id not in [self.bot.user.id, self.bot.owner_id]:
                message = f"<@!{msg.author.id}> >> {msg.content}"
                await owner.send(message)

            # 我的DM
            if msg.author.id == self.bot.owner_id:
            
                # quick_pixiv_user
                if "https://www.pixiv.net/users/" in msg.content:
                    await owner.send(">> 'quick_pixiv_user' Processing...")
                    target = self.bot.get_channel(self.bot.json_loader.get(
                        ['text_channel_id', 'pixiv_user']))
                    id = msg.content.split("/")[4]
                    pixiv_downloader = PixivDownloader()
                    res = await pixiv_downloader.illust_user(user_ids=[id])
                    if res:
                        await utils.send_illusts(target=target, illusts=res)
                        await self.bot.reply(owner, "'quick_pixiv_user' Complete")
                        await self.bot.reply(target, "'quick_pixiv_user' Complete")
                    else:
                        await owner.send(owner, "'pixiv_user' No Result Found")

def setup(bot):
    bot.add_cog(Msg(bot))
