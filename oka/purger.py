import os
import time
from pathlib import Path

from oka import config
from oka.subscription import Subscription


def purge(subscription: Subscription):
    files_path = config.get("downloader.directory")
    now = time.time()

    if not subscription.retention:
        return

    if not subscription.title:
        print(f"Can't purge subscription without title ({subscription.id}).")
        return

    for item in Path(files_path).glob(f"{subscription.destination}/*"):
        if item.is_file():
            if os.stat(item).st_mtime < now - subscription.retention * 86400:
                print(f"Deleting: {str(item.absolute())}")
                os.remove(item)
