import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import feedparser
import scrapetube

from oka.common import config, persistence

logger = logging.getLogger(__name__)


class Subscription:
    def __init__(
        self,
        url: str,
        destination: str = "",
        includes: List = [],
        excludes: List = [],
        retention: int = 0,
        audio_only: bool = False,
    ):
        self.url = url
        self.destination = destination
        self.includes = includes
        self.excludes = excludes
        self.retention = retention
        self.audio_only = audio_only

    @property
    def links(self):
        raise NotImplementedError

    @property
    def last_episode(self):
        data = persistence.get(self.destination) or {}

        if not data.get("last_episode"):
            data["last_episode"] = 0
            persistence.set(self.destination, data)

        return data["last_episode"]

    @last_episode.setter
    def last_episode(self, value: int):
        data = persistence.get(self.destination) or {}

        data["last_episode"] = value
        persistence.set(self.destination, data)

    def _filter(self, video: dict) -> bool:
        """Returns True if title pass the include and exclude filters."""
        title = video["title"]["runs"][0]["text"]

        rtn = True
        if self.includes:
            rtn = False
            for include in self.includes:
                if include.lower() in title.lower():
                    rtn = True
                    break
        if self.excludes:
            for exclude in self.excludes:
                if exclude.lower() in title.lower():
                    rtn = False
                    break

        return rtn


class ChannelSubscription(Subscription):
    @property
    def links(self) -> List[str]:
        links = [
            v["videoId"]
            for v in scrapetube.get_channel(
                channel_url=self.url, sort_by="newest", limit=300
            )
            if self._filter(v)
        ]

        links.reverse()

        return links


class PlaylistSubscription(Subscription):
    @property
    def links(self) -> List[str]:
        return [
            v["videoId"]
            for v in scrapetube.get_playlist(playlist_id=self.url)
            if self._filter(v)
        ]


def from_config(
    id: str,
    type: str,
    destination: str,
    includes: List[str] = [],
    excludes: List[str] = [],
    retention: int = 0,
    audio_only: bool = False,
) -> Subscription:
    if type == "channel":
        if id[0] == "@":
            url = f"https://www.youtube.com/{id}"
        else:
            url = f"https://www.youtube.com/channel/{id}"

        return ChannelSubscription(
            url=url,
            destination=destination,
            includes=includes,
            excludes=excludes,
            retention=retention,
            audio_only=audio_only,
        )
    elif type == "playlist":
        return PlaylistSubscription(
            url=id,
            destination=destination,
            includes=includes,
            excludes=excludes,
            retention=retention,
            audio_only=audio_only,
        )
    else:
        raise ValueError(f"Invalid value for {type} subscription: {id}")
