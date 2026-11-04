#!/usr/bin/env python3
"""Regression test for paragraph-aligned GEOS 1.x relocation streams."""
from __future__ import annotations
import struct
import sys
from pathlib import Path

SDK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SDK))
from pcgeos1.geode import parse, resource_bytes


def make_fixture() -> bytes:
    data = bytearray(324)
    data[:4] = bytes.fromhex("c745cf53")
    # GEOS 1.x header: attributes, type, kernel protocol, resource/import/export counts.
    struct.pack_into("<7H", data, 200, 0, 0, 622, 3, 1, 0, 0)
    tail = 224
    struct.pack_into("<H", data, tail + 2, 0)
    struct.pack_into("<H", data, tail + 4, 0)
    struct.pack_into("<H", data, tail + 50, 0)
    struct.pack_into("<H", data, tail + 52, 0)
    struct.pack_into("<H", data, tail + 56, 1)

    table = 288
    struct.pack_into("<H", data, table, 3)       # resource size
    struct.pack_into("<I", data, table + 2, 304) # absolute file position
    struct.pack_into("<H", data, table + 6, 4)   # one four-byte relocation
    struct.pack_into("<H", data, table + 8, 0)   # resource flags

    data[304:307] = b"ABC"
    # Poison the 13-byte paragraph gap so a parser using position + size fails.
    data[307:320] = b"\xff" * 13
    data[320:324] = b"\x00\x00\x00\x00"
    return bytes(data)


def main() -> None:
    data = make_fixture()
    info = parse(data, "synthetic-paragraph-alignment-test")
    resource = info["resources"][0]
    assert resource["file_offset"] == 304
    assert resource["relocation_offset"] == 320
    assert resource_bytes(data, info, 0) == b"ABC"
    assert len(info["relocations"]) == 1
    assert info["relocations"][0]["record_file_offset"] == 320
    print("PASS: GEOS 1.x relocation stream starts after paragraph padding")


if __name__ == "__main__":
    main()
