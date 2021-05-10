# Twitch Recorder

This repo is a dump for some tooling to record and transcode twitch streams for archiving. 

Since Twitch implemented a new separate audio stream (soundtrack) for audio that may contain copyrighted content, VOD recordings on Twitch.tv no longer give the full audio stream from the livestream, just the non-soundtrack stream which makes streams that heavily utilize music less fun to watch in VOD form.

I watch a handful of slots streamers and they like to DJ while playing slots, but some of them stream from Malta in timezones that don't make it easy to catch them live from California, so this tooling was to give me an archive and backlog of slots content to throw on a screen while doing other things.

To save on storage, I processed the streams with `ffmpeg`, dropping the 60fps streams to 30fps and transcoding to `x265` to save on space but keep decent quality.

If you happen to end up here, good luck if you decide to use this as-is software.

## Running the Twitch Recorder

To start monitoring a channel and record it when it shows up, run the `record_stream.py` script as follows:

```
python3 record_stream.py --channel <twitch_channel_name> --path <recording_dest_path>
```

Where `<twitch_channel_name>` comes from `twitch.tv/<twitch_channel_name>` for the broadcaster and `<recording_dest_path>` is the path where you'd like the software to create folders and stream files.

## Running the Transcoder

To start transcoding your recorded streams, install `ffmpeg` and run the `transcode.py` script as follows:

```
python3 transcode.py --path <recording_dest_path>
```

I recommend running these in their own `gnu-screen` or `tmux` sessions so you can detach and leave them running long-term.

Tweak the `ffmpeg` transcoding configuration and/or quality choices for the live stream as desired.

Thanks!