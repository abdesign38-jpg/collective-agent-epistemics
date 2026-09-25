#!/usr/bin/env python3
"""Placeholder for building browser-ready replay snapshots from experiment outputs."""

from pathlib import Path


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "public" / "data"
    out.mkdir(parents=True, exist_ok=True)
    print(f"Snapshot build placeholder. Output dir ready: {out}")


if __name__ == "__main__":
    main()
