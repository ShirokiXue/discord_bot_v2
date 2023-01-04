# https://github.com/upbit/pixivpy
import json
import os
import sys
from collections import namedtuple

sys.path.append(os.path.abspath(os.path.join(
    os.path.split(os.path.abspath(__file__))[0], "..")))
import pixivpy3
from pixivpy3 import *
from utils import to_thread




Illust = namedtuple('Illust', 'title, artist, file_list')
RANKING_MODES = ["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie",
                 "day_r18", "day_male_r18", "day_female_r18", "week_r18", "week_r18g"]


class PixivDownloader():
    def __init__(self, jfile="json/bot_config.json") -> None:

        with open(jfile, 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
            self.download_dir = jdata["download_dir"] + "pixiv/"
            self.token = jdata["pixiv"]["token"]
            self.favorite_user_id_list = jdata["pixiv"]["favorite_user_id_list"]
            self.tag_list = jdata["pixiv"]["tag_list"]

        self.api = AppPixivAPI()
        self.api.auth(refresh_token=self.token)

    def mkdir(self, download_path):
        try:
            os.makedirs(download_path)
        except FileExistsError:
            pass

    async def illust_follow(self, limit=5, use_tag=True, output=True):
        limit = limit % 100

        download_path = os.path.join(self.download_dir, "illust_follow")
        # download_path = f"{self.download_dir}" + "illust_follow/"
        self.mkdir(download_path)

        res = []
        next_qs = {"restrict": "public"}
        for _ in range(99):
            json_result = self.api.illust_follow(**next_qs)
            res_per_page, next_qs = await self.download_one_page(
                json_result,
                download_path,
                use_tag=use_tag,
                output=output
            )
            res.extend(res_per_page)

            if not (next_qs and len(res) < limit):
                break

        return res[:limit]

    async def illust_user(self, user_ids: list, limit=5, use_tag=False, output=True):

        all_res = []

        # User loop
        for user_id in user_ids.split() if user_ids is str else user_ids:

            user = self.api.user_detail(int(user_id))
            if user.error:
                continue
            download_path = os.path.join(self.download_dir, "illust_user", user.user.name)

            self.mkdir(download_path)

            res = []
            next_qs = {"user_id": user_id}
            for _ in range(99):
                json_result = self.api.user_illusts(**next_qs)
                res_per_page, next_qs = await self.download_one_page(
                    json_result,
                    download_path,
                    use_tag=use_tag,
                    output=output
                )
                res.extend(res_per_page)
                if not next_qs:
                    break

            all_res.extend(res[:limit])

        return all_res

    # ranking_mode = ["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie",
    #             "day_r18", "day_male_r18", "day_female_r18", "week_r18", "week_r18g"]
    async def illust_ranking(self, limit=5, use_tag=True, mode="day", output=True):
        limit = limit % 100

        download_path = os.path.join(self.download_dir, "illust_ranking", mode)
        self.mkdir(download_path)

        res = []
        next_qs = {"mode": mode}
        for _ in range(99):
            json_result = self.api.illust_ranking(**next_qs)
            res_per_page, next_qs = await self.download_one_page(
                json_result,
                download_path,
                use_tag=use_tag,
                output=output
            )
            res.extend(res_per_page)

            if not (next_qs and len(res) < limit):
                break

        return res[:limit]

    @to_thread
    def download_one_page(self, json_result, download_path, use_tag=True, output=False):

        if "R-18" in self.tag_list:
            self.mkdir(os.path.join(download_path, 'r18'))
        res = []

        for illust in json_result.illusts:

            prefix = f"u{illust.user['id']}_a"

            if not use_tag or any(any([required_tag == tag.name for tag in illust.tags]) for required_tag in self.tag_list):
                if illust.meta_single_page.original_image_url:
                    url = illust.meta_single_page.original_image_url
                    path = download_path if "R-18" not in [tag['name'] for tag in illust.tags] \
                                            else os.path.join(download_path, 'r18')
                    self.download(url, path=path, prefix=prefix)
                    if output:
                        print("[%s] %s" % (illust.title, url))

                    file = os.path.join(path, prefix+os.path.basename(url))
                    file_list = [file]
                    res.append(
                        Illust(illust.title, illust.user.name, file_list))

                elif illust.meta_pages:

                    file_list = []

                    for p in illust.meta_pages:
                        url = p.image_urls.original
                        path = download_path if "R-18" not in [tag['name'] for tag in illust.tags] \
                                            else os.path.join(download_path, 'r18')
                        self.download(url, path=path, prefix=prefix)
                        file = os.path.join(path, prefix+os.path.basename(url))
                        file_list.append(file)
                        # time.sleep(1)
                    if output:
                        print("[%s] %s" % (illust.title,
                                           illust.meta_pages[0].image_urls.original))
                    res.append(
                        Illust(illust.title, illust.user.name, file_list))
                else:
                    pass
            # time.sleep(1)

        next_qs = self.api.parse_qs(json_result.next_url)

        return res, next_qs

    def download(self, url, path, prefix='', retry:int=5):
        try:
            self.api.download(url, path=path, prefix=prefix)
        except pixivpy3.utils.PixivError:
            if retry>0:
                self.api.download(url, path=path, retry=retry-1)
            else:
                pass

if __name__ == "__main__":
    import asyncio
    p = PixivDownloader(jfile="json/bot_config.json")
    task = p.illust_user(user_ids=["3689679"])
    asyncio.run(task)
