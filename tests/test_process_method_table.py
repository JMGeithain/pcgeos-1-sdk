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
    def test_far_pointers_store_resource_before_offset(self):
        methods = [
            (0x0A01, "native_open"),
            (0x0A03, "native_close"),
            (0x0004, "native_attach"),
        ]
        symbols = {
            "native_open": 0x002F,
            "native_close": 0x0071,
            "native_attach": 0x0068,
        }
        dgroup = bytearray(512)

        relocations = write_process_methods(dgroup, methods, symbols)

        self.assertEqual(struct.unpack_from("<H", dgroup, 0x46)[0], 3)
        self.assertEqual(
            [struct.unpack_from("<H", dgroup, 0x52 + 2 * i)[0] for i in range(3)],
            [0x0A01, 0x0A03, 0x0004],
        )
        expected_handlers = [0x002F, 0x0071, 0x0068]
        for i, handler in enumerate(expected_handlers):
            offset = 0x52 + 2 * len(methods) + 4 * i
            self.assertEqual(struct.unpack_from("<HH", dgroup, offset), (2, handler))
            self.assertEqual(relocations[i], (0x22, 0, offset))

    def test_missing_handler_symbol_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing method symbol"):
            write_process_methods(bytearray(512), [(0x0A01, "not_present")], {})


if __name__ == "__main__":
    unittest.main()
