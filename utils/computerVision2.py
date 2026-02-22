import cv2
import os
from utils.baseModels import VideoMetadata

class Extract:

    @staticmethod
    def metadata(path:str)-> VideoMetadata:
        '''Uses computer vision (cv2) librarby to read the video and extract relevant info.'''
        path = str(path)                                    # Stringfy the path just to make sure.
        
        try:

            video   = cv2.VideoCapture(path)                # Loads the video.

            name    = os.path.basename(path)                # Extract the name to extract the id.
            id      = int(name.split('.')[0])               # Extracts the video ID from the name.
            width   = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # Width.
            height  = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Height.
            fps     = video.get(cv2.CAP_PROP_FPS)           # Frames per second.
            frames  = video.get(cv2.CAP_PROP_FRAME_COUNT)   # Total frames in the video.
            duration= frames / fps                          # Duration.
            
            video.release()                                 # Releases the video.

            return VideoMetadata(id=id, width=width, height=height, duration=duration)
        
        except Exception as e:
            print(f'Exception: Extract.metadata()\n{e}')

    @staticmethod
    def keyframes(path:str, quantity=3):
        '''Uses computer vision (cv2) librarby to read the video and extract relevant video frames.'''
        path = str(path)

        try:
            video   = cv2.VideoCapture(path)                # Loads the video.
            frames  = int(video.get(cv2.CAP_PROP_FRAME_COUNT))   
            keyframes = []
            
            for i in range(1, quantity + 1):
                percentage = int(frames * (i/(quantity + 1)))
                video.set(cv2.CAP_PROP_POS_FRAMES, percentage)
                
                ret, frame = video.read()
                if ret:
                    keyframes.append(frame)

            video.release()
            return keyframes

        except Exception as e:
            print(f'Exception: Extract.keyframes()\n{e}')