#!/usr/bin/env python3

from datetime import datetime
import math
from pathlib import Path
from s3 import S3
from urllib.parse import quote, quote_plus


# Globals
with open(Path(__file__).parent / "index.html") as f:
    index = str(f.read())

with open(Path(__file__).parent / "404.html") as f:
    _404 = str(f.read())

s3 = S3()

CDN_URL = "https://kruitana-files.b-cdn.net"


def format_filesize(size_in_bytes: int) -> str:
    if size_in_bytes == 0:
        return "0B"
    prefix = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix_index = int(math.floor(math.log(size_in_bytes, 1024)))
    prefix_divisor = math.pow(1024, prefix_index)
    shrunk_bytes = round(size_in_bytes / prefix_divisor)
    return f"{shrunk_bytes}{prefix[prefix_index]}"


def is_visible(prefix: str) -> bool:
    """Given an S3 object's key, return True if the object should be visible"""
    if prefix == "hidden/" or prefix == "misc/":
        return False

    return not prefix.rstrip("/").rpartition("/")[2].startswith(".")


def format_directory(directory: str) -> str:
    short_name: str = directory.strip("/").rpartition("/")[2] + "/"

    return '<a href="{href}">{filename}</a>{whitespace} {datetime:>17}{filesize:>8}'.format(
        href=f"/{quote_plus(directory, safe='/')}",
        filename=(
            f"{short_name[:50]}" if len(short_name) <= 50 else f"{short_name[:47]}..>"
        ),
        whitespace=" " * (50 - len(short_name)),
        datetime="-",
        filesize="-",
    )


def format_object(s3_object) -> str:
    object_key: str = s3_object["Key"]
    object_datetime: datetime = s3_object["LastModified"]
    object_size_in_bytes: int = s3_object["Size"]

    short_name: str = object_key.rpartition("/")[2]

    return '<a href="{href}">{filename}</a>{whitespace} {datetime}{filesize:>8}'.format(
        href=f"/{quote_plus(object_key.removeprefix('misc/'), safe='/')}",
        filename=(
            f"{short_name[:50]}" if len(short_name) <= 50 else f"{short_name[:47]}..>"
        ),
        whitespace=" " * (50 - len(short_name)),
        datetime=object_datetime.strftime("%d-%b-%Y %R"),
        filesize=format_filesize(object_size_in_bytes),
    )


def redirect(url: str) -> dict:
    return {
        "statusCode": 301,
        "headers": {
            "Content-Type": "text/html",
            "X-Robots-Tag": "noindex, nofollow",
            "Cache-Control": "max-age=86400, stale-while-revalidate=86400, stale-if-error=86400",
            "Location": url,
        },
        "body": "Redirecting...",
    }


def display_directory(path):
    # Display directory.
    # HTML content to be placed inside the <pre> tag.
    html = ""

    # Only add a link to go back on subdirectories.
    if path:
        html += '<a href="../">../</a>\n'

    common_prefixes = s3.get_common_prefixes(path)
    if common_prefixes:
        directories = filter(is_visible, (obj["Prefix"] for obj in common_prefixes))
        html += "\n".join(map(format_directory, directories)) + "\n"

    contents = s3.get_contents(path)
    files = (file for file in contents if is_visible(file["Key"]))
    html += "\n".join(map(format_object, files))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "X-Robots-Tag": "noindex, nofollow",
            "Cache-Control": "max-age=60, stale-while-revalidate=300, stale-if-error=86400",
        },
        "body": index.replace("{index_of}", "/" + path).replace(
            "{list_of_files}", html
        ),
    }


# Possible paths of execution:
# - Load a file (redirect)
# - Redirect to a folder if there was missing /
# - Load a directory (display)
# - Load neither a file nor directory (404)
def lambda_handler(event, context):
    # `path` is unquoted (similar to unquote_plus) and never has a trailing /.
    path: str = event["requestContext"]["http"]["path"]

    # Preserve the trailing slash in `path` if it was present in the original request.
    # This is useful throughout, though especially for the prefix in the S3 call.
    rawPath: str = event["rawPath"]
    if len(rawPath) > 1 and rawPath.endswith("/"):
        path += "/"

    # S3 keys don't begin with /, but the path we're given does.
    path = path.lstrip("/")

    # If the path is a file, then just redirect to the cdn.
    # We also want files in hidden/ and misc/ to be accessible on the root.
    for prefix in ["", "hidden/", "misc/"]:
        # The posix emulation filesystem mount creates files of zero size
        # with the same key as the directory.
        # Checking for the size of the file guards against that attempting
        # to redirect as a file.
        if any(
            prefix + path == obj.get("Key") and obj.get("Size") != 0
            for obj in s3.get_contents(prefix + path)
        ):
            return redirect(f"{CDN_URL}/{prefix}{quote(path)}")

        if any(
            prefix + path + ".html" == obj.get("Key")
            for obj in s3.get_contents(prefix + path)
        ):
            return redirect(f"{CDN_URL}/{prefix}{quote(path)}.html")

    # It looks like the user requested a valid directory, but forgot to append a /.
    if not s3.is_directory(path) and (s3.is_directory(path + "/")):
        return redirect(f"/{quote_plus(path, safe='/')}/")

    if s3.is_directory(path):
        return display_directory(path)

    # If the user had requested a valid file, they would have been redirected by now.
    if not s3.is_directory(path):
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "text/html",
                "X-Robots-Tag": "noindex, nofollow",
                "Cache-Control": "max-age=30, stale-while-revalidate=30, stale-if-error=86400",
            },
            "body": _404.replace(
                "{file_or_page}", "Page" if path.endswith("/") else "File"
            ),
        }
