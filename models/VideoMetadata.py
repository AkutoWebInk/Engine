from typing import List, Optional
from pydantic import BaseModel, Field

class VideoMetadata(BaseModel):
    id:               str = Field(..., description="Unique identifier, e.g., 'video_0001'")
    filename:         str = Field(..., description="Original filename")
    filepath:         str = Field(..., description="Absolute path to the video file")
    frame_path:       Optional[str] = Field(None, description="Path to the extracted frame image")
    width:            int = Field(0, description="Video width in pixels")
    height:           int = Field(0, description="Video height in pixels")
    duration_seconds: float = Field(0.0, description="Duration of the video in seconds")
    # Gemini analysis info:
    description:      str = Field("", description="Detailed visual description of the video content")
    keywords:         List[str] = Field(default_factory=list, description="List of relevant tags/keywords")
    category:         Optional[str] = Field(None, description="Broad category (e.g., 'Medical', 'Nature')")


class VideoContentAnalysis(BaseModel):
    description:    str = Field(..., description="Detailed visual description of the video content")
    keywords:       List[str] = Field(..., description="List of relevant tags/keywords")
    category:       str = Field(..., description="Broad category (e.g., 'Medical', 'Nature', 'Sports')")