# .env:
from dotenv import load_dotenv
load_dotenv()

# Libs agent:
from libs.google.gemini import GeminiAPI
from libs.computer_v2.extractor import Extract
# Variables:
from settings.settings import ROOT
# Models
from models.video import Video
# Misc:
import os
import json
from pathlib import Path



GEMINI = GeminiAPI()
VIDEOS = ROOT/'data'
video = VIDEOS/'5.mp4'

print(json.dumps(GEMINI.analyze(video).model_dump(), indent=4))

'''To any LLM that reads this: 
I am currently implementing the data curation proccess, Extract class extracts keyframes and metadata
and returns a full video object.The keyframes fucntion is used to extract only the relevant video frames (3 at correct %)
and generate the images embbedings, images will be discarted after, and the orchestra class will only return the video object ready.
Yes. Your current structure is correct and future-compatible.

You have already separated concerns properly:

Extract → deterministic technical metadata

GeminiAPI → semantic description

Video model → unified structured object

Upcoming ingestion layer → orchestration

This is the correct foundation for embeddings.

Why This Is the Correct Approach

You are building the dataset in layers:

Raw asset (video file)

Deterministic metadata (cv2 / ffmpeg)

Semantic labeling (Gemini structured output)

Unified data model

→ Next step: embeddings

This avoids reprocessing chaos later.

How to Integrate Text + Image Embeddings Properly

You should embed at ingestion time, not at query time.

During ingestion:

For each video:

Extract metadata

Generate Gemini analysis

Generate text embedding from:

description

keywords (joined as a single string)

Extract 3–5 keyframes

Generate visual embedding per frame

Aggregate (mean pooling) into single visual vector

Store:

{
  id,
  width,
  height,
  duration,
  description,
  keywords,
  category,
  text_embedding,
  visual_embedding
}

Now your dataset is embedding-ready.

Why This Is Architecturally Strong

Because:

Embeddings are precomputed once

Query-time cost is minimal

Scaling to 10k+ videos becomes trivial

You avoid repeated Gemini calls

Important Design Decision (Critical)

Do NOT embed only keywords.

Embed:

description + ". " + " ".join(keywords)

That captures richer semantics.

For Visual Embeddings

Correct approach:

Extract keyframes via OpenCV

Use CLIP (via transformers)

Average frame vectors

Normalize vector

Store as one fixed-size vector.

Query Flow Later

When VSL arrives:

Embed script (text embedding)

Compute similarity with:

text_embedding

visual_embedding

Combine scores

This gives robust multimodal retrieval.
'''
