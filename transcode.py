import os
import time
from pathlib import Path

import click
import ffmpeg

candidates = []


def enqueue(candidate: str):
    if candidate not in candidates:
        candidate_path = Path(candidate)
        transcoded_dir = f"{candidate_path.parent.parent.absolute()}/processed"
        transcoded_path = (
            f"{transcoded_dir}/{candidate_path.name.replace('.mp4', '_x265.mp4')}"
        )
        if not Path(transcoded_path).exists():
            candidates.append(candidate)


def find_transcoding_candidates(search_root: str):
    stream_paths = [f.path for f in os.scandir(search_root) if f.is_dir()]
    for path in stream_paths:
        completed_path = f"{path}/completed"
        if os.path.exists(completed_path):
            _, _, filenames = next(os.walk(completed_path))
            full_paths = [
                f"{completed_path}/{x}" for x in filenames if x.endswith(".mp4")
            ]
            for candidate in full_paths:
                enqueue(candidate)


def transcode(candidate: str):
    candidate_path = Path(candidate)
    transcoded_dir = f"{candidate_path.parent.parent.absolute()}/processed"
    if not os.path.exists(transcoded_dir):
        os.makedirs(transcoded_dir)
    transcoded_path = (
        f"{transcoded_dir}/{candidate_path.name.replace('.mp4', '_x265.mp4')}"
    )
    print(
        f"Transcoding from source: {candidate_path} to destination: {transcoded_path}"
    )
    try:
        (
            ffmpeg.input(candidate_path)
            .filter("fps", fps=30)
            .output(transcoded_path, vcodec="libx265", crf="28", preset="fast")
            .run()
        )
    except Exception as e:
        print("Encountered an exception while transcoding:")
        print(e)
    os.remove(candidate_path)


@click.command()
@click.option(
    "--path", default="/mnt/secundus/Media/Streams", help="Transcoding file output path"
)
def run(path: str):
    while True:
        print(f"Looking for transcoding candidates...")
        find_transcoding_candidates(path)
        if len(candidates) > 0:
            print(f"Found {len(candidates)} candidates for transcoding.")
            for candidate in candidates:
                print(f"Starting transcoding of candidate: {candidate}.")
                candidates.remove(candidate)
                transcode(candidate)
            print(f"Finished transcoding {len(candidates)} candidates.")
        else:
            print(f"Didn't find any transcoding candidates...")
        time.sleep(30)


if __name__ == "__main__":
    run()
