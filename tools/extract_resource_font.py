#!/usr/bin/env python3
"""Extract the first sfnt resource from a classic Mac resource fork."""

import argparse
import struct
from pathlib import Path


def extract(source: Path, destination: Path) -> None:
    data = source.read_bytes()
    data_offset, map_offset, _, _ = struct.unpack(">IIII", data[:16])
    type_list_offset, _ = struct.unpack(">HH", data[map_offset + 24:map_offset + 28])
    type_list = map_offset + type_list_offset
    type_count = struct.unpack(">H", data[type_list:type_list + 2])[0] + 1
    for index in range(type_count):
        entry = type_list + 2 + index * 8
        resource_type = data[entry:entry + 4]
        count, references = struct.unpack(">HH", data[entry + 4:entry + 8])
        if resource_type != b"sfnt":
            continue
        reference = type_list + references
        resource_offset = int.from_bytes(data[reference + 5:reference + 8], "big")
        position = data_offset + resource_offset
        length = struct.unpack(">I", data[position:position + 4])[0]
        destination.write_bytes(data[position + 4:position + 4 + length])
        print(f"Extracted {length} bytes to {destination}")
        return
    raise SystemExit("No sfnt resource found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    extract(args.source, args.destination)
