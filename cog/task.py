
from datetime import datetime

import utils
import os
from asyncpg import PostgresConnectionError
from bot import ShiroBot
from discord.ext import commands, tasks
from module import *


class TaskCog(commands.Cog):
    def __init__(self, bot: ShiroBot):
        self.bot = bot
        self.pixiv_follow_task.add_exception_type(PostgresConnectionError)
        self.pixiv_follow_task.start()

    @tasks.loop(hours=1)
    async def pixiv_follow_task(self):
        await self.bot.wait_until_ready()

        hour = datetime.now().strftime("%H")
        if hour == '10':
            self.bot.logger.info("'pixiv_follow_task' start")
            pixiv_downloader = PixivDownloader()
            target = self.bot.get_channel(self.bot.json_loader.get(
                ['text_channel_id', 'pixiv_follow']))
            res = await pixiv_downloader.illust_follow(
                limit=50,
                use_tag=True,
                output=False
            )
            dupli_list = find_duplicate(res, task="pixiv_follow")
            new_res = [illust for i, illust in enumerate(res) if i not in dupli_list]

            await utils.send_illusts(target=target, illusts=new_res)
            await self.bot.reply(target, "'pixiv_follow_task' Complete")
            self.bot.logger.info("'pixiv_follow_task' end")

def find_duplicate(res, task)->list:
    with open("json/history.json","r", encoding='utf8') as jfile:
        jdata = json.load(jfile)
        history = jdata[task]

    dupli_list = []
    for i, illust in enumerate(res):
        file = os.path.split(illust.file_list[0])[1]
        if  file not in history:
            history.insert(0,file)
        else:
            dupli_list.append(i)
    jdata[task] = history[:100]
    with open("json/history.json","w", encoding='utf8') as jfile:
        json.dump(jdata, jfile, indent=4)

    return dupli_list

def setup(bot):
    bot.add_cog(TaskCog(bot))
