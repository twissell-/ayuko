#!/usr/bin/env python3

import logging
from logging.handlers import RotatingFileHandler

import typer

from oka import config, downloader, purger, subscription

root_logger = logging.getLogger("")
root_logger.setLevel(logging.DEBUG)

log_handler = RotatingFileHandler("./oka.log", backupCount=3)
log_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
root_logger.addHandler(log_handler)
log_handler.doRollover()

oka = typer.Typer()


@oka.command(
    help="Searchs torrents for new episodes for each anime in watching list and add them to qBitTorrent."
)
def download(
    verbose: bool = typer.Option(False),
):
    if verbose:
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
        log_handler.setLevel(logging.INFO)
        root_logger.addHandler(log_handler)

    for sub_config in config.get("subscriptions"):
        sub = subscription.from_config(**sub_config)
        downloader.download(sub)


@oka.command(
    help="Searchs torrents for new episodes for each anime in watching list and add them to qBitTorrent."
)
def purge(
    verbose: bool = typer.Option(False),
):
    if verbose:
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
        log_handler.setLevel(logging.INFO)
        root_logger.addHandler(log_handler)

    for sub_config in config.get("subscriptions"):
        sub = subscription.from_config(**sub_config)
        purger.purge(sub)


if __name__ == "__main__":
    oka()
