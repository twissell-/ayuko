import asyncio
import json

import config
import downloader
import openai
import subscription
from deepgram import Deepgram

DEEPGRAM_API_KEY = "cd882613bd0cc2c6b6de5d0ea79bed0762055b8e"
PATH_TO_FILE = "tmp/Extra History/20230916 - Henry Ford： The Boy Who Hated Horses - #1 - Extra History [tQAFS1d-0hY].mp3"


async def main():
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, "rb") as audio:
        # ...or replace mimetype as appropriate
        # source = {"buffer": audio, "mimetype": "audio/wav"}
        # response = await deepgram.transcription.prerecorded(
        #     source, {"punctuate": True, "diarize": True, "paragraphs": True}
        # )

        # transcript = response["results"]
        with open("response.json") as f:
            response = json.load(f)
        transcript = response["results"]["channels"][0]["alternatives"][0][
            "paragraphs"
        ]["transcript"]
        with open("transcript.md", "w") as f:
            f.write(transcript)
        # print(json.dumps(transcript, indent=2))


asyncio.run(main())

exit(0)


def _download_transcript(subscription: Subscription):
    for link in subscription.links:
        video_id = link.split("?")[1].replace("v=", "")
        transcript = [v["text"] for v in YouTubeTranscriptApi.get_transcript(video_id)]
        transcript = " ".join(transcript).replace("/n", " ")

        return transcript
        break


openai.api_key = "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"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
)
print(completion.choices[0].message.content)

exit

for sub_config in config.get("subscriptions"):
    sub = subscription.from_config(**sub_config)
    # downloader.download(sub)
    trsc = downloader._download_transcript(sub)
