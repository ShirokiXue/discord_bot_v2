import logging
import os
from datetime import datetime

import discord
from discord.ext import commands

from module import *


class ShiroBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="/bot ", intents=intents)

        self.json_loader = JsonLoader("json/bot_config.json")
        self.owner_id = int(self.json_loader.get_owner_id())
        self.debug_guilds = self.json_loader.get(["debug_guilds"])
        self.bot = self

        # create logger
        formatter = logging.Formatter(
            '[%(levelname)s]: %(name)s: %(asctime)s: %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        fh = logging.FileHandler("log/bot.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        for filename in os.listdir("./cog"):
            if filename.endswith('py'):
                self.load_extension(f"cog.{filename[:-3]}")

    # ready funtion
    async def on_ready(self):
        await self.change_presence(activity=discord.Game("開發中"))
        self.logger.info(f"Logged in as {self.user.name} | {self.user.id}")

        test = 0
        if test:
            await self.test()

    async def reply(self, target, text):
        await target.send(f">> {text}")

    async def test(self):
        pass

