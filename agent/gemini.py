# Google generative ai libs:
from google import genai
from google.genai.errors import ClientError, ServerError, APIError

# Agent response format:
from models.VideoMetadata import VideoContentAnalysis

# Agent system instructions:
from agent.instructions import INSTRUCTIONS

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
    "response_schema"       : VideoContentAnalysis
}

class GeminiAPI:
    def __init__(self):
        self.api = genai.Client(api_key=API_KEY)
        
    def describe(self, video:str):
        try:
            print(f'Uploading:  {video}')
            
            uri = self.api.files.upload(file=video)
            while uri.state.name == 'PROCESSING':
                print(f'Pooling response:  \n{uri}')
                time.sleep(2)
                
                uri = self.api.files.get(name= uri.name)

            response = self.api.models.generate_content(model=MODEL, contents=[uri], config=CONFIG).text        
            return response
        
        except (ClientError, ServerError, APIError) as e:
            print(f'API Error occurred:\n{e}')
            return None