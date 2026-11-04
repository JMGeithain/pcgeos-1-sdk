# SDK tests

Run against your own matching target archive:

```sh
python3 tests/selftest.py --gwp /path/to/GWP2.zip
```

On a Linux development machine with both compiler families installed:

```sh
python3 tests/selftest.py --gwp /path/to/GWP2.zip --all-toolchains
```

The self-test builds a temporary copy of the Hello example and checks the resulting geode format, kernel protocol, UI import, permanent identity, resources and relocations. It does not boot GEOS.

Run the parser's paragraph-alignment regression independently:

```sh
python3 tests/test_geode_alignment.py
```

This synthetic test places relocation records after a nonzero paragraph gap and poisons the gap bytes, so a parser that reads at position + size fails.
