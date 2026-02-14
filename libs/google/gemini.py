# Google generative ai libs:
from google import genai
from google.genai.errors import ClientError, ServerError, APIError

# Agent response format:
from models.video import VideoAnalysis

from libs.google.instructions import INSTRUCTIONS

# Misc:
import os
import time



API_KEY = os.getenv("GENAI_API_KEY")
MODEL   = 'gemini-2.0-flash'
CONFIG  = {
    "temperature"           : 0.0,
    "top_p"                 : 0,
    "top_k"                 : 1,
    "candidate_count"       : 1,
    "system_instruction"    : INSTRUCTIONS, 
    "response_mime_type"    : "application/json",
    "response_schema"       : VideoAnalysis
}

class GeminiAPI:
    def __init__(self):
        self.api = genai.Client(api_key=API_KEY)
        
    def analyze(self, video:str) -> VideoAnalysis:
        '''Calls Gemini API and analyzes a video, following system instructions and response schema.'''
        
        try:
            # Upload the video and get the URI:
            print('- Uploading video file.')
            uri = self.api.files.upload(file=video)
            
            # Pool for the URI:
            while uri.state.name == 'PROCESSING':
                print('- Pooling for URI...')
                time.sleep(1)
                uri = self.api.files.get(name= uri.name)

            # Send the URI to the Gemini model:
            response = self.api.models.generate_content(model=MODEL, contents=[uri], config=CONFIG).parsed
            print('- Parsing response...')
  
            return response
        
        except (ClientError, ServerError, APIError) as e:
            print(f'API Error occurred:\n{e}')
            return None