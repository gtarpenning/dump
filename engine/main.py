import os
from typing import Any

import openai
from flask import Flask, flash, redirect, request
from werkzeug.utils import secure_filename

from .cli_v1 import parse_text_with_chatgpt

openai.api_key = os.environ["OPENAI_API_KEY"]

WHISPER_PROMPT = "Um, well, I sort of did this at 10:00, and also at 1:00 I worked out."
UPLOAD_FOLDER = "./data/audio/remote"
ALLOWED_EXTENSIONS = {"m4a", "mp3", "wav"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/transcribe/", methods=["POST"])
def upload_file() -> Any:
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    filename = secure_filename(file.filename)  # type: ignore
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    out_text, tags = "", ""
    with open(filepath, "rb") as newfile:
        transcript = openai.Audio.transcribe("whisper-1", newfile, prompt=WHISPER_PROMPT)
        out_text = str(transcript["text"])
        tags = parse_text_with_chatgpt(out_text, target=False)
        tags = tags[1:-1]  # TODO(zam): fix me
        print(f"{type(transcript)=} {transcript=} {tags=}")

    # TODO(gst): upload to S3
    # for now, delete the files after we're done with them
    os.remove(filepath)

    return {"message": out_text, "tags": tags}


@app.route("/", methods=["GET"])  # type: ignore
async def main() -> str:
    content = """
<!doctype html>
<body>
<form action="/transcribe/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return content
