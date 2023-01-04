import typing
from discord.ext import commands


class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 傳送訊息到指定ID的使用者或聊天室
    @commands.command()
    async def sendto(self, ctx, id:typing.Optional[int] , *, msg:str):
        if ctx.message.author.id==self.bot.owner_id:
            target = self.bot.get_channel(id)
            if not target: target = await self.bot.fetch_user(id)
            msg = await target.send(msg)
            if msg and target:
                await ctx.send(f"<@!{target.id}> << {msg.content}")
    
def setup(bot):
    bot.add_cog(UtilsCog(bot))
