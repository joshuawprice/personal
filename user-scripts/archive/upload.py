#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import urllib.request
from abc import ABC, abstractmethod
from typing import BinaryIO

import requests


class FilesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Remove duplicates based on file path
        files = []
        for value in values:
            for file in files:
                if value.name == file.name:
                    value.close()
                    break
            else:
                files.append(value)

        setattr(namespace, self.dest, files)


class SingleAppendAction(argparse.Action):
    """
    A custom action similar to the default append action. However, only
    appends one instance of a data type to dest.

    Intended to be used for ensuring uploaders are only added to dest
    once.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # If destinations is empty, add values and return
        if not getattr(namespace, self.dest):
            setattr(namespace, self.dest, [values])
            return

        # Exit if Uploader is already in destinations
        if any((isinstance(x, type(values)) for x in getattr(namespace, self.dest))):
            return

        # Append values to destination then resave destinations
        destinations = getattr(namespace, self.dest)
        destinations.append(values)
        setattr(namespace, self.dest, destinations)


class SingleAppendConstAction(SingleAppendAction):
    """
    A custom action similar to the default append const action. However,
    only appends one instance of a data type to dest.

    Intended to be used for ensuring uploaders are only added to dest
    once.
    """

    def __init__(
        self,
        option_strings,
        dest,
        const,
        default=None,
        required=False,
        help=None,
        metavar=None,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, self.const, option_string)


class Uploader(ABC):
    @abstractmethod
    def upload(self, file: BinaryIO) -> str:
        raise NotImplementedError


class TheNullPointer(Uploader):
    def upload(self, file: BinaryIO) -> str:
        r = requests.post("https://0x0.st", files={"file": file}, timeout=5)
        r.raise_for_status()
        return r.text.strip()


class X0(Uploader):
    def upload(self, file: BinaryIO) -> None:
        r = requests.post("https://x0.at", files={"file": file}, timeout=5)
        r.raise_for_status()
        return r.text.strip()


class Asgard(Uploader):
    def __init__(self, location: str) -> None:
        self.location = location

        # TODO: Look up ssh agents to check if SSH_ASKPASS is really required.
        if not os.getenv("SSH_ASKPASS") and bool(
            subprocess.run(
                ["ssh-add", "-qL"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ).returncode
        ):
            print("SSH_ASKPASS is not set, upload to asgard may fail.", file=sys.stderr)

    def upload(self, file: BinaryIO) -> str:
        for i in range(3):
            if not bool(
                subprocess.run(
                    [
                        "scp",
                        "-qo",
                        "ServerAliveInterval 3",
                        file.name,
                        f"admin@asgard.jprice.uk:/opt/media/{self.location}/",
                    ]
                ).returncode
            ):
                break
        else:
            print("Upload to asgard failed 3 times.")
            sys.exit(1)
        return "https://files.kruitana.com/" + urllib.request.pathname2url(
            file.name.rpartition("/")[2]
        )


class Catgirls(Uploader):
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError
        self.api_key = api_key

    def upload(self, file: BinaryIO) -> str:
        r = requests.post(
            "https://catgirlsare.sexy/api/upload",
            data={"key": self.api_key},
            files={"file": file},
            timeout=5,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.exceptions.HTTPError(r.json()["error"]) from None
        return r.json()["url"]


def send_notification(urls):
    # TODO: Confirm that there's a notification server running.
    # TODO: Determine app name programmatically.
    if len(urls) > 1:
        subprocess.run(
            [
                "notify-send",
                "--urgency=low",
                "--app-name=upload",
                "--icon=folder",
                "Files uploaded",
            ]
        )
        return

    # TODO: Show image in notification if there is one.
    # TODO: Show icon for filetype.

    subprocess.run(
        [
            "notify-send",
            "--urgency=low",
            "--app-name=upload",
            f"File {urls[0].rpartition("/")[2]} uploaded",
        ]
    )


def main():
    # Start parsing options
    parser = argparse.ArgumentParser(
        description="Uploads file to destination specified."
    )
    # Miscellaneous features
    parser.add_argument(
        "-n",
        "--notify",
        action="store_true",
        help="send a notification upon completion",
    )
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="copy the response url to clipboard",
    )

    # Add destinations for the script
    destinations = parser.add_argument_group(
        "destinations",
        """care should be taken when using arguments with optional values as
        if it is given a valid file on your filesystem, it will ignore it""",
    )
    destinations.add_argument(
        "--0x0",
        action=SingleAppendConstAction,
        const=TheNullPointer(),
        dest="destinations",
        help="upload to 0x0.st",
    )
    destinations.add_argument(
        "--x0",
        action=SingleAppendConstAction,
        const=X0(),
        dest="destinations",
        help="upload to x0.at",
    )
    destinations.add_argument(
        "--asgard",
        action=SingleAppendAction,
        nargs="?",
        const=".misc",
        type=Asgard,
        metavar="LOCATION",
        dest="destinations",
        help="upload to asgard",
    )
    destinations.add_argument(
        "--catgirls",
        action=SingleAppendAction,
        nargs="?",
        const="",
        type=Catgirls,
        metavar="API_KEY",
        dest="destinations",
        help="upload to catgirlsare.sexy",
    )

    # Finally, allow files to be uploaded, including - (stdin)
    parser.add_argument(
        "files",
        type=argparse.FileType("rb"),
        action=FilesAction,
        metavar="FILE",
        nargs="+",
        help="file to be uploaded",
    )

    # Save parsed arguments to args object
    args = parser.parse_intermixed_args()

    # Quit if no destinations are given
    if not args.destinations:
        parser.error("at least one destination is required")

    urls = []
    for destination in args.destinations:
        for file in args.files:
            urls.append(destination.upload(file))
            print(urls[len(urls) - 1])
            file.seek(0)

    if args.notify:
        send_notification(urls)


if __name__ == "__main__":
    main()

# vim: shiftwidth=4 softtabstop=4 expandtab
