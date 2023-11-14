# Oka

My personal solution to consume YouTube more consciously, and algorithm free.

## Features

- Automatic video download, based on a channel id, a channel name (eg. "@channelname") or a playlist id.
- Title based filters.
- Automatic video deletion based on age.
- Configurable through a simple json file.
- Audio only downloads.
- Ignores videos shorter than a minute.

## Usage

Oka comes with two git-like subcommands:

- `download`: Downloads up to `max_downloads` for each subscription in the configuration file.
- `purge`: Deletes subscription videos older than `retention` days if the retention is not 0.

## Installation

For the moment, clone and run `oka.sh`. This will create the virtualenv if it doesn't exists.

```sh
git clone git@github.com:twissell-/oka.git
cd oka
./oka.sh
```

Additionally, you can add an alias in your `.bashrc`:

```sh
echo "
# Oka
export OKA_CONFIG_FILE=\"$(readlink -f config.json)\"
alias oka=\"$(readlink -f oka.sh)\"
" > ~/.bashrc
```

## Configuration

The configuration files has two sections that are explain below. You can start by copying the template and setting the values to your liking.

```sh
cp config.template.json config.json
```

### `downlaoder` section

| Option               | Description                                                                               | Mandatory | Default |
| -------------------- | ----------------------------------------------------------------------------------------- | :-------: | ------- |
| directory            | Path to the base directory where the videos will be downloaded                            |    Yes    |         |
| concurrent_fragments | Number of fragments of a dash/hlsnative video that should be downloaded concurrently      |    No     | `4`     |
| download_archive     | Path to the file where downloaded videos will be recorded to avoid downloading them twice |    Yes    |         |

### `subscriptions` section

`subscriptions` is a list of objects, each with the following options:

| Option        | Description                                                                                                         | Mandatory | Default |
| ------------- | ------------------------------------------------------------------------------------------------------------------- | :-------: | ------- |
| id            | Either a channel id, a playlist id, or a channel username (@username)                                               |    Yes    |         |
| destination   | A name to identify the subscription. Downloads will be placed on `{downloader.directory}/{substiption.destination}` |    Yes    |         |
| type          | One of "channel\|playlist"                                                                                          |    Yes    |         |
| includes      | List of strings. Download only videos with one of these terms in its title. Case insensitive                        |    No     | `[]`    |
| excludes      | List of strings. Do not download videos with one of these terms in its title. Case insensitive                      |    No     | `[]`    |
| retention     | Number of days a video should be kept, based on the download date. `0` disables this feature.                       |    No     | `0`     |
| audio_only    | If `true`, converts the downloaded video to audio.                                                                  |    No     | `false` |
| reverse_order | Playlist type only. If `true`, downloads the playlist videos starting from the last (higher index) one.             |    No     | `false` |

#### Clarifications

- I strongly recommend setting a title for `playlist` subscriptions. That will cause all videos from that playlist to be downloaded in the same folder instead of each in their respective channel folder.
- The `channel` type will download videos from the list of all videos of a channel.
- The `channel` type will download only from the newest 300 videos.
- If `retention` is not `0`, only videos between `retention` days and now will be downloaded.
- When using both **filters** `includes` are checked first, then `excludes`, meaning the later will apply only to those titles matching the former. Here's an example:

Given these filters:

```json
"includes": ["Extra History"],
"excludes": ["LIES"]
```

and these titles:

```
Across the Silk Road - The Buddhist Expansion #5 - Extra History
King Arthur vs. Excalibur - European Arthurian Legend - Extra Mythology
The Buddhist Expansion - LIES - Extra History
```

Oka will match only:

```
Across the Silk Road - The Buddhist Expansion #5 - Extra History
```
