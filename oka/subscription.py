from typing import List

import feedparser
import scrapetube


class Subscription:
    def __init__(
        self,
        url: str,
        title: str = "",
        destination: str = "",
        includes: List = [],
        excludes: List = [],
        retention: int = 0,
        audio_only: bool = False,
    ):
        # TODO: scrape the title if not set
        self.title = title or url
        self.url = url
        self.destination = destination
        self.includes = includes
        self.excludes = excludes
        self.retention = retention
        self.audio_only = audio_only

    @property
    def links(self):
        raise NotImplementedError

    def _filter(self, title: str) -> bool:
        """Returns True if title pass the include and exclude filters."""
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
        return [
            v["videoId"]
            for v in scrapetube.get_channel(channel_url=self.url, sort_by="oldest")
            if self._filter(v["title"]["runs"][0]["text"])
        ]


class PlaylistSubscription(Subscription):
    @property
    def links(self) -> List[str]:
        return [
            v["videoId"]
            for v in scrapetube.get_playlist(playlist_id=self.url)
            if self._filter(v["title"]["runs"][0]["text"])
        ]


class RssSubscription(Subscription):
    @property
    def links(self) -> List[str]:
        return [
            e.link for e in feedparser.parse(self.url).entries if self._filter(e.title)
        ]


def from_config(
    id: str,
    type: str,
    title: str = "",
    includes: List[str] = [],
    excludes: List[str] = [],
    retention: int = 0,
    audio_only: bool = False,
) -> Subscription:
    destination = title or "%(uploader)s"

    if type == "channel":
        if id[0] == "@":
            url = f"https://www.youtube.com/{id}"
        else:
            url = f"https://www.youtube.com/channel/{id}"

        return ChannelSubscription(
            url=url,
            title=title,
            destination=destination,
            includes=includes,
            excludes=excludes,
            retention=retention,
            audio_only=audio_only,
        )
    elif type == "playlist":
        return PlaylistSubscription(
            url=id,
            title=title,
            destination=destination,
            includes=includes,
            excludes=excludes,
            retention=retention,
            audio_only=audio_only,
        )
    elif type == "rss" and id[0] != "@":
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={id}"

        return RssSubscription(
            url=url,
            title=title,
            destination=destination,
            includes=includes,
            excludes=excludes,
            retention=retention,
            audio_only=audio_only,
        )
    else:
        raise ValueError(f"Invalid value for {type} subscription: {id}")
