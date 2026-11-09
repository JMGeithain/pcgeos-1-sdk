#!/usr/bin/env python3
from __future__ import annotations

import struct
import sys
import unittest
from pathlib import Path

SDK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SDK))

from pcgeos1.packer import write_process_methods


class ProcessMethodTableTests(unittest.TestCase):
    def test_far_pointers_store_offset_before_resource(self):
        methods = [
            (0x0A01, "native_open"),
            (0x0A03, "native_close"),
            (0x0004, "native_attach"),
        ]
        symbols = {
            "native_open": 0x0000,
            "native_close": 0x0038,
            "native_attach": 0x007A,
        }
        dgroup = bytearray(512)

        relocations = write_process_methods(dgroup, methods, symbols)

        self.assertEqual(struct.unpack_from("<H", dgroup, 0x46)[0], 3)
        self.assertEqual(
            [struct.unpack_from("<H", dgroup, 0x52 + 2 * i)[0] for i in range(3)],
            [0x0A01, 0x0A03, 0x0004],
        )
        pointer_table = 0x52 + 2 * len(methods)
        expected_offsets = [0x0000, 0x0038, 0x007A]
        for i, expected_offset in enumerate(expected_offsets):
            pointer = pointer_table + 4 * i
            self.assertEqual(struct.unpack_from("<HH", dgroup, pointer), (expected_offset, 2))
            self.assertEqual(relocations[i], (0x22, 0, pointer + 2))

    def test_missing_handler_symbol_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing method symbol"):
            write_process_methods(bytearray(512), [(0x0A01, "not_present")], {})


if __name__ == "__main__":
    unittest.main()
