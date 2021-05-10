import os
import click
import time
from streamlink import Streamlink, NoPluginError, PluginError, StreamError
from datetime import datetime

streamlink = Streamlink()

@click.command()
@click.option("--channel", default="roshtein", help="Twitch channel to capture from.")
@click.option(
    "--path", default="/mnt/secundus/Media/Streams", help="Recording file output path"
)
@click.option("--quality", default="best", help="Twitch stream quality")
def start_capturing(channel: str, path: str, quality: str):
    while True:
        try:
            # Set up parameters
            now = datetime.now()
            stream_url = f"https://api.twitch.tv/{channel}"
            out_dir = f"{path}/{channel}/in_progress"
            completed_dir = f"{path}/{channel}/completed"
            filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            if not os.path.exists(completed_dir):
                os.makedirs(completed_dir)
            
            out_path = f"{out_dir}/{filename}"
            completed_path = f"{completed_dir}/{filename}"

            # Initialize Stream Recording
            streams = streamlink.streams(stream_url)
            best_stream = streams[quality]
            fd = best_stream.open()
            out = open(out_path, "ab")

            print(f"Recording from {stream_url} at {quality} quality to {out_path}")

            # Read from stream buffer and write to file
            while True:
                data = fd.read(1024)
                if data is None or data == -1 or data == 0:
                    break
                else:
                    out.write(data)
            fd.flush()
            fd.close()
            out.flush()
            out.close()
            print("Stream ended, cleaning up...")
            os.rename(out_path, completed_path)
            print(f"Moved finished stream file to {completed_path}")

        except NoPluginError as e:
            print("Failed to find plugin: ")
            print(e)
        except PluginError as e:
            print("Got a plugin error:")
            print(e)
        except StreamError as e:
            print("Got a stream error:")
            print(e)
        except Exception as e:
            print("Got some other exception (likely streamer is offline):")
            print(e)
        time.sleep(60)


if __name__ == "__main__":
    start_capturing()
