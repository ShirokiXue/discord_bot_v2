
import asyncio
from datetime import datetime

import discord
from asyncpg import PostgresConnectionError
from bot import ShiroBot
from discord.ext import commands, tasks
from module import *


class RemindCog(commands.Cog):
    def __init__(self, bot: ShiroBot):
        self.bot = bot
        self.json_loader = bot.json_loader
        self.routine.add_exception_type(PostgresConnectionError)
        self.routine.start()
        self.main.add_exception_type(PostgresConnectionError)
        self.main.start()

    @tasks.loop(minutes=1)
    async def routine(self):
        await self.bot.wait_until_ready()

        hour = int(datetime.now().strftime("%H"))
        if hour == 13:
            target = self.bot.get_channel(self.json_loader.get(["text_channel_id", "task_routine"]))
            embed = discord.Embed(title="Routine", url="https://cog-creators.github.io/discord-embed-sandbox/", description="Sent daily at 1pm", color=0xc832ff)
            embed.set_author(name="bot.task.remind", url="https://cog-creators.github.io/discord-embed-sandbox/")
            embed.set_thumbnail(url="https://i.imgur.com/7ZiHjeB.png")

            task_manager = GoogleTaskManager()
            for task_list in task_manager.get_task_lists():
                if task_list['title'] == 'Routine':
                    embed = self.add_task(task_manager, embed, task_list)

            await target.send(embed=embed)
            self.bot.logger.info("'Routine' remind")
            await asyncio.sleep(3600)

    @tasks.loop(minutes=1)
    async def main(self):
        await self.bot.wait_until_ready()

        hour = int(datetime.now().strftime("%H"))
        if hour == 13:
            target = self.bot.get_channel(self.json_loader.get(["text_channel_id", "task_main"]))
            embed = discord.Embed(title="Main", url="https://cog-creators.github.io/discord-embed-sandbox/", description="Sent daily at 1pm", color=0xc832ff)
            embed.set_author(name="bot.task.remind", url="https://cog-creators.github.io/discord-embed-sandbox/")
            embed.set_thumbnail(url="https://i.imgur.com/0YxzU41.png")

            task_manager = GoogleTaskManager()
            for task_list in task_manager.get_task_lists():
                if task_list['title'] == 'Main':
                    embed = self.add_task(task_manager, embed, task_list)
                    
            await target.send(embed=embed)
            self.bot.logger.info("'Main' remind")
            await asyncio.sleep(3600)

    def add_task(self, task_manager:GoogleTaskManager, embed:discord.Embed, task_list):
        tasks = task_manager.get_tasks_from_list(task_list['id'])
        tasks = sorted(tasks, key=lambda s: int(s['position']))
        is_parent_list = [task['parent'] if 'parent' in task else None for task in tasks]
        for task in tasks:
            if 'parent' in task:
                parent = task_manager.get_task_with_id(task_list['id'], task['parent'])
                title = f"{parent['title']} - {task['title']}"
                notes = task['notes'] if 'notes' in task else '-'
                embed.add_field(name=title, value=notes, inline=False)
            elif task['id'] not in is_parent_list:
                title = f"{task['title']}"
                notes = task['notes'] if 'notes' in task else '-'
                embed.add_field(name=title, value=notes, inline=False)
            else:
                pass
        embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %a\t%H:%M:%S"))
        return embed


def setup(bot):
    bot.add_cog(RemindCog(bot))
