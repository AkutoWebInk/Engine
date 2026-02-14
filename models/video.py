from typing import List, Optional
from pydantic import BaseModel, Field

class VideoMetadata(BaseModel):
    id              : int = Field(..., description="Unique identifier, e.g., '001'")
    width           : int = Field(0, description="Video width in pixels")
    height          : int = Field(0, description="Video height in pixels")
    duration        : float = Field(0.0, description="Duration of the video in seconds")
    
class VideoAnalysis(BaseModel):
    description     : str = Field(..., description="Detailed visual description of the video content")
    keywords        : List[str] = Field(..., description="List of relevant tags/keywords")
    category        : str = Field(..., description="Broad category (e.g., 'Medical', 'Nature', 'Sports')")

class Video(BaseModel):
    model_config    = {"validate_assignment":True}
    id              : int = Field(..., description="Unique identifier, e.g., '001'")
    width           : int = Field(0, description="Video width in pixels")
    height          : int = Field(0, description="Video height in pixels")
    duration        : float = Field(0.0, description="Duration of the video in seconds")
    description     : str = Field(..., description="Detailed visual description of the video content")
    keywords        : List[str] = Field(..., description="List of relevant tags/keywords")
    category        : str = Field(..., description="Broad category (e.g., 'Medical', 'Nature', 'Sports')")
    text_embedding  : List[float] = Field(..., description="Values for text embeddings.")
    visual_embedding: List[float] = Field(..., description="Values for image embeddings.")