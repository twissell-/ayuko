#!/usr/bin/env python3

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import typer

from oka import config, downloader, purger, subscription

oka_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

root_logger = logging.getLogger("")
root_logger.setLevel(logging.DEBUG)

log_handler = RotatingFileHandler(f"{oka_dir}/oka.log", backupCount=3)
log_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
root_logger.addHandler(log_handler)
log_handler.doRollover()

oka = typer.Typer(no_args_is_help=True)


@oka.command(
    help="Downloads up to `max_downloads` for each subscription in the configuration file"
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
    help="Deletes subscription videos older than `retention` days if the retention is not 0"
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
    oka(prog_name="oka")
