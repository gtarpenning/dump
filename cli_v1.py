import argparse
import json
import os
import re
from argparse import Namespace
from typing import Optional

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

WHISPER_PROMPT = "Um, well, I sort of did this at 10:00, and also at 1:00 I worked out."


def transcribe(filename: str, use_cache: bool = True, verbose: bool = False) -> str:
    """Transcribe an audio file to text."""
    # check if cached
    if use_cache:
        if f"{filename}.txt" in os.listdir("text"):
            cache_path = f"text/{filename}.txt"
            if verbose:
                print(f"Returning from cached file: {cache_path}")
            return open(cache_path, "r").read()

    # transcribe with whisper
    print(f"Hitting WHISPER API, transcribing: {filename}")  # always print this
    audio_file = open(f"audio/{filename}.m4a", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=WHISPER_PROMPT)
    text: str = str(transcript["text"])

    # cache
    with open(f"text/{filename}.txt", "w") as f:
        f.write(text)

    return text


def parse_text_with_chatgpt(
    paragraph: str,
    filename: Optional[str] = None,
    use_cache: bool = True,
    verbose: bool = False,
    target: bool = False,
) -> str:
    if use_cache and filename is not None:
        if f"{filename}.json" in os.listdir("tags"):
            if verbose:
                print("Using cached tags...")
            try:
                tags = json.load(open(f"tags/{filename}.json", "r"))
                if isinstance(tags, list):
                    return ",".join(tags)
                else:
                    return str(tags)
            except Exception as e:
                print(f"Error: {e}.  Generating new tags...")

    if target is False:
        example = "Today was a tiring day. I ate a lot of bad greasy food. I'm currently tired because I had a long day at work. I also went to the gym briefly"
        preamble = f"You are an Extractor. As an Extractor you extract user content like the following:\n{example}\n"
        example2 = """{"unhealthy food", "work", "exercise"}"""
        prompt = f"{preamble}And as an Extractor you return a JSON of relevant succinct tags like this example:\n{example2}\nReturn only the json"
    else:
        example = (
            "I am medium energy, I have had a 9 productive day, I am a low happiness"
        )
        preamble = f"You are an extractor. As an extractor you extract user content in this format:\n{example}\n"
        example2 = "{energy : 5, productivity : 9, happiness : 2}"
        prompt = f"{preamble} And as an extractor you return a score bounded between 1-10 that captures the user's sentiment for each category in the following json format: {example2}\n Only return the json value."

    print("Hitting CHAT API...")  # always print this
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": paragraph},
        ],
        temperature=0,
    )
    content = response["choices"][0]["message"]["content"]
    print(f"{content=}")
    # regex to extract between two curly braces
    tag_list = re.findall(r"\{.*?\}", content)
    tag_str = ""
    if len(tag_list) > 0:
        tag_str = ",".join([x.replace('"', "").strip() for x in tag_list[0].split(",")])
    else:
        print("No tags found. Returning empty.")
        tag_str = "{}"

    print(f"{tag_str=}")

    return tag_str


def parse() -> Namespace:
    parser = argparse.ArgumentParser(description="Transcribe audio files to text.")
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        help="path to audio file",
        default="audio/test-msg.m4a",
    )
    parser.add_argument(
        "--whisp",
        "-w",
        help="overrite whisper transcription",
        action="store_false",
        default=True,
    )
    parser.add_argument(
        "--tag",
        "-t",
        help="overrite chatgpt tagging",
        action="store_false",
        default=True,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="increase output verbosity",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--target",
        "-tg",
        help="audio transcript is a target",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--all", "-a", help="all files in audio dir", action="store_true", default=False
    )
    args = parser.parse_args()
    return args


def main() -> None:
    # TODO(zam): Add --all functionality --> accept iterable input.
    args = parse()
    name = args.path.split("/")[1].split(".")[0]

    transcription = transcribe(name, use_cache=args.whisp, verbose=args.verbose)
    if args.verbose:
        print(f"Transcription:\n{transcription}")

    tags = parse_text_with_chatgpt(
        transcription,
        name,
        use_cache=args.tag,
        verbose=args.verbose,
        target=args.target,
    )
    print(f"Tags:\n{tags}")


if __name__ == "__main__":
    main()
