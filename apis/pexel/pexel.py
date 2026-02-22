import requests
import json
import os
from pathlib import Path
from utils.settings import ROOT

# Pexels API:
API_KEY  = os.getenv('PEXELS_API_KEY')
URL = os.getenv('PEXELS_BASE_URL')

# Path to save the videos:
SAVE_DIR = ROOT.joinpath('data/untreated')


class PexelAPI():
    def __init__(self, saveDir:Path = SAVE_DIR):

        self.api      = requests.Session()
        self.api.headers.update({"Authorization": API_KEY})
        self.saveDir  = Path(saveDir)
        self.saveDir.mkdir(exist_ok=True)

    def search(self, query:str, limit:int= 5) -> list:
        '''Searches Pexels API for videos matching the query.'''

        params = {
            "query"       : query,
            "per_page"    : limit,
            "orientation" : "landscape",
            "size"        : "medium"
        }

        try:
            response = self.api.get(URL, params=params)
            response.raise_for_status()

            print(json.dumps(response.json(), indent=4))

            return response.json().get("videos", [])

        except requests.RequestException as e:
            print(f'API Error occurred:\n{e}')
            return []

    def download(self, video:dict) -> str:
        '''Downloads a single video to the save directory. Returns the file path.'''

        print(json.dumps(video, indent=4))

        videoId    = video.get("id")
        videoFiles = video.get("video_files", [])
        if not videoFiles:
            return None

        videoUrl = videoFiles[0].get("link")
        filePath = self.saveDir / f"{videoId}.mp4"

        if filePath.exists():
            print(f'- Already exists: {filePath.name}')
            return str(filePath)

        try:
            print(f'- Downloading: {filePath.name}')
            with self.api.get(videoUrl, stream=True) as r:
                r.raise_for_status()
                with open(filePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            return str(filePath)

        except requests.RequestException as e:
            print(f'Download error:\n{e}')
            return None
