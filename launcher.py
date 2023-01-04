import logging

from bot import ShiroBot

logging.basicConfig(
    # stream=sys.stdout,
    filename='log/discord.log', encoding='utf-8',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.WARNING, filemode='a',
    format='[%(levelname)s]: %(name)s: %(asctime)s: %(message)s'
    )

if __name__ == "__main__":
    bot = ShiroBot()
    bot.run(bot.json_loader.get_token())