import logging
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
    logging.info(
        f"Transcoding from source: {candidate_path} to destination: {transcoded_path}"
    )
    mixed_in = ffmpeg.input(candidate_path)
    video = mixed_in.video.filter("fps", fps=30)
    audio = mixed_in.audio
    try:
        (
            ffmpeg.output(
                video, audio, transcoded_path, vcodec="libx265", crf="28", preset="fast"
            ).run()
        )
    except Exception as e:
        logging.error("Encountered an exception while transcoding:")
        logging.exception(e)
    os.remove(candidate_path)


@click.command()
@click.option(
    "--path", default="/mnt/secundus/Media/Streams", help="Transcoding file output path"
)
def run(path: str):
    while True:
        logging.info(f"Looking for transcoding candidates...")
        find_transcoding_candidates(path)
        if len(candidates) > 0:
            num_candidates = len(candidates)
            logging.info(f"Found {num_candidates} candidates for transcoding.")
            for candidate in candidates:
                logging.info(f"Starting transcoding of candidate: {candidate}.")
                candidates.remove(candidate)
                transcode(candidate)
            logging.info(f"Finished transcoding {num_candidates} candidates.")
        else:
            logging.info(f"Didn't find any transcoding candidates...")
        time.sleep(30)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run()
