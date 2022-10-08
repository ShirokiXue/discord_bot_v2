# python 3.10.4

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

install("pip")
install("wheel")

install("py-cord")
install("opencv-python")
install("cloudscraper")
install("pixivpy")
install("tqdm")
install("imgurpython")
install("beautifulsoup4")
install("asyncpg")

install("google-api-python-client")
install("google_auth_oauthlib")
install("oauth2client")
install("apiclient")

install("saucenao_api")
install("favicon")
