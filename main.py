import os

import openai
from flask import Flask, flash, redirect, request
from werkzeug.utils import secure_filename

from cli_v1 import parse_text_with_chatgpt

openai.api_key = os.environ["OPENAI_API_KEY"]

WHISPER_PROMPT = "Um, well, I sort of did this at 10:00, and also at 1:00 I worked out."
UPLOAD_FOLDER = "./audio/tmp"
ALLOWED_EXTENSIONS = {"m4a", "mp3", "wav"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/transcribe/", methods=["POST"])
def upload_file():
    if request.method == "POST":
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

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        fp = open(filepath, "rb")
        transcript = openai.Audio.transcribe("whisper-1", fp, prompt=WHISPER_PROMPT)
        tags = parse_text_with_chatgpt(transcript["text"], target=False)
        tags = tags[1:-1]
        print(f"{type(transcript)=} {transcript=} {tags=}")

        # for now, delete the files after we're done with them
        os.remove(filepath)

        return {"message": transcript["text"], "tags": tags}


@app.route("/", methods=["GET"])
async def main():
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
