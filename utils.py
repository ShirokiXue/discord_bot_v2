import asyncio
import functools
import json
import os
import typing

import cv2
import discord
import numpy as np
from tqdm import tqdm

with open('json/bot_config.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
    imgur_config = jdata["imgur"]


async def say_hello(bot):
    target = bot.lab
    msg = "hello"
    if msg and target:
        await target.send(msg)


async def send_illusts(target, illusts: list, reverse=True):

    index = list(range(len(illusts)))
    pbar = tqdm(total=len(illusts))
    if reverse:
        illusts.reverse()
        index.reverse()

    await target.send("=======================")
    for i, illust in zip(index, illusts):
        await target.send(f"#{i+1} {illust.title}")
        for f in illust.file_list:
            img = discord.File(compress_image(f, mb=8))
            try:
                await target.send(file=img)
            except discord.HTTPException as e:
                if e.code == 40005:
                    await target.send(f"<{os.path.split(f)[1]} is too large to send>")
                else:
                    await target.send("<Some problems happened>")
        await target.send(f"Artist: {illust.artist}")
        await target.send("=======================")
        pbar.update(1)
    pbar.close()


def get_size(file):
    # 獲取檔案大小:MB
    size = os.path.getsize(file)
    return size / 1024 / 1024


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def compress_image(imgpath, mb=8):
    if get_size(imgpath) < mb:
        return imgpath
    img = imread(imgpath)
    dir, _ = os.path.splitext(imgpath)
    outfile = f"{dir}_mini.jpg"

    # save the image in JPEG format with 85% quality
    for i in range(20):
        jpg_quality = 100-i*5
        imwrite(outfile, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
        if get_size(outfile) < mb:
            break

    return outfile


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper
