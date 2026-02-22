# .env:
from dotenv import load_dotenv
load_dotenv()

# APIs:
from apis.pexel.pexel import PexelAPI
from apis.google.gemini import GeminiAPI
from apis.google.instructions import GEMINI_INSTRUCTIONS
# Models:
from utils.baseModels import VideoAnalysis, Video
# Utils:
from utils.computerVision2 import Extract
from utils.clipTorch import Embed
from utils.settings import ROOT
# Misc:
import json

# Agents:
PEXEL             = PexelAPI()
AGENTE_DESCRICAO  = GeminiAPI(instructions=GEMINI_INSTRUCTIONS, responseType=VideoAnalysis)

# Paths:
VIDEOS_DIR = ROOT / 'data'
JSONS_DIR  = ROOT / 'data' / 'jsons'
JSONS_DIR.mkdir(parents=True, exist_ok=True)


def process(path: str) -> Video | None:
    '''Takes a video path, runs the full pipeline, saves a JSON and returns the Video object.'''

    print(f'\n[1/4] Extracting metadata and keyframes...')
    metadata  = Extract.metadata(path)
    keyframes = Extract.keyframes(path)

    print(f'[2/4] Analyzing video with Gemini...')
    analysis = AGENTE_DESCRICAO.analyze(path)

    if analysis is None:
        raise Exception('Gemini returned no response. API key may be exhausted.')

    if not analysis.suitable:
        print(f'[--] Video {metadata.id} marked as unsuitable. Skipping.')
        return None

    print(f'[3/4] Generating embeddings...')
    textEmbedding   = Embed.text(analysis.description)
    visualEmbedding = Embed.video(keyframes)

    video = Video(
        id               = metadata.id,
        width            = metadata.width,
        height           = metadata.height,
        duration         = metadata.duration,
        suitable         = analysis.suitable,
        description      = analysis.description,
        keywords         = analysis.keywords,
        category         = analysis.category,
        text_embedding   = textEmbedding,
        visual_embedding = visualEmbedding
    )

    print(f'[4/4] Saving JSON...')
    output = JSONS_DIR / f'{video.id}.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(video.model_dump(), f, indent=4, ensure_ascii=False)

    print(f'[OK] Saved: {output.name}')
    return video


if __name__ == '__main__':

    videos    = sorted(VIDEOS_DIR.glob('*.mp4'), key=lambda f: int(f.stem))
    existing  = {f.stem for f in JSONS_DIR.glob('*.json')}
    pending   = [v for v in videos if v.stem not in existing]

    print(f'Total: {len(videos)} | Already processed: {len(existing)} | Pending: {len(pending)}')

    for i, path in enumerate(pending, 1):
        print(f'\n{"="*50}')
        print(f'[{i}/{len(pending)}] Processing: {path.name}')

        try:
            process(str(path))
        except Exception as e:
            print(f'[STOP] {path.name}: {e}')
            break
