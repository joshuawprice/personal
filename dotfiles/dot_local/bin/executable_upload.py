#!/usr/bin/env python3

import argparse
import os
import sys
import io


# Dedupe input files based on absolute file path
class files(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Remove duplicates
        for i in range(0, len(values)):
            for j in range(i + 1, len(values)):
                if (os.path.abspath(values[i].name) == os.path.abspath(values[j].name)):
                    values.pop(j)

        # Append extra files found
        for i in extra_files:
            values.append(i)

        setattr(namespace, self.dest, values)


class destinations_with_optional_value(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if not value.endswith("/"): 
            if os.path.isfile(value):
                if getattr(namespace, "files") != None:
                    print(f"Local file given to {option_string} flag. Dazed and confused, but trying to continue", file=sys.stderr)
                else:
                    extra_files.append(open(value, 'rb'))
                    value=self.const
        else:
            value = value.rstrip("/")

        setattr(namespace, self.dest, value)

def at_least_one_dest(args):
    destinations = ["0x0", "x0", "asgard", "catgirls", "clipboard"]
    for i in destinations:
        if getattr(args, i) != None and getattr(args, i) != False:
            return True
    return False


def main():
    # Start parsing options
    parser = argparse.ArgumentParser(description="Uploads file to destination specified.")
    # Miscellaneous features
    parser.add_argument("-n", "--notify", action="store_true", help="send a notification upon completion")
    parser.add_argument("-c", "--clipboard", action="store_true", help="copy the response url to clipboard")

    # Add destinations for the script
    destinations = parser.add_argument_group("destinations", "care should be taken when using arguments with optional values as if it is given a valid file on your filesystem, it will ignore it")
    destinations.add_argument("--0x0", action="store_true", help="upload to 0x0.st")
    destinations.add_argument("--x0", action="store_true", help="upload to x0.at")
    destinations.add_argument("--asgard", nargs='?', const=".misc", action=destinations_with_optional_value, help="upload to asgard")
    destinations.add_argument("--catgirls", nargs='?', action=destinations_with_optional_value, const="63850fbc6c1416658bc42a63c6fd999590ae06161d5f77a1cd591faade2d9d9f", help="upload to catgirlsare.sexy")

    # Finally, allow files to be uploaded, including - (stdin)
    parser.add_argument("files", type=argparse.FileType('rb'), metavar="FILE", nargs="+", help="file to be uploaded", action=files)

    # Save parsed arguments to args object
    args = parser.parse_args()
    # TODO: Switch to intermixed parsing
    #args = parser.parse_intermixed_args()

    # Debugging
    print(args.files, file=sys.stderr)
    print(args, file=sys.stderr)

    # Quit if no destinations are given
    if not at_least_one_dest(args):
        parser.error("at least one destination is required")

    # Reminder: Make uploader classes!


if __name__ == "__main__":
    extra_files = list()
    main()

# vim: softtabstop=4 shiftwidth=4 expandtab
