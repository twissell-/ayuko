import logging
from os import path

import yt_dlp
from yt_dlp.YoutubeDL import MaxDownloadsReached

from oka.common import config
from oka.subscription import PlaylistSubscription, Subscription

logger = logging.getLogger(__name__)


class Downloader:
    pass


def _filter(info, *, incomplete):
    """Download only videos longer than a minute (or with unknown duration) and skip lives."""
    duration = info.get("duration")
    if duration and duration < 60:
        return "The video is too short"

    if info.get("is_live"):
        return "The video is live"


_YDL_BASE_OPTIONS = {
    "match_filter": _filter,
    # "format": None,
    # "outtmpl": None,
    "concurrent_fragment_downloads": config.get("downloader.concurrent_fragments"),
    "download_archive": config.get("downloader.download_archive"),
    "max_downloads": 1,
    "quiet": True,
    "no_warnings": True,
    # "simulate": True,
}


def download(subscription: Subscription):
    episode = subscription.last_episode + 1
    file_template = (
        f"{subscription.destination} - {episode} - %(title)s [%(id)s].%(ext)s"
    )
    ydl_opts = _YDL_BASE_OPTIONS.copy()

    ydl_opts["outtmpl"] = path.join(
        config.get("downloader.directory"), subscription.destination, file_template
    )

    if subscription.retention:
        ydl_opts["daterange"] = yt_dlp.utils.DateRange(
            f"today-{subscription.retention}day"
        )

    if subscription.reverse_order:
        ydl_opts["playlistreverse"] = subscription.reverse_order

    if subscription.audio_only:
        ydl_opts["postprocessors"] = [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ]
    else:
        # ydl_opts["format"] = "wv*[ext=mp4]+ba[ext=m4a]/w[ext=mp4] / wv*+wa/b"
        ydl_opts["format"] = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b"

    try:
        if _download(ydl_opts, subscription.links):
            logger.info(f"Error downloading from {subscription.url}")

    except MaxDownloadsReached:
        subscription.last_episode = episode
        logger.info(f"Max downloads reached for {subscription.url}")


def _download(ydl_options: dict, links: list):
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        # returns the error code
        return ydl.download(links)
