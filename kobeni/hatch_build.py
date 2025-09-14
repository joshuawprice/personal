import subprocess
import sys
from pathlib import Path

import google.protobuf
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class ProtocBuildHook(BuildHookInterface):
    PLUGIN_NAME = "protoc"

    def initialize(self, version, build_data):
        """Run protoc to generate Python files from .proto files"""
        src_dir = Path("kobeni")

        if not src_dir.exists():
            print(f"Warning: Proto directory {src_dir} not found")
            return

        proto_files = list(src_dir.glob("*.proto"))

        if not proto_files:
            return

        # Protobuf's runtime needs to be equal or newer to the generated python module version.
        # Therefore check that the python protobuf version is at least as new as the version on the current system.
        python_version = google.protobuf.__version__.partition(".")[2]

        try:
            result = subprocess.run(
                ["protoc", "--version"], capture_output=True, text=True
            )
            protoc_version = result.stdout.strip().split()[-1]
        except FileNotFoundError:
            protoc_version = "protoc not found in PATH"
            sys.exit(1)

        if protoc_version.partition(".")[0] > python_version.partition(".")[0] or (
            protoc_version.partition(".")[0] == python_version.partition(".")[0]
            and protoc_version.partition(".")[2] > python_version.partition(".")[2]
        ):
            print("protoc version newer than project's protobuf version. quitting.")
            sys.exit(1)

        # Run protoc for each .proto file
        for proto_file in proto_files:
            cmd = [
                "protoc",
                f"--proto_path={src_dir}",
                f"--python_out={src_dir}",
                str(proto_file),
            ]

            print(f"Running: {' '.join(cmd)}")

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"Successfully compiled {proto_file.name}")
            except subprocess.CalledProcessError as e:
                print(f"Error compiling {proto_file.name}: {e}")
                print(f"stdout: {e.stdout}")
                print(f"stderr: {e.stderr}")
                sys.exit(1)
