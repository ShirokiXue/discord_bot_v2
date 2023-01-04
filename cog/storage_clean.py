from datetime import datetime

from pathlib import Path
from asyncpg import PostgresConnectionError
from bot import ShiroBot
from discord.ext import commands, tasks
from module import *


class StorageCleanCog(commands.Cog):
    def __init__(self, bot: ShiroBot):
        self.bot = bot
        self.del_mini_images.add_exception_type(PostgresConnectionError)
        self.del_mini_images.start()

    @tasks.loop(hours=1)
    async def del_mini_images(self):
        await self.bot.wait_until_ready()

        hour = datetime.now().strftime("%H")
        if hour == '08':
            path = self.bot.json_loader.get(["download_dir"])
            p = Path(path)
            n = len([file.unlink() for file in list(p.glob(f'{path}/**/*_mini.*'))])
            if n: self.bot.logger.info(f"'del_mini_images' end. deleted {n} files.")

def setup(bot):
    bot.add_cog(StorageCleanCog(bot))
