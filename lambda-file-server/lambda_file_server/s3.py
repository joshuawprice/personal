import boto3
from collections import OrderedDict
from itertools import accumulate, chain, pairwise
import os
from time import time


# With a 128MB function my max memory usage was 82MB, so lets round up to 90.
# That gives me 38 bytes of free memory for my cache.abs
# Now, with a small directory size, the a dict from this cache takes up about 1500 bytes.
# Lets round that up to 15000 for safety.abs
# 38 * 1000 * 1000 / 15000 = ~2500
def TimeBoundedLRU(func, maxsize=2048, maxage=60):
    "LRU Cache that invalidates and refreshes old entries."
    cache = OrderedDict()  # { args : (timestamp, result)}

    def inner(*args):
        if args in cache:
            cache.move_to_end(args)
            timestamp, result = cache[args]
            if time() - timestamp <= maxage:
                return result
        result = func(*args)
        cache[args] = time(), result
        if len(cache) > maxsize:
            cache.popitem(0)
        return result

    return inner


class S3:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=os.environ.get("REGION"),
            endpoint_url=os.environ.get("ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
        )

    def list_objects(self, path: str):
        head, _ = os.path.split(path)

        if not head:
            return self._list_objects_cached(path)

        # We only want to cache valid directories.
        for current_path, next_path in pairwise(
            accumulate(chain([""], head.split("/")), lambda x, y: os.path.join(x, y))
        ):
            if current_path:
                current_path += "/"

            objects = self._list_objects_cached(current_path)

            if next_path + "/" not in (
                p["Prefix"] for p in objects.get("CommonPrefixes", [])
            ):
                # We may look for any missing files in misc and hidden,
                # so one more api call is expected.
                return {}

        # We're only going to cache the directory, manually filter the response.
        objects = self._list_objects_cached(head + "/")
        objects = objects.copy()

        contents = objects.get("Contents", [])
        common_prefixes = objects.get("CommonPrefixes", [])

        objects["Contents"] = [x for x in contents if x["Key"].startswith(path)]
        objects["CommonPrefixes"] = [
            x for x in common_prefixes if x["Prefix"].startswith(path)
        ]
        objects["Prefix"] = path

        return objects

    @TimeBoundedLRU
    def _list_objects_cached(self, prefix):
        return self.s3.list_objects_v2(Bucket="asgard1", Delimiter="/", Prefix=prefix)

    def get_contents(self, prefix: str) -> list:
        return self.list_objects(prefix).get("Contents", [])

    def get_common_prefixes(self, prefix: str) -> list[dict[str, str]]:
        return self.list_objects(prefix).get("CommonPrefixes", [])

    def get_key_count(self, prefix: str) -> int:
        return self.list_objects(prefix).get("KeyCount", 0)

    def is_directory(self, path: str):
        # Root is represented by "".
        if not path:
            return True

        if not path.endswith("/"):
            return False

        # Don't allow access to hidden directories.
        if (
            any(segment.startswith(".") for segment in path.split("/"))
            or path.partition("/")[0] == "hidden"
        ):
            return False

        common_prefixes = self.get_common_prefixes(path)
        key_count = self.get_key_count(path)

        # Testing against contents here would break the is_viewable_directory(path + "/") test.
        return bool(key_count) and all(
            prefix["Prefix"].startswith(path) for prefix in common_prefixes
        )