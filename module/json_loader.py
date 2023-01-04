import json

class JsonLoader():
    def __init__(self, jfile:str) -> None:

        with open(jfile, encoding='utf-8') as f:
            self.jdata = json.load(f)
    
    def get_token(self):
        return self.jdata["token"]
    
    def get_owner_id(self):
        return self.jdata["owner_id"]
    
    def get_download_path(self):
        return self.jdata["download_path"]

    def get(self, keys:list):
        res=self.jdata
        for key in keys: res=res[key]
        return res