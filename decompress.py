#!/usr/bin/env python3
"""
decompress.py - Decompress .gz and .tar files found in a source directory.

Supported formats:
  .tar        - uncompressed tar archive
  .tar.gz     - gzip-compressed tar archive
  .tgz        - gzip-compressed tar archive (short form)
  .tar.bz2    - bzip2-compressed tar archive
  .tar.xz     - xz-compressed tar archive
  .gz         - single gzip-compressed file

Usage:
  python decompress.py [source_path] [output_path]

  source_path  : directory containing files to decompress (default: ./source)
  output_path  : directory where decompressed files will be placed (default: same as source_path)
"""

import argparse
import gzip
import os
import shutil
import tarfile


def _safe_extract(tar: tarfile.TarFile, output_dir: str) -> None:
    """Extract tar members only to paths inside output_dir (prevents path traversal)."""
    abs_output = os.path.realpath(output_dir)
    for member in tar.getmembers():
        member_path = os.path.realpath(os.path.join(abs_output, member.name))
        if not member_path.startswith(abs_output + os.sep) and member_path != abs_output:
            raise ValueError(f"Unsafe path in archive: {member.name}")
    tar.extractall(path=output_dir)


def decompress_tar(filepath: str, output_dir: str) -> None:
    with tarfile.open(filepath, "r:*") as tar:
        _safe_extract(tar, output_dir)
    print(f"[OK] Extracted tar archive: {filepath} -> {output_dir}")


def decompress_gz(filepath: str, output_dir: str) -> None:
    filename = os.path.basename(filepath)
    # Strip the .gz extension to get the output filename
    out_filename = filename[:-3] if filename.endswith(".gz") else filename
    out_path = os.path.join(output_dir, out_filename)
    with gzip.open(filepath, "rb") as gz_file, open(out_path, "wb") as out_file:
        shutil.copyfileobj(gz_file, out_file)
    print(f"[OK] Decompressed gz file: {filepath} -> {out_path}")


def process_directory(source_path: str, output_path: str) -> None:
    if not os.path.isdir(source_path):
        print(f"[ERROR] Source path does not exist or is not a directory: {source_path}")
        return

    os.makedirs(output_path, exist_ok=True)

    files = os.listdir(source_path)
    if not files:
        print(f"[INFO] No files found in: {source_path}")
        return

    processed = 0
    for filename in sorted(files):
        filepath = os.path.join(source_path, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            lower = filename.lower()
            if lower.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tar.xz", ".tar")):
                decompress_tar(filepath, output_path)
                processed += 1
            elif lower.endswith(".gz"):
                decompress_gz(filepath, output_path)
                processed += 1
            else:
                print(f"[SKIP] Unsupported format: {filename}")
        except Exception as exc:
            print(f"[ERROR] Failed to decompress {filename}: {exc}")

    print(f"\nDone. {processed} file(s) decompressed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Decompress .gz and .tar files found in a source directory."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="./source",
        help="Path to the directory containing files to decompress (default: ./source)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Path to the output directory (default: same as source)",
    )
    args = parser.parse_args()

    source_path = os.path.abspath(args.source)
    output_path = os.path.abspath(args.output) if args.output else source_path

    print(f"Source : {source_path}")
    print(f"Output : {output_path}")
    print()

    process_directory(source_path, output_path)


if __name__ == "__main__":
    main()
