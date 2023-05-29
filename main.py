from fastapi import FastAPI, File
from fastapi.responses import HTMLResponse

from cli_v1 import parse_text_with_chatgpt

from typing import Annotated

import json
import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

WHISPER_PROMPT = "Um, well, I sort of did this at 10:00, and also at 1:00 I worked out."


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/text/{filename}")
async def get_text(filename: str):
    if f"{filename}.txt" not in os.listdir('text'):
        return "File not found"
    return open(f"./text/{filename}.txt", "r").read()


@app.get("/tags/{filename}")
async def get_tags(filename: str):
    if f"{filename}.json" not in os.listdir('tags'):
        return "Tags not found"
    return json.load(open(f"./tags/{filename}.json", "r"))

@app.post("/transcribe/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    print("READING: {}")
    with open("tmp/audio.m4a", "wb") as f:
        f.write(file)

    fp = open("tmp/audio.m4a", "rb")
    print("HITTING WHISPER")
    transcript = openai.Audio.transcribe("whisper-1", fp, prompt=WHISPER_PROMPT)

    tags = parse_text_with_chatgpt(transcript['text'], target=False)
    tags = tags[1:-1]
    print(f"{type(transcript)=} {transcript=} {tags=}")
    return {"file_size": len(file), "message": transcript['text'], 'tags': tags}


@app.get("/upload")
async def main():
    content = """
<body>
<form action="/transcribe/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
