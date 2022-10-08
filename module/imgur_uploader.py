from imgurpython import ImgurClient
from datetime import datetime

class ImgurUploader():
    def __init__(self, client_id, client_secret, access_token, refresh_token, album_id) -> None:

        self.client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        self.album_id = album_id

    def upload(self, local_img, name="", title="")->dict:
        config = {
            'album': self.album_id,
            'name':  name,
            'title': title,
            'description': f'test-{datetime.now()}'
        }
        image = self.client.upload_from_path(local_img, config=config, anon=False)

        return image