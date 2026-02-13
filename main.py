# .env:
from dotenv import load_dotenv
load_dotenv()

# Gemini agent:
from agent.gemini import GeminiAPI

# Globals:
from settings.settings import ROOT

# Misc:
import os
from pathlib import Path


GEMINI = GeminiAPI()

VIDEOS = ROOT.parent/'Curadoria'/'data'
video = VIDEOS/'201.mp4'

description = GEMINI.describe(video)
print(description)