import os
from collections import defaultdict
from typing import Any

import openai
from flask import Flask, flash, redirect, request
from werkzeug.utils import secure_filename

from .cli_v1 import parse_text_with_chatgpt
from .db.connect import DBConnection

openai.api_key = os.environ["OPENAI_API_KEY"]
db = DBConnection()

WHISPER_PROMPT = "Um, well, I sort of did this at 10:00, and also at 1:00 I worked out."
UPLOAD_FOLDER = "./data/audio/remote"
ALLOWED_EXTENSIONS = {"m4a", "mp3", "wav"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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
        try:
            transcript = openai.Audio.transcribe("whisper-1", newfile, prompt=WHISPER_PROMPT)
        except openai.error.InvalidRequestError as e:
            print(f"Error: {e}")
            return {"message": "Error: " + str(e)}

        out_text = str(transcript["text"])
        tags = parse_text_with_chatgpt(out_text, target=False)
        tags = tags[1:-1]  # TODO(zam): fix me
        print(f"{type(transcript)=} {transcript=} {tags=}")

    # TODO(gst): upload to S3
    # for now, delete the files after we're done with them
    os.remove(filepath)

    db.put_user_transcription(user_id=1, transcription=out_text, version=1)

    tag_date_list = db.get_user_tags_from_tags(user_id=1, tags=tags)

    # get date string from tag occurences
    dates = defaultdict(list)
    for tag in tag_date_list:
        dates[tag[0]] += [tag[1]]

    tag_date_str = ";".join([",".join(dates[x]) for x in dates])

    return {"message": out_text, "tags": tags, "tag_dates": tag_date_str}


@app.route("/user/<user_id>", methods=["GET"])
async def user_info(user_id: int) -> Any:
    """Get user info."""
    info = db.get_user(user_id)
    transcriptions = db.get_user_transcriptions(user_id)

    return {"user_info": info, "transcriptions": transcriptions}


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


# flask --app main.py --debug run
