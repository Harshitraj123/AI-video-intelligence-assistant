from dotenv import load_dotenv

load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all


source = "https://www.youtube.com/watch?v=T-D1OfcDW1M"
language = "english"


chunks = process_input(source)

transcript = transcribe_all(
    chunks,
    language=language
)

print("\n" + "=" * 60)
print("📝 TRANSCRIPT")
print("=" * 60)

if len(transcript) > 500:
    print(transcript[:500] + "...")
else:
    print(transcript)