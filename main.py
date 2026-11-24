#!/usr/bin/env python3
"""Weirdest Job Title entry: publish the title in entry.txt.

The entry text lives in exactly one place, the sibling ``entry.txt``
file. This program copies its raw bytes unchanged to the grader's
``/output/entry.txt`` and then proves the copy by reading the output
back and comparing it byte for byte: a silent truncation or a stray
newline would otherwise reach the judge unnoticed. The gate wants
UTF-8 text of 1 to 60 characters, not only whitespace, so the text is
validated before anything is written.

Why this title: a real-sounding senior job with one hilariously
specific twist. An executive whose whole remit is apologising to a
machine that never forgives is instantly picturable, lands on the
first read, and is stranger than ordinary work without being word
salad -- exactly what the judge's brief rewards.
"""

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EntryConfig:
    """Everything the gate and the grader pin down, in one place."""

    max_chars: int = 60
    source_name: str = "entry.txt"
    output_path: Path = Path("/output/entry.txt")


class EntryError(ValueError):
    """The entry text cannot be published as it stands."""


def read_source(config, repo_root):
    """Return the entry file's raw bytes after validating its text."""
    source = repo_root / config.source_name
    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EntryError("entry.txt is not valid UTF-8") from exc
    if not text.strip():
        raise EntryError("entry.txt holds only whitespace")
    if text != text.strip():
        raise EntryError("entry.txt has leading or trailing whitespace")
    if len(text) > config.max_chars:
        raise EntryError(
            f"entry is {len(text)} chars, over the {config.max_chars} cap"
        )
    return raw, text


def publish(config, raw):
    """Write the bytes verbatim, then verify the copy byte for byte."""
    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    config.output_path.write_bytes(raw)
    if config.output_path.read_bytes() != raw:
        raise EntryError("output does not match entry.txt byte for byte")


def main(argv=None):
    config = EntryConfig()
    repo_root = Path(__file__).resolve().parent
    raw, text = read_source(config, repo_root)
    publish(config, raw)
    print(f"wrote {len(text)} chars to {config.output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
